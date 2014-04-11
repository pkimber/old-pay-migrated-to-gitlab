# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.scenario import (
    default_scenario_login,
    get_user_web,
)


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        self.web = get_user_web()
        self.client.login(
            username=self.web.username,
            password=self.web.username
        )

    def test_ask(self):
        response = self.client.get(reverse('pay.ask'))
        self.assertEqual(response.status_code, 200)
