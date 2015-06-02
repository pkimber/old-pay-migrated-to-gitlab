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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Payment plan run',
                'verbose_name_plural': 'Payment plan run',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'verbose_name': 'Payment plan audit',
                'verbose_name_plural': 'Payment plan audit',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name': 'Payment plan header',
                'verbose_name_plural': 'Payment plan headers',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanInterval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('days_after', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('deleted', models.BooleanField(default=False)),
                ('payment_plan_header', models.ForeignKey(to='pay.PaymentPlanHeader')),
            ],
            options={
                'ordering': ('payment_plan_header__slug', 'days_after'),
                'verbose_name': 'Payment plan interval',
                'verbose_name_plural': 'Payment plan intervals',
            },
        ),
        migrations.AddField(
            model_name='paymentplanaudit',
            name='payment_interval',
            field=models.ForeignKey(to='pay.PaymentPlanInterval'),
        ),
        migrations.AddField(
            model_name='paymentplanaudit',
            name='payment_plan',
            field=models.ForeignKey(to='pay.PaymentPlan'),
        ),
        migrations.AddField(
            model_name='paymentplan',
            name='payment_plan_header',
            field=models.ForeignKey(to='pay.PaymentPlanHeader'),
        ),
        migrations.AlterUniqueTogether(
            name='paymentplanaudit',
            unique_together=set([('payment_plan', 'payment_interval')]),
        ),
        migrations.AlterUniqueTogether(
            name='paymentplan',
            unique_together=set([('payment_plan_header', 'content_type', 'object_id')]),
        ),
    ]
