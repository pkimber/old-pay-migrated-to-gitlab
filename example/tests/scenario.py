# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.scenario import (
    default_scenario_login,
    get_user_web,
)

from pay.tests.model_maker import (
    make_payment,
    make_product,
)
from pay.tests.scenario import init_app_pay

from example.tests.model_maker import make_sales_ledger


def default_scenario_pay():
    pencil = make_product('Pencil', 'pencil', Decimal('1.32'))
    payment = make_payment(
        'test@pkimber.net',
        pencil,
        'Colour pencils',
        1,
        Decimal('10.00'),
        make_sales_ledger('Carol'),
    )
    print('make_payment: {}'.format(payment.description))
    payment = make_payment(
        'a@pkimber.net',
        pencil,
        'Pencils',
        2,
        Decimal('2.50'),
        make_sales_ledger('Andi'),
    )
    print('make_payment: {}'.format(payment.description))
