# -*- encoding: utf-8 -*-
from decimal import Decimal

from mail.tests.model_maker import make_notify
from stock.service import (
    init_product,
    init_product_category,
    init_product_type,
)

from example.tests.model_maker import make_sales_ledger


def default_scenario_pay():
    make_notify('test@pkimber.net')
    stock = init_product_type('Stock', 'stock')
    stationery = init_product_category('Stationery', 'stationery', stock)
    pencil = init_product('Pencil', 'pencil', Decimal('1.32'), stationery)
    make_sales_ledger('test@pkimber.net', 'Carol', pencil, 2)
    make_sales_ledger('test@pkimber.net', 'Andi', pencil, 1)
