# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from example.tests.model_maker import make_sales_ledger

from pay.models import Payment
from pay.tests.model_maker import (
    make_payment,
    make_product,
)
from pay.tests.scenario import init_app_pay


class TestPayment(TestCase):

    def setUp(self):
        init_app_pay()
        self.pencil = make_product('Pencil', 'pencil', Decimal('1.32'))

    def _make_payment(self):
        line = make_sales_ledger('Carol')
        return make_payment(
            'test@pkimber.net',
            self.pencil,
            'Colour pencils',
            1,
            Decimal('10.00'),
            line
        )

    def test_make_payment(self):
        self._make_payment()

    def test_no_content_object(self):
        """Payments must be linked to a content object."""
        payment = Payment(**dict(product=self.pencil, quantity=Decimal(2)))
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            payment,
        )

    def test_total(self):
        line = make_sales_ledger('Carol')
        payment = make_payment(
            'test@pkimber.net',
            self.pencil,
            'Colour pencils',
            2,
            Decimal('1.32'),
            line
        )
        self.assertEqual(Decimal('2.64'), payment.total)

    def test_unique_together(self):
        line = make_sales_ledger('Carol')
        self._make_payment()
