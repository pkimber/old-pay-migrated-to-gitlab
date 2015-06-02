# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pay', '0006_auto_20150528_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Payment plan run',
                'verbose_name': 'Payment plan run',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Payment plan headers',
                'verbose_name': 'Payment plan header',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('days_after', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('deleted', models.BooleanField(default=False)),
                ('payment_plan_header', models.ForeignKey(to='pay.PaymentPlanHeader')),
            ],
            options={
                'verbose_name_plural': 'Payment plan intervals',
                'verbose_name': 'Payment plan interval',
                'ordering': ('payment_plan_header__slug', 'days_after'),
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('payment_interval', models.ForeignKey(to='pay.PaymentPlanInterval')),
                ('payment_plan', models.ForeignKey(to='pay.PaymentPlan')),
            ],
            options={
                'verbose_name_plural': 'Payment plan item',
                'verbose_name': 'Payment plan item',
            },
        ),
        migrations.AddField(
            model_name='paymentplan',
            name='payment_plan_header',
            field=models.ForeignKey(to='pay.PaymentPlanHeader'),
        ),
        migrations.AlterUniqueTogether(
            name='paymentplanitem',
            unique_together=set([('payment_plan', 'payment_interval')]),
        ),
        migrations.AlterUniqueTogether(
            name='paymentplan',
            unique_together=set([('payment_plan_header', 'content_type', 'object_id')]),
        ),
    ]
