# -*- encoding: utf-8 -*-
import factory

from example_pay.models import SalesLedger
from stock.tests.factories import ProductFactory


class SalesLedgerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SalesLedger

    product = factory.SubFactory(ProductFactory)
    quantity = 1
