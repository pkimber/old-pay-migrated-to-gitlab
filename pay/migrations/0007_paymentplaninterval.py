# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        ('pay', '0006_auto_20150528_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPlanInterval',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('days_after', models.PositiveIntegerField()),
                ('deleted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='stock.ProductCategory')),
            ],
            options={
                'verbose_name_plural': 'Payment plan intervals',
                'ordering': ('category', 'days_after'),
                'verbose_name': 'Payment plan interval',
            },
        ),
    ]
