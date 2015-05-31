# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0006_auto_20150528_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Payment plan',
                'verbose_name': 'Payment plan',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanInterval',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('days_after', models.PositiveIntegerField()),
                ('value', models.DecimalField(max_digits=8, decimal_places=2)),
                ('deleted', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(to='pay.PaymentPlan')),
            ],
            options={
                'verbose_name_plural': 'Payment plan intervals',
                'verbose_name': 'Payment plan interval',
                'ordering': ('plan__slug', 'days_after'),
            },
        ),
    ]
