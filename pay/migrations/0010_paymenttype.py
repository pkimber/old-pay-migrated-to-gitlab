# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0009_auto_20150603_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('amount', models.BooleanField(help_text="Display 'amount' when collecting payment")),
            ],
            options={
                'verbose_name_plural': 'Payment type',
                'verbose_name': 'Payment type',
                'ordering': ('name',),
            },
        ),
    ]
