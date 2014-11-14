# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pay.models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_auto_20141114_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='state',
            field=models.ForeignKey(default=pay.models._default_payment_state_pk, to='pay.PaymentState'),
            preserve_default=True,
        ),
    ]
