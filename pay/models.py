# -*- encoding: utf-8 -*-
import logging

from decimal import Decimal

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

import reversion
import stripe

from finance.models import (
    legacy_vat_code,
    VatCode,
)
from base.model_utils import TimeStampedModel
from stock.models import Product


logger = logging.getLogger(__name__)


def default_checkout_state():
    return CheckoutState.objects.get(slug=CheckoutState.DUE).pk


def log_stripe_error(log, e, message):
    log.error(
        'StripeError\n'
        '{}\n'
        'http body: {}\n'
        'http status: {}'.format(
            message,
            e.http_body,
            e.http_status,
        )
    )


class CheckoutError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class CheckoutStateManager(models.Manager):

    @property
    def due(self):
        return self.model.objects.get(slug=self.model.DUE)

    @property
    def fail(self):
        return self.model.objects.get(slug=self.model.FAIL)

    @property
    def success(self):
        return self.model.objects.get(slug=self.model.SUCCESS)


class CheckoutState(TimeStampedModel):

    DUE = 'due'
    FAIL = 'fail'
    SUCCESS = 'success'

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    objects = CheckoutStateManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Payment state'
        verbose_name_plural = 'Payment state'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(CheckoutState)


class CustomerManager(models.Manager):

    def _create_customer(self, email, customer_id):
        obj = self.model(email=email, customer_id=customer_id)
        obj.save()
        return obj

    def _stripe_customer_create(self, email, description, token):
        """Use the Stripe API to create a customer."""
        try:
            return stripe.Customer.create(
                email=email,
                description=description,
                card=token,
            )
        except stripe.StripeError as e:
            log_stripe_error(logger, e, 'create - email: {}'.format(email))

    def _stripe_customer_update(self, customer_id, description, token):
        """Use the Stripe API to update a customer."""
        try:
            stripe_customer = stripe.Customer.retrieve(customer_id)
            stripe_customer.description = description
            stripe_customer.card = token
            stripe_customer.save()
        except stripe.StripeError as e:
            log_stripe_error(logger, e, 'update - id: {}'.format(customer_id))

    def init_customer(self, email, description, token):
        try:
            obj = self.model.objects.get(email=email)
            obj.save()
            self._stripe_customer_update(obj.customer_id, description, token)
        except self.model.DoesNotExist:
            stripe_customer = self._stripe_customer_create(email, description, token)
            obj = self._create_customer(email, token)
        return obj


class Customer(TimeStampedModel):

    email = models.EmailField(unique=True)
    customer_id = models.TextField()
    objects = CustomerManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return '{} {}'.format(self.email, self.customer_id)

    @property
    def has_customer(self):
        return bool(self.customer_id)

reversion.register(Customer)


class CheckoutManager(models.Manager):

    def create_checkout(self, email, description, token, content_object):
        """Create a checkout request."""
        customer = Customer.objects.init_customer(email, description, token)
        obj = self.model(
            content_object=content_object,
            customer=customer,
        )
        obj.save()
        return obj

    def audit(self):
        """Select all valid payments for a list of payments."""
        return self.model.objects.all().order_by('-pk')

    def payments(self):
        return self.audit().filter(state__slug=CheckoutState.SUCCESS)


