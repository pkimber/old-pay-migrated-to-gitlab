# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

import factory

from pay.models import Payment


class PaymentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Payment

    quantity = 1
    price = Decimal('10.00')

    @factory.sequence
    def email(n):
        return '{:02d}@pkimber.net'.format(n)

    @factory.sequence
    def name(n):
        return 'Mr {} Smith'.format(n)

    @factory.sequence
    def title(n):
        return 'Purchase ref {:03d}'.format(n)
