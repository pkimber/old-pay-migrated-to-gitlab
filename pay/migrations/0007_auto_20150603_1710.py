# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0006_auto_20150528_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('payment', models.OneToOneField(help_text='The plan is initiated with a payment', to='pay.Payment')),
            ],
            options={
                'verbose_name_plural': 'Payment plans',
                'verbose_name': 'Payment plan',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Payment plan audit',
                'verbose_name': 'Payment plan audit',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanAuditStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Payment plans audit status',
                'verbose_name': 'Payment plan audit status',
            },
        ),
        migrations.CreateModel(
            name='PaymentPlanHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            name='PaymentPlanStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Payment plans status',
                'verbose_name': 'Payment plan status',
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
            unique_together=set([('payment', 'payment_plan_header')]),
        ),
    ]
