# -*- encoding: utf-8 -*-
from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from pay.models import (
    Payment,
    PaymentState,
)


def make_payment(
        name, email, title, quantity, price,
        content_object, url, url_failure, **kwargs):
    defaults = dict(
        name=name,
        email=email,
        title=title,
        quantity=quantity,
        price=price,
        content_object=content_object,
        url=url,
        url_failure=url_failure,
    )
    defaults.update(kwargs)
    return clean_and_save(Payment(**defaults))


def make_payment_state(name, slug, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(slug),
    )
    defaults.update(kwargs)
    return clean_and_save(PaymentState(**defaults))
