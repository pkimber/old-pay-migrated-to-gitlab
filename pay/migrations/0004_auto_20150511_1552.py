# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0003_auto_20141115_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='stripecustomer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
