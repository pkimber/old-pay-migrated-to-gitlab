# -*- encoding: utf-8 -*-
from django.test import TestCase

from pay.management.commands import init_app_pay


class TestCommand(TestCase):

    def test_init_app(self):
        """ Test the management command """
        command = init_app_pay.Command()
        command.handle()
