# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.scenario import (
    default_scenario_login,
    get_user_web,
)

from pay.models import Payment
from pay.service import init_app_pay
from pay.views import PAYMENT_PK

from example.tests.scenario import default_scenario_pay


class TestView(TestCase):

    def setUp(self):
        init_app_pay()
        default_scenario_login()
        default_scenario_pay()
        self.web = get_user_web()
        self.client.login(
            username=self.web.username,
            password=self.web.username
        )

    def test_project_home(self):
        response = self.client.get(reverse('project.home'))
        self.assertEqual(response.status_code, 200)

    def test_stripe(self):
        payment = Payment.objects.get(email='test@pkimber.net')
        # Session variables difficult to test ref:
        # http://stackoverflow.com/questions/4453764/how-do-i-modify-the-session-in-the-django-test-framework
        session = self.client.session
        session[PAYMENT_PK] = payment.pk
        session.save()
        response = self.client.get(
            reverse('pay.stripe', kwargs=dict(pk=payment.pk))
        )
        self.assertEqual(response.status_code, 200)
