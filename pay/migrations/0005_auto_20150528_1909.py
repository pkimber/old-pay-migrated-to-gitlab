# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models, migrations


def _create_legacy_product(model, product_category):
    try:
        instance = model.objects.get(slug='legacy')
    except model.DoesNotExist:
        instance = model(**dict(
            category=product_category,
            description="Legacy product ('pay' conversion)",
            legacy=True,
            name='Legacy',
            price=Decimal(),
            slug='legacy',
        ))
        instance.save()
        instance.full_clean()
    return instance


def _create_legacy_product_category(model, product_type):
    try:
        instance = model.objects.get(slug='legacy')
    except model.DoesNotExist:
        instance = model(**dict(
            name='Legacy',
            product_type=product_type,
            slug='legacy',
        ))
        instance.save()
        instance.full_clean()
    return instance


def _create_legacy_product_type(model):
    try:
        instance = model.objects.get(slug='legacy')
    except model.DoesNotExist:
        instance = model(**dict(name='Legacy', slug='legacy'))
        instance.save()
        instance.full_clean()
    return instance


def _create_payment_line(model, payment, product, quantity, price, vat_code):
    try:
        model.objects.get(payment=payment)
    except model.DoesNotExist:
        instance = model(**dict(
            line_number=1,
            net=price,
            payment=payment,
            product=product,
            quantity=quantity,
            save_price=price,
            save_vat_rate=Decimal(),
            units='each',
            vat=Decimal(),
            vat_code=vat_code,
        ))
        instance.save()
        instance.full_clean()


def _get_vat_code(model):
    return model.objects.get(slug='L')


def create_payment_lines(apps, schema_editor):
    """Create payment lines from the payment model (before removing fields).

    To check in the shell::

      Payment.objects.count()
      PaymentLine.objects.count()
      for item in PaymentLine.objects.all(): print(item.net, item.quantity, item.payment.price, item.payment.quantity)

    We can't import models directly as it may be a newer # version than this
    migration expects.  We use the historical version.

    """
    payment_model = apps.get_model('pay', 'Payment')
    paymentline_model = apps.get_model('pay', 'PaymentLine')
    product_category_model = apps.get_model('stock', 'ProductCategory')
    product_model = apps.get_model('stock', 'Product')
    product_type_model = apps.get_model('stock', 'ProductType')
    vat_code_model = apps.get_model('finance', 'VatCode')
    # init
    product_type = _create_legacy_product_type(product_type_model)
    product_category = _create_legacy_product_category(
        product_category_model,
        product_type,
    )
    product = _create_legacy_product(product_model, product_category)
    vat_code = _get_vat_code(vat_code_model)
    # transfer
    for payment in payment_model.objects.all():
        _create_payment_line(
            paymentline_model,
            payment,
            product,
            payment.quantity,
            payment.price,
            vat_code,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0004_auto_20150528_1908'),
    ]

    operations = [
        migrations.RunPython(create_payment_lines),
    ]
