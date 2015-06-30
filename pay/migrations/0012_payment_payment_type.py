# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pay.models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0011_auto_20150619_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(to='pay.PaymentType', default=pay.models.default_payment_type),
        ),
    ]
