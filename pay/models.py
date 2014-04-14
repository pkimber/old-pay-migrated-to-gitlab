# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


STATE_DUE = 'due'


def _default_payment_state():
    return PaymentState.objects.get(slug=STATE_DUE)


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

    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    state = models.ForeignKey(
        PaymentState,
        default=_default_payment_state,
    )
    # who requested the payment
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'

    def __str__(self):
        return '{}'.format(self.total)

    def _total(self):
        return self.product.price * self.quantity
    total = property(_total)

reversion.register(Payment)
