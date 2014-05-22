# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from mail.service import init_mail_template
from pay.models import (
    PaymentState,
    Product,
)
from pay.tests.model_maker import (
    make_payment_state,
    make_product,
)


# slug for the email template
PAYMENT_LATER = 'payment_later'
PAYMENT_THANKYOU = 'payment_thankyou'


def _init_payment_state(name, slug):
    try:
        state = PaymentState.objects.get(slug=slug)
        state.name = name
        state.save()
    except PaymentState.DoesNotExist:
        make_payment_state(name, slug)
        #print('make_payment_state("{}")'.format(name))


def init_app_pay():
    _init_payment_state('Due', PaymentState.DUE)
    _init_payment_state('Fail', PaymentState.FAIL)
    _init_payment_state('Later', PaymentState.LATER)
    _init_payment_state('Paid', PaymentState.PAID)
    # for the description, check 'mail_template_context' in 'pay.models'
    init_mail_template(
        PAYMENT_LATER,
        'Thank you for your application',
        (
            "We will contact you to arrange payment.\n\n"
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ description }} transaction detail.\n"
            "{{ total }} total value of the transaction."
        )
    )
    init_mail_template(
        PAYMENT_THANKYOU,
        'Thank you for your payment',
        (
            "You can add the following variables to the template:\n"
            "{{ name }} name of the customer.\n"
            "{{ description }} transaction detail.\n"
            "{{ total }} total value of the transaction."
        )
    )


def init_product(title, slug, description, price):
    """Create a new product - if it doesn't exist."""
    slug = slugify(slug)
    try:
        result = Product.objects.get(slug=slug)
        # If the product exists - don't update it!!!
        # The user might have set a new price or description!!
    except Product.DoesNotExist:
        if not description:
            description = ''
        result = make_product(title, slug, price, description=description)
        #print('make_product("{}")'.format(title))
    return result
