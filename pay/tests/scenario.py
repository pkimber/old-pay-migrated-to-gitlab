# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from pay.models import (
    PaymentState,
    STATE_DUE,
    STATE_FAIL,
    STATE_PAID,
)
from pay.tests.model_maker import make_payment_state


def _init_payment_state(name, slug):
    try:
        state = PaymentState.objects.get(slug=slug)
        state.name = name
        state.save()
    except PaymentState.DoesNotExist:
        make_payment_state(name, slug)
        #print('make_payment_state("{}")'.format(name))


def init_app_pay():
    _init_payment_state('Due', STATE_DUE)
    _init_payment_state('Fail', STATE_FAIL)
    _init_payment_state('Paid', STATE_PAID)
