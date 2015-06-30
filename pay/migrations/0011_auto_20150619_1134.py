# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _init_state(model, slug, name, amount):
    try:
        instance = model.objects.get(slug=slug)
        instance.amount = amount
        instance.save()
    except model.DoesNotExist:
        instance = model(**dict(name=name, slug=slug, amount=amount))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    state = apps.get_model('pay', 'PaymentType')
    _init_state(state, 'payment', 'Pay', True)
    _init_state(state, 'payment-plan', 'Set-up Payment Plan', False)
    _init_state(state, 'refresh-card', 'Refresh Card', False)


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0010_paymenttype'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
