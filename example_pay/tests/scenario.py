# -*- encoding: utf-8 -*-
from decimal import Decimal

from mail.tests.model_maker import make_notify
from stock.tests.model_maker import (
    make_product,
    make_product_category,
    make_product_type,
)

from example_pay.tests.model_maker import make_sales_ledger


def default_scenario_pay():
    make_notify('test@pkimber.net')
    stock = make_product_type('Stock', 'stock')
    stationery = make_product_category('Stationery', 'stationery', stock)
    pencil = make_product('Pencil', 'pencil', Decimal('1.32'), stationery)
    make_sales_ledger('test@pkimber.net', 'Carol', pencil, 2)
    make_sales_ledger('test@pkimber.net', 'Andi', pencil, 1)
