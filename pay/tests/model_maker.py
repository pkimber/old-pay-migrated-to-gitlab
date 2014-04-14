# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from pay.models import (
    Payment,
    PaymentState,
    Product,
)


def make_payment(product, quantity, content_object, **kwargs):
    defaults = dict(
        product=product,
        quantity=quantity,
        content_object=content_object,
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


def make_product(slug, title, price, **kwargs):
    defaults = dict(
        title=title,
        slug=slugify(slug),
        price=price,
    )
    defaults.update(kwargs)
    return clean_and_save(Product(**defaults))
