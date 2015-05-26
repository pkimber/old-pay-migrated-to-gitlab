# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import finance.models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20150526_0949'),
        ('pay', '0006_auto_20150524_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentline',
            name='description',
        ),
        migrations.RemoveField(
            model_name='paymentline',
            name='price',
        ),
        migrations.RemoveField(
            model_name='paymentline',
            name='vat_rate',
        ),
        migrations.AddField(
            model_name='paymentline',
            name='save_price',
            field=models.DecimalField(decimal_places=2, help_text='Price of the product when the line was saved.', max_digits=8, default=Decimal('0')),
        ),
        migrations.AddField(
            model_name='paymentline',
            name='save_vat_rate',
            field=models.DecimalField(decimal_places=3, help_text='VAT rate when the line was saved.', max_digits=5, default=Decimal('0')),
        ),
        migrations.AddField(
            model_name='paymentline',
            name='vat_code',
            field=models.ForeignKey(to='finance.VatCode', default=finance.models.legacy_vat_code),
        ),
    ]
