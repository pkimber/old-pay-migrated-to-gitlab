# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.scenario import (
    default_scenario_login,
    get_user_web,
)

from pay.models import Payment
from pay.service import init_app_pay
from pay.tests.model_maker import make_product
from pay.views import PAYMENT_PK

from example.tests.model_maker import make_sales_ledger
from example.tests.scenario import default_scenario_pay


class TestView(TestCase):
    """
    Session variables difficult to test ref:
    http://stackoverflow.com/questions/4453764/how-do-i-modify-the-session-in-the-django-test-framework
    """

    def setUp(self):
        init_app_pay()
        default_scenario_login()
        #default_scenario_pay()
        self.web = get_user_web()
        self.client.login(
            username=self.web.username,
            password=self.web.username
        )
        # create a payment
        pencil = make_product('Pencil', 'pencil', Decimal('1.32'))
        sales_ledger = make_sales_ledger(
            'test@pkimber.net', 'Joan', pencil, 2
        )
        self.payment = sales_ledger.create_payment()
        self.payment.save()
        self.payment.url = reverse(
            'example.payment', kwargs=dict(pk=self.payment.pk)
        )
        self.payment.url_failure = reverse(
            'example.payment', kwargs=dict(pk=self.payment.pk)
        )
        self.payment.save()

    def _set_session_payment_pk(self, pk):
        session = self.client.session
        session[PAYMENT_PK] = pk
        session.save()

    def test_pay_later(self):
        self._set_session_payment_pk(self.payment.pk)
        response = self.client.post(
            reverse('example.pay.later', kwargs=dict(pk=self.payment.pk))
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/example/payment/', response.url)

    def test_project_home(self):
        response = self.client.get(reverse('project.home'))
        self.assertEqual(response.status_code, 200)

    def test_stripe(self):
        #payment = Payment.objects.get(email='test@pkimber.net')
        self._set_session_payment_pk(self.payment.pk)
        response = self.client.get(
            reverse('example.pay.stripe', kwargs=dict(pk=self.payment.pk))
        )
        self.assertEqual(response.status_code, 200)
