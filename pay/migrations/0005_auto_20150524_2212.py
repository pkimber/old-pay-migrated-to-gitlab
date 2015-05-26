# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        ('pay', '0004_auto_20150511_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLine',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('line_number', models.IntegerField()),
                ('quantity', models.DecimalField(max_digits=6, decimal_places=2)),
                ('units', models.CharField(max_length=5)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('net', models.DecimalField(max_digits=8, decimal_places=2)),
                ('vat_rate', models.DecimalField(max_digits=5, decimal_places=3)),
                ('vat', models.DecimalField(max_digits=8, decimal_places=2)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Payment lines',
                'ordering': ['line_number'],
                'verbose_name': 'Payment line',
            },
        ),
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
        migrations.AddField(
            model_name='paymentline',
            name='payment',
            field=models.ForeignKey(to='pay.Payment'),
        ),
        migrations.AddField(
            model_name='paymentline',
            name='product',
            field=models.ForeignKey(to='stock.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='paymentline',
            unique_together=set([('payment', 'line_number')]),
        ),
    ]
