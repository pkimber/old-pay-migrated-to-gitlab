# -*- encoding: utf-8 -*-
from django.test import TestCase

from example_pay.management.commands import demo_data_pay

from pay.management.commands import init_app_pay


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        pre_command = init_app_pay.Command()
        pre_command.handle()
        command = demo_data_pay.Command()
        command.handle()
