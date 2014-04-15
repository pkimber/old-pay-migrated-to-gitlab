# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from example.tests.scenario import default_scenario_pay


class Command(BaseCommand):

    help = "Create demo data for 'pay'"

    def handle(self, *args, **options):
        default_scenario_pay()
        print("Created 'pay' demo data...")
