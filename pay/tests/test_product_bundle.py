# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from pay.tests.model_maker import (
    make_product,
    make_product_bundle,
    make_product_category,
    make_product_type,
)


class TestProductBundle(TestCase):

    def setUp(self):
        stock = make_product_type('Stock', 'stock')
        stationery = make_product_category('Stationery', 'stationery', stock)
        # products
        self.pack_pencils = make_product(
            'Pack pencils',
            'pack_pencil',
            Decimal('2.00'),
            stationery,
        )
        self.pen = make_product(
            'Pen',
            'pen',
            Decimal('2.00'),
            stationery,
        )
        self.pencil = make_product(
            'Pencil',
            'pencil',
            Decimal('1.32'),
            stationery,
        )
        # two available bundles when a person buys a pencil
        self.promotion = make_product_bundle(
            'Pens and Pencils',
            'pen_promo',
            self.pencil,
            Decimal('2.50'),
        )
        self.special_offer = make_product_bundle(
            'Pencils and more pencils',
            'pencils_promo',
            self.pencil,
            Decimal('1.50'),
        )
        # add products to the 'promotion' bundle
        self.promotion.bundle.add(self.pen)
        self.promotion.bundle.add(self.pencil)
        # add products to the 'special_offer' bundle
        self.special_offer.bundle.add(self.pack_pencils)
        self.special_offer.bundle.add(self.pencil)

    def test_bundle(self):
        self.assertEqual(2, self.promotion.bundle.count())
        slugs = [p.slug for p in self.promotion.bundle.all()]
        self.assertListEqual(['pen', 'pencil'], slugs)

    #def test_is_bundle(self):
    #    self.assertFalse(self.pen.is_bundle)
    #    self.assertFalse(self.pencil.is_bundle)
    #    self.assertTrue(self.promotion.is_bundle)

    def test_product_in_two_bundles(self):
        # check bundle counts
        self.assertEqual(2, self.special_offer.bundle.count())
        self.assertEqual(2, self.promotion.bundle.count())
        # check product set counts
        slugs = [p.slug for p in self.pencil.bundles.all()]
        self.assertListEqual(['pencils_promo', 'pen_promo'], slugs)
        slugs = [p.slug for p in self.pack_pencils.bundles.all()]
        self.assertListEqual(['pencils_promo',], slugs)
        #self.assertEqual(2, self.pencil.product_set.count())
        #self.assertEqual(1, self.pack_pencils.product_set.count())

    #def test_bundle_lookup(self):
    #    # which bundles (promotions) is the 'pencil' in?
    #    bundles = self.pencil.product_set.all()
    #    slugs = [p.slug for p in bundles]
    #    self.assertListEqual(['pen_promo', 'pencils_promo'], slugs)
