# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from pay.service import init_app_pay


class Command(BaseCommand):

    help = "Initialise 'pay' application"

    def handle(self, *args, **options):
        init_app_pay()
        print("Initialised 'pay' app...")
