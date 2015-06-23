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

    model = apps.get_model('pay', 'CheckoutState')
    _init_state(model, 'Due', 'due')
    _init_state(model, 'Fail', 'fail')
    _init_state(model, 'Success', 'success')


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0007_auto_20150623_0821'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
