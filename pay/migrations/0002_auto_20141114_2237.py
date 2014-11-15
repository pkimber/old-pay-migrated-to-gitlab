# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _init_state(model, name, slug):
    try:
        model.objects.get(slug=slug)
    except model.DoesNotExist:
        instance = model(**dict(name=name, slug=slug))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    """

    Create default states.

    We can't import a model directly as it may be a newer version than this
    migration expects.  We use the historical version.

    """

    PaymentState = apps.get_model('pay', 'PaymentState')
    _init_state(PaymentState, 'Due', 'due')
    _init_state(PaymentState, 'Fail', 'fail')
    _init_state(PaymentState, 'Later', 'later')
    _init_state(PaymentState, 'Paid', 'paid')


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
