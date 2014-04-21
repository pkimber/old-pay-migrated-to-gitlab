# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from base.tests.model_maker import clean_and_save

from pay.models import (
    Payment,
    PaymentState,
)
from pay.tests.model_maker import (
    make_payment,
    make_product,
)
from pay.tests.scenario import init_app_pay

from example.models import SalesLedger
from example.tests.model_maker import make_sales_ledger

class TestPayment(TestCase):

    def setUp(self):
        init_app_pay()
        self.pencil = make_product('Pencil', 'pencil', Decimal('1.32'))

    def _get_payment(self):
        return Payment.objects.get(email='test@pkimber.net')

    def _make_payment(self, line):
        return make_payment(
            'test@pkimber.net',
            self.pencil,
            'Colour pencils',
            1,
            Decimal('10.00'),
            line,
            '/url/after/',
        )

    def test_make_payment(self):
        line = make_sales_ledger('Carol')
        self._make_payment(line)

    def test_no_content_object(self):
        """Payments must be linked to a content object."""
        payment = Payment(**dict(
            product=self.pencil, quantity=Decimal(2), url='/after/')
        )
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            payment,
        )

    def test_set_paid(self):
        line = make_sales_ledger('Carol')
        self.assertFalse(line.is_paid)
        payment = self._make_payment(line)
        self.assertFalse(payment.is_paid())
        payment.set_paid()
        payment = self._get_payment()
        self.assertTrue(payment.is_paid())
        line = SalesLedger.objects.get(title='Carol')
        self.assertTrue(line.is_paid)

    def test_set_payment_failed(self):
        line = make_sales_ledger('Carol')
        self.assertFalse(line.is_paid)
        payment = self._make_payment(line)
        self.assertFalse(payment.is_paid())
        payment.set_payment_failed()
        payment = self._get_payment()
        self.assertFalse(payment.is_paid())
        line = SalesLedger.objects.get(title='Carol')
        self.assertFalse(line.is_paid)
        self.assertEqual(PaymentState.FAIL, payment.state.slug)

    def test_total(self):
        line = make_sales_ledger('Carol')
        payment = make_payment(
            'test@pkimber.net',
            self.pencil,
            'Colour pencils',
            2,
            Decimal('1.32'),
            line,
            '/url/after/'
        )
        self.assertEqual(Decimal('2.64'), payment.total)

    def test_unique_together(self):
        line = make_sales_ledger('Carol')
        self._make_payment(line)
        self.assertRaises(
            IntegrityError,
            self._make_payment,
            line,
        )
