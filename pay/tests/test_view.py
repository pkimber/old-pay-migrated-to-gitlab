# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.scenario import (
    default_scenario_login,
    get_user_web,
)

from pay.tests.scenario import init_app_pay


class TestView(TestCase):

    pass

    #def test_paypal(self):
    #    response = self.client.get(reverse('pay.paypal'))
    #    self.assertEqual(response.status_code, 200)

