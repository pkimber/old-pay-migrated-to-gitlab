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
        self.pen = make_product('Pen', 'pen', Decimal('2.00'))
        self.promotion.bundle.add(self.pen)
        self.pencil = make_product('Pencil', 'pencil', Decimal('1.32'))
        self.promotion.bundle.add(self.pencil)

    def test_bundle(self):
        self.assertEqual(2, self.promotion.bundle.count())
        products = self.pen.product_set.all()
        self.assertEqual(1, len(products))
        p = products[0]
        self.assertEqual('pen_promo', p.slug)

    def test_is_bundle(self):
        self.assertFalse(self.pen.is_bundle)
        self.assertFalse(self.pencil.is_bundle)
        self.assertTrue(self.promotion.is_bundle)

    def test_product_in_two_bundles(self):
        special_offer = make_product(
            'Pencils and more pencils', 'pencils_promo', Decimal('1.50')
        )
        pack_pencils = make_product(
            'Pack pencils', 'pack_pencil', Decimal('2.00'),
        )
        special_offer.bundle.add(pack_pencils)
        special_offer.bundle.add(self.pencil)
        self.assertEqual(2, special_offer.bundle.count())
        self.assertEqual(2, self.promotion.bundle.count())
        self.assertEqual(2, self.pencil.product_set.count())
        self.assertEqual(1, pack_pencils.product_set.count())
