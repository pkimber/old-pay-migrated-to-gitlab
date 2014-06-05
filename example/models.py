# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from pay.models import (
    default_payment_state,
    Payment,
    PaymentState,
    Product,
)


class SalesLedger(models.Model):
    """List of prices."""

    email = models.EmailField()
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    payment_state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Sales ledger'
        verbose_name_plural = 'Sales ledger'

    def __str__(self):
        return '{}'.format(self.title)

    def create_payment(self):
        return Payment(**dict(
            content_object=self,
            email=self.email,
            name=self.title,
            price=self.product.price,
            quantity=self.quantity,
            title=self.product.name,
        ))

    @property
    def is_paid(self):
        paid = PaymentState.objects.get(slug=PaymentState.PAID)
        return self.payment_state == paid

    @property
    def can_pay(self):
        due = PaymentState.objects.get(slug=PaymentState.DUE)
        return self.payment_state == due
