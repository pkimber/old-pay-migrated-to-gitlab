# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pay.models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0008_auto_20150603_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='status',
            field=models.ForeignKey(to='pay.PaymentPlanStatus', default=pay.models.default_payment_plan_status),
        ),
        migrations.AddField(
            model_name='paymentplanaudit',
            name='status',
            field=models.ForeignKey(to='pay.PaymentPlanAuditStatus', default=pay.models.default_payment_plan_audit_status),
        ),
    ]
