# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from pay.models import Payment
from pay.service import init_app_pay
from pay.tests.helper import check_payment

from example.tests.scenario import default_scenario_pay


class TestSalesLedger(TestCase):

    def setUp(self):
        init_app_pay()
        default_scenario_pay()

    def test_link_to_payment(self):
        payment = Payment.objects.get(email='test@pkimber.net')
        check_payment(payment)