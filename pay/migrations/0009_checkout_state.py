# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pay.models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0008_auto_20150623_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='state',
            field=models.ForeignKey(to='pay.CheckoutState', default=pay.models.default_checkout_state),
        ),
    ]
