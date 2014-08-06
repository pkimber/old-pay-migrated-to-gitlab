# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

import reversion

from base.model_utils import TimeStampedModel


def default_payment_state():
    return PaymentState.objects.get(slug=PaymentState.DUE)


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


class Payment(TimeStampedModel):
    """List of payments."""

    name = models.TextField()
    email = models.EmailField()
    title = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )
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
        return '{} ({} x £{:.2f})'.format(self.title, self.quantity, self.price)

    def _set_payment_state(self, payment_state):
        """Mirror payment state to content object (to make queries easy)."""
        self.state = payment_state
        self.save()
        self.content_object.payment_state = payment_state
        self.content_object.save()

    def _total(self):
        return self.price * self.quantity
    total = property(_total)

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
            self.description,
            request.build_absolute_uri(self.content_object.get_absolute_url()),
        )
        return subject, message

    def mail_template_context(self):
        return {
            self.email: dict(
                description=self.description,
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
