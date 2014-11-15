# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pay.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('pay', '0002_auto_20141114_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=75)),
                ('title', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('url', models.CharField(help_text='redirect to this location after payment.', max_length=100)),
                ('url_failure', models.CharField(help_text='redirect to this location if the payment fails.', max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('state', models.ForeignKey(to='pay.PaymentState', default=pay.models._default_payment_state_pk)),
            ],
            options={
                'verbose_name_plural': 'Payment',
                'ordering': ('pk',),
                'verbose_name': 'Payment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('customer_id', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Stripe customers',
                'ordering': ('pk',),
                'verbose_name': 'Stripe customer',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set([('object_id', 'content_type')]),
        ),
    ]
