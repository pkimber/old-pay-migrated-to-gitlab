# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from pay.models import STATE_DUE
from pay.tests.model_maker import make_payment_state


def default_scenario_pay():
    pass


def init_pay():
    make_payment_state('Due', STATE_DUE)
