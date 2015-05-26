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
    state = apps.get_model('pay', 'PaymentState')
    _init_state(state, 'due', 'Due')
    _init_state(state, 'fail', 'Fail')
    _init_state(state, 'later', 'Later')
    _init_state(state, 'paid', 'Paid')


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0005_auto_20150524_2212'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]
