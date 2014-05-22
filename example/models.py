# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from pay.models import (
    default_payment_state,
    PaymentState,
)


class SalesLedger(models.Model):
    """List of prices."""

    title = models.CharField(max_length=100)
    payment_state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Sales ledger'
        verbose_name_plural = 'Sales ledger'

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def is_paid(self):
        paid = PaymentState.objects.get(slug=PaymentState.PAID)
        return self.payment_state == paid

    def set_paid(self):
        self.is_paid = True
        self.save()

    def set_payment_failed(self):
        self.is_paid = False
        self.save()
