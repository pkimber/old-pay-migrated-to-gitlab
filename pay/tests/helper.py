# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from base.tests.model_maker import clean_and_save

from pay.models import PaymentState


def check_payment(model_instance):
    """The 'Payment' model links to generic content."""
    # can we create a payment instance (need to set url before save).
    payment = model_instance.create_payment()
    payment.url = reverse('project.home')
    payment.url_failure = reverse('project.home')
    clean_and_save(payment)
    # can the generic content be paid?
    paid = PaymentState.objects.get(slug=PaymentState.PAID)
    current = model_instance.payment_state
    model_instance.payment_state = paid
    # the generic content must implement 'get_absolute_url'
    model_instance.get_absolute_url()
    clean_and_save(model_instance)
