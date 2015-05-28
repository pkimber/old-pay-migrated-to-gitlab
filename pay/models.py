# -*- encoding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

import reversion

from finance.models import (
    legacy_vat_code,
    VatCode,
)
from base.model_utils import TimeStampedModel
from stock.models import Product


def default_payment_state():
    return PaymentState.objects.get(slug=PaymentState.DUE).pk


class PayError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class PaymentState(TimeStampedModel):

    DUE = 'due'
    FAIL = 'fail'
    LATER ='later'
    PAID = 'paid'

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Payment state'
        verbose_name_plural = 'Payment state'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(PaymentState)


class PaymentManager(models.Manager):

    def create_payment(self, name, email, content_object):
        """Create a payment.

        - 'name' is the name of the customer.

        """
        obj = self.model(
            content_object=content_object,
            email=email,
            name=name,
        )
        obj.save()
        return obj


class Payment(TimeStampedModel):
    """List of payments."""

    name = models.TextField()
    email = models.EmailField()
    state = models.ForeignKey(PaymentState, default=default_payment_state)
    url = models.CharField(
        max_length=100,
        help_text='redirect to this location after payment.'
    )
    url_failure = models.CharField(
        max_length=100,
        help_text='redirect to this location if the payment fails.'
    )
    # link to the object in the system which requested the payment
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    objects = PaymentManager()

    class Meta:
        ordering = ('pk',)
        # payment should only link to one other object.
        unique_together = ('object_id', 'content_type')
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'

    def __str__(self):
        return '{} = {}'.format(self.description, self.total)

    @property
    def description(self):
        result = []
        for line in self.paymentline_set.all():
            s = ''
            quantity = line.quantity.normalize()
            if quantity > 1:
                s = s + '{} x '.format(quantity)
            s = s + '{} (£{:.2f}'.format(
                line.product.name,
                line.net,
            )
            if line.vat:
                s = s + ' + £{:.2f} vat'.format(line.vat)
            s = s + ')'
            result.append(s)
        return result

    def _set_payment_state(self, payment_state):
        """Mirror payment state to content object (to make queries easy)."""
        self.state = payment_state
        self.save()
        # this method should set the state and save the data
        self.content_object.set_payment_state(payment_state)

    @property
    def total(self):
        result = Decimal()
        for line in self.paymentline_set.all():
            result = result + line.gross
        return result

    @property
    def check_can_pay(self):
        allowed = (PaymentState.DUE, PaymentState.FAIL, PaymentState.LATER)
        if not self.state.slug in allowed:
            raise PayError(
                "Cannot pay this transaction (it did not fail and is not due "
                "now or later) [{}, '{}']".format(self.pk, self.state.slug)
            )
        td = timezone.now() - self.created
        diff = td.days * 1440 + td.seconds / 60
        if abs(diff) > 60:
            raise PayError(
                "Cannot pay this transaction.  It is too old "
                "(or has travelled in time, {} {} {}).".format(
                    self.created.strftime('%d/%m/%Y %H:%M'),
                    timezone.now().strftime('%d/%m/%Y %H:%M'),
                    abs(diff),
                )
            )

    def check_can_pay_later(self):
        if not self.state.slug in (PaymentState.FAIL, PaymentState.LATER):
            raise PayError(
                'Cannot pay this transaction (it is not due to '
                'be paid later or failed) [{}]'.format(self.pk)
            )

    def get_next_line_number(self):
        try:
            self.line_number = self.line_number
        except AttributeError:
            self.line_number = 1
        while(True):
            try:
                self.paymentline_set.get(line_number=self.line_number)
            except PaymentLine.DoesNotExist:
                break
            self.line_number = self.line_number + 1
        return self.line_number

    @property
    def is_paid(self):
        return self.state.slug == PaymentState.PAID

    @property
    def is_pay_later(self):
        return self.state.slug == PaymentState.LATER

    def mail_subject_and_message(self, request):
        if self.is_paid:
            caption = 'payment received'
        elif self.is_pay_later:
            caption = 'request to pay by payment plan (or cheque)'
        else:
            caption = 'unknown request'
        subject = '{} from {}'.format(caption.capitalize(), self.name)
        message = '{} - {} from {}, {}:'.format(
            self.created.strftime('%d/%m/%Y %H:%M'),
            caption,
            self.name,
            self.email,
        )
        message = message + '\n\n{}\n\n{}'.format(
            ', '.join(self.description),
            request.build_absolute_uri(self.content_object.get_absolute_url()),
        )
        return subject, message

    def mail_template_context(self):
        return {
            self.email: dict(
                description=', '.join(self.description),
                name=self.name,
                total='£{:.2f}'.format(self.total),
            ),
        }

    def save_token(self, token):
        self.check_can_pay()
        self.token = token
        self.save()

    def set_paid(self):
        payment_state = PaymentState.objects.get(slug=PaymentState.PAID)
        self._set_payment_state(payment_state)

    def set_payment_failed(self):
        payment_state = PaymentState.objects.get(slug=PaymentState.FAIL)
        self._set_payment_state(payment_state)

    def set_pay_later(self):
        payment_state = PaymentState.objects.get(slug=PaymentState.LATER)
        self._set_payment_state(payment_state)

    def total_as_pennies(self):
        return int(self.total * Decimal('100'))

reversion.register(Payment)


class PaymentLineManager(models.Manager):

    def create_payment_line(
            self, payment, product, quantity, units, vat_code):
        obj = self.model(
            payment=payment,
            product=product,
            line_number=payment.get_next_line_number(),
            quantity=quantity,
            units=units,
            vat_code=vat_code,
        )
        obj.save()
        return obj


class PaymentLine(TimeStampedModel):
    """Payment line.

    Copied from 'InvoiceLine'

    Line numbers for each line increment from 1
    Line total can be calculated by adding the net and vat amounts

    """
    payment = models.ForeignKey(Payment)
    line_number = models.IntegerField()
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    units = models.CharField(max_length=5)
    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat_code = models.ForeignKey(
        VatCode,
        default=legacy_vat_code,
    )
    vat = models.DecimalField(max_digits=8, decimal_places=2)
    save_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0'),
        help_text='Price of the product when the line was saved.'
    )
    save_vat_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=Decimal('0'),
        help_text='VAT rate when the line was saved.',
    )
    objects = PaymentLineManager()

    class Meta:
        ordering = ['line_number',]
        unique_together = ('payment', 'line_number')
        verbose_name = 'Payment line'
        verbose_name_plural = 'Payment lines'

    def __str__(self):
        return "{} {} {} @{}".format(
            self.line_number, self.quantity, self.product.name, self.save_price
        )

    def clean(self):
        if self.price < Decimal():
            raise ValidationError(
                'Price must always be greater than zero. '
                'To make a credit note, use a negative quantity.'
            )

    def save(self, *args, **kwargs):
        """Save a payment line.

        Originally copied from 'InvoiceLine'.

        """
        # copy the current price and vat rate into the 'save' fields
        self.save_price = self.product.price
        self.save_vat_rate = self.vat_code.rate
        self.net = self.save_price * self.quantity
        self.vat = self.save_price * self.quantity * self.save_vat_rate
        # Call the "real" save() method.
        super(PaymentLine, self).save(*args, **kwargs)

    @property
    def gross(self):
        return self.net + self.vat

reversion.register(PaymentLine)


class StripeCustomer(TimeStampedModel):

    email = models.EmailField(unique=True)
    customer_id = models.TextField()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Stripe customer'
        verbose_name_plural = 'Stripe customers'

    def __str__(self):
        return '{} ({})'.format(self.email, self.customer_id)

reversion.register(StripeCustomer)
