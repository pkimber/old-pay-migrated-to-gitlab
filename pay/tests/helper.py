# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


def check_payment(model_instance):
    """The 'Payment' model links to generic content.

    Check that the generic content can be paid.

    """
    model_instance.set_payment_failed()
    model_instance.set_paid()
