# -*- encoding: utf-8 -*-
from decimal import Decimal

from mail.tests.model_maker import make_notify
from stock.models import (
    Product,
    ProductCategory,
    ProductType,
)

from example_pay.tests.model_maker import make_sales_ledger


def default_scenario_pay():
    make_notify('test@pkimber.net')
    stock = ProductType.objects.create_product_type(
        'stock', 'Stock'
    )
    stationery = ProductCategory.objects.create_product_category(
        'stationery', 'Stationery', stock
    )
    pencil = Product.objects.create_product(
        'pencil', 'Pencil', '', Decimal('1.32'), stationery
    )
    make_sales_ledger('test@pkimber.net', 'Carol', pencil, 2)
    make_sales_ledger('test@pkimber.net', 'Andi', pencil, 1)
