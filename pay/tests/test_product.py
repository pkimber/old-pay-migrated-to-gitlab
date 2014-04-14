# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from pay.tests.model_maker import make_product


class TestProduct(TestCase):

    def test_make(self):
        make_product('Pencil', 'pencil', Decimal('1.32'))

    def test_no_duplicate(self):
        make_product('Pencil', 'pencil', Decimal('1.32'))
        self.assertRaises(
            IntegrityError,
            make_product,
            'Pencil',
            'pencil',
            Decimal('1.00'),
        )
