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
    make_payment(
        'test@pkimber.net',
        pencil,
        'Colour pencils',
        1,
        Decimal('10.00'),
        make_sales_ledger('Carol'),
        '/url/after/',
    )
    make_payment(
        'a@pkimber.net',
        pencil,
        'Pencils',
        2,
        Decimal('2.50'),
        make_sales_ledger('Andi'),
        '/url/after/',
    )
