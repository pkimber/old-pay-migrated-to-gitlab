# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import finance.models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20150526_1127'),
        ('stock', '0001_initial'),
        ('pay', '0003_auto_20141115_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('line_number', models.IntegerField()),
                ('quantity', models.DecimalField(max_digits=6, decimal_places=2)),
                ('units', models.CharField(max_length=5)),
                ('net', models.DecimalField(max_digits=8, decimal_places=2)),
                ('vat', models.DecimalField(max_digits=8, decimal_places=2)),
                ('save_price', models.DecimalField(default=Decimal('0'), max_digits=8, help_text='Price of the product when the line was saved.', decimal_places=2)),
                ('save_vat_rate', models.DecimalField(default=Decimal('0'), max_digits=5, help_text='VAT rate when the line was saved.', decimal_places=3)),
            ],
            options={
                'verbose_name': 'Payment line',
                'ordering': ['line_number'],
                'verbose_name_plural': 'Payment lines',
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
        migrations.AlterField(
            model_name='payment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='stripecustomer',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
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
        migrations.AddField(
            model_name='paymentline',
            name='vat_code',
            field=models.ForeignKey(default=finance.models.legacy_vat_code, to='finance.VatCode'),
        ),
        migrations.AlterUniqueTogether(
            name='paymentline',
            unique_together=set([('payment', 'line_number')]),
        ),
    ]
