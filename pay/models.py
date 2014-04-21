# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

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


class Product(TimeStampedModel):
    """List of products and their price."""

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return '{}'.format(self.title)

reversion.register(Product)


class PaymentState(TimeStampedModel):

    DUE = 'due'
    FAIL = 'fail'
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

    email = models.EmailField()
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=100)
    quantity = models.IntegerField()
    # we store the price in case the product is edited!
    price = models.DecimalField(max_digits=8, decimal_places=2)
    state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )
    url = models.CharField(
        max_length=100,
        help_text='redirect to this location after payment.'
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

    def _description(self):
        return '{} ({} x £{:.2f})'.format(self.title, self.quantity, self.price)
    description = property(_description)

    def _total(self):
        return self.price * self.quantity
    total = property(_total)

    def check_can_pay(self):
        if not self.state.slug in (PaymentState.DUE, PaymentState.FAIL):
            raise PayError(
                'Cannot pay this transaction (it is not due or '
                'failed earlier) [{}]'.format(self.pk)
            )

    def is_paid(self):
        return self.state.slug == PaymentState.PAID

    def save_token(self, token):
        self.check_can_pay()
        self.token = token
        self.save()

    def set_paid(self):
        self.state = PaymentState.objects.get(slug=PaymentState.PAID)
        self.content_object.set_paid()
        self.save()

    def set_payment_failed(self):
        self.state = PaymentState.objects.get(slug=PaymentState.FAIL)
        self.content_object.set_payment_failed()
        self.save()

    def total_as_pennies(self):
        return int(self.total * Decimal('100'))

reversion.register(Payment)
