# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class SalesLedger(models.Model):
    """List of prices."""

    title = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Sales ledger'
        verbose_name_plural = 'Sales ledger'

    def __str__(self):
        return '{}'.format(self.title)

    def set_paid(self):
        self.is_paid = True
        self.save()

    def set_payment_failed(self):
        self.is_paid = False
        self.save()
