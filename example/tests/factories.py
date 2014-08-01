# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from example.models import SalesLedger
from stock.tests.factories import ProductFactory


class SalesLedgerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SalesLedger

    product = factory.SubFactory(ProductFactory)
    quantity = 1
