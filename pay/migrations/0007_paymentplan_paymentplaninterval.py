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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Payment plan',
                'ordering': ('slug',),
                'verbose_name': 'Payment plan',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanInterval',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('days_after', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('deleted', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(to='pay.PaymentPlan')),
            ],
            options={
                'verbose_name_plural': 'Payment plan intervals',
                'ordering': ('plan__slug', 'days_after'),
                'verbose_name': 'Payment plan interval',
            },
        ),
    ]
