# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from example_pay.tests.scenario import default_scenario_pay


class Command(BaseCommand):

    help = "Create demo data for 'pay'"

    def handle(self, *args, **options):
        default_scenario_pay()
        print("Created 'pay' demo data...")
