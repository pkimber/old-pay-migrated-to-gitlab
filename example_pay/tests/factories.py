# -*- encoding: utf-8 -*-
import factory

from example_pay.models import (
    CardRefresh,
    SalesLedger,
)
from stock.tests.factories import ProductFactory


class CardRefreshFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CardRefresh

    @factory.sequence
    def email(n):
        return '{:02d}@pkimber.net'.format(n)

    @factory.sequence
    def name(n):
        return 'title_{:02d}'.format(n)


class SalesLedgerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SalesLedger

    product = factory.SubFactory(ProductFactory)
    quantity = 1

    @factory.sequence
    def email(n):
        return '{:02d}@pkimber.net'.format(n)

    @factory.sequence
    def title(n):
        return 'title_{:02d}'.format(n)
