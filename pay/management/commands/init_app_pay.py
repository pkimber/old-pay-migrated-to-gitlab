# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from pay.tests.scenario import init_app_pay


class Command(BaseCommand):

    help = "Initialise 'pay' application"

    def handle(self, *args, **options):
        init_app_pay()
        print("Initialised 'pay' app...")
