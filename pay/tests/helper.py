# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from pay.models import PaymentState


def check_payment(model_instance):
    """The 'Payment' model links to generic content.

    Check that the generic content can be paid.

    """
    paid = PaymentState.objects.get(slug=PaymentState.PAID)
    current = model_instance.payment_state
    model_instance.payment_state = paid
    model_instance.save()
