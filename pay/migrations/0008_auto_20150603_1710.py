# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _init_state(model, slug, name):
    try:
        model.objects.get(slug=slug)
    except model.DoesNotExist:
        instance = model(**dict(name=name, slug=slug))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    state = apps.get_model('pay', 'PaymentPlanStatus')
    _init_state(state, 'active', 'Active')
    _init_state(state, 'complete', 'Complete')
    _init_state(state, 'deleted', 'Deleted')
    state = apps.get_model('pay', 'PaymentPlanAuditStatus')
    _init_state(state, 'received', 'Received')
    _init_state(state, 'requested', 'Requested')


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0007_auto_20150603_1710'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