class Checkout(TimeStampedModel):
    """Checkout."""

    customer = models.ForeignKey(Customer)
    state = models.ForeignKey(CheckoutState, default=default_checkout_state)
    # link to the object in the system which requested the checkout
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    objects = CheckoutManager()

    class Meta:
        ordering = ('pk',)
        # payment should only link to one other object.
        # unique_together = ('object_id', 'content_type')
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return '{}'.format(self.customer.email)

    @property
    def content_object_url(self):
        try:
            return self.content_object.get_absolute_url()
        except AttributeError:
            return None

    #@property
    #def description(self):
    #    result = []
    #    for line in self.paymentline_set.all():
    #        s = ''
    #        quantity = line.quantity_normalize
    #        if quantity > 1:
    #            s = s + '{} x '.format(quantity)
    #        s = s + '{} (£{:.2f}'.format(
    #            line.product.name,
    #            line.net,
    #        )
    #        if line.vat:
    #            s = s + ' + £{:.2f} vat'.format(line.vat)
    #        s = s + ')'
    #        result.append(s)
    #    return result

    #def _set_payment_state(self, payment_state):
    #    """Mirror payment state to content object (to make queries easy)."""
    #    self.state = payment_state
    #    self.save()
    #    # this method should set the state and save the data
    #    self.content_object.set_payment_state(payment_state)

    #@property
    #def total(self):
    #    result = Decimal()
    #    for line in self.paymentline_set.all():
    #        result = result + line.gross
    #    return result

    #@property
    #def check_can_pay(self):
    #   """Probably don't need this method as we won't create this record until
    #   the payment is complete.
    #   """
    #    allowed = (PaymentState.DUE, PaymentState.FAIL, PaymentState.LATER)
    #    if not self.state.slug in allowed:
    #        raise PayError(
    #            "Cannot pay this transaction (it did not fail and is not due "
    #            "now or later) [{}, '{}']".format(self.pk, self.state.slug)
    #        )
    #    td = timezone.now() - self.created
    #    diff = td.days * 1440 + td.seconds / 60
    #    if abs(diff) > 60:
    #        raise PayError(
    #            "Cannot pay this transaction.  It is too old "
    #            "(or has travelled in time, {} {} {}).".format(
    #                self.created.strftime('%d/%m/%Y %H:%M'),
    #                timezone.now().strftime('%d/%m/%Y %H:%M'),
    #                abs(diff),
    #            )
    #        )

    #def check_can_pay_later(self):
    #    if not self.state.slug in (PaymentState.FAIL, PaymentState.LATER):
    #        raise PayError(
    #            'Cannot pay this transaction (it is not due to '
    #            'be paid later or failed) [{}]'.format(self.pk)
    #        )

    #def get_next_line_number(self):
    #    try:
    #        self.line_number = self.line_number
    #    except AttributeError:
    #        self.line_number = 1
    #    while(True):
    #        try:
    #            self.paymentline_set.get(line_number=self.line_number)
    #        except PaymentLine.DoesNotExist:
    #            break
    #        self.line_number = self.line_number + 1
    #    return self.line_number

    #@property
    #def is_paid(self):
    #    return self.state.slug == PaymentState.PAID

    #@property
    #def is_pay_later(self):
    #    return self.state.slug == PaymentState.LATER

    #@property
    #def is_payment_failed(self):
    #    return self.state.slug == PaymentState.FAIL

    #def mail_subject_and_message(self, request):
    #    if self.is_paid:
    #        caption = 'payment received'
    #    elif self.is_pay_later:
    #        caption = 'request to pay by payment plan (or cheque)'
    #    else:
    #        caption = 'unknown request'
    #    subject = '{} from {}'.format(caption.capitalize(), self.name)
    #    message = '{} - {} from {}, {}:'.format(
    #        self.created.strftime('%d/%m/%Y %H:%M'),
    #        caption,
    #        self.name,
    #        self.email,
    #    )
    #    message = message + '\n\n{}\n\n{}'.format(
    #        ', '.join(self.description),
    #        request.build_absolute_uri(self.content_object.get_absolute_url()),
    #    )
    #    return subject, message

    #def mail_template_context(self):
    #    return {
    #        self.email: dict(
    #            description=', '.join(self.description),
    #            name=self.name,
    #            total='£{:.2f}'.format(self.total),
    #        ),
    #    }

    #@property
    #def mail_template_name(self):
    #    """Ask the content object which mail template to use.

    #    The 'payment_state' can be 'PaymentState.PAID' or 'PaymentState.LATER'

    #    """
    #    return self.content_object.mail_template_name

    #def save_token(self, token):
    #    self.check_can_pay
    #    self.token = token
    #    self.save()

    #def set_paid(self):
    #    payment_state = PaymentState.objects.get(slug=PaymentState.PAID)
    #    self._set_payment_state(payment_state)

    #def set_payment_failed(self):
    #    payment_state = PaymentState.objects.get(slug=PaymentState.FAIL)
    #    self._set_payment_state(payment_state)

    #def set_pay_later(self):
    #    payment_state = PaymentState.objects.get(slug=PaymentState.LATER)
    #    self._set_payment_state(payment_state)

    #def total_as_pennies(self):
    #    return int(self.total * Decimal('100'))

reversion.register(Checkout)
