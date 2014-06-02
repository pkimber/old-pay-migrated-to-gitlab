# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from pay.models import (
    Payment,
    PaymentState,
    Product,
    ProductCategory,
    ProductType,
)


def make_payment(
        name, email, product, title, quantity, price,
        content_object, url, url_failure, **kwargs):
    defaults = dict(
        name=name,
        email=email,
        product=product,
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


def make_product(name, slug, price, category, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(slug),
        price=price,
        category=category,
    )
    defaults.update(kwargs)
    return clean_and_save(Product(**defaults))


def make_product_category(name, slug, product_type, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(slug),
        product_type=product_type,
    )
    defaults.update(kwargs)
    return clean_and_save(ProductCategory(**defaults))


def make_product_type(name, slug, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(slug),
    )
    defaults.update(kwargs)
    return clean_and_save(ProductType(**defaults))
