# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from pay.tests.model_maker import (
    make_product,
    make_product_category,
    make_product_type,
)


class TestProduct(TestCase):

    def setUp(self):
        stock = make_product_type('Stock', 'stock')
        self.stationery = make_product_category(
            'Stationery', 'stationery', stock
        )

    def test_make(self):
        make_product('Pencil', 'pencil', Decimal('1.32'), self.stationery)

    def test_no_duplicate(self):
        make_product('Pencil', 'pencil', Decimal('1.32'), self.stationery)
        self.assertRaises(
            IntegrityError,
            make_product,
            'Pencil',
            'pencil',
            Decimal('1.00'),
            self.stationery,
        )
