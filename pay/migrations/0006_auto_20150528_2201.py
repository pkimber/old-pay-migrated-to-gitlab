# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0005_auto_20150528_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='price',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='title',
        ),
    ]
