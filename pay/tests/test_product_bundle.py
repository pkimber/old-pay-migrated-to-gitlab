# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from pay.tests.model_maker import make_product


class TestProductBundle(TestCase):

    def setUp(self):
        self.promotion = make_product(
            'Pens and Pencils', 'pen_promo', Decimal('2.50')
        )
        self.pen = make_product(
            'Pen', 'pen', Decimal('2.00'), bundle=self.promotion
        )
        self.pencil = make_product(
            'Pencil', 'pencil', Decimal('1.32'), bundle=self.promotion
        )

    def test_bundle(self):
        self.assertEqual(2, self.promotion.product_set.count())
        self.assertEqual('pen_promo', self.pen.bundle.slug)

    def test_is_bundle(self):
        self.assertFalse(self.pen.is_bundle)
        self.assertFalse(self.pencil.is_bundle)
        self.assertTrue(self.promotion.is_bundle)
