# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from pay.tests.model_maker import (
    make_payment,
    make_product,
)

from example.tests.model_maker import make_sales_ledger


def default_scenario_pay():
    pencil = make_product('Pencil', 'pencil', Decimal('1.32'))
    make_sales_ledger('test@pkimber.net', 'Carol', pencil, 2)
    make_sales_ledger('test@pkimber.net', 'Andi', pencil, 1)
