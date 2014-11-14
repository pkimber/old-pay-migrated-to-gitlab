# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=75)),
                ('title', models.TextField()),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('url', models.CharField(help_text='redirect to this location after payment.', max_length=100)),
                ('url_failure', models.CharField(help_text='redirect to this location if the payment fails.', max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payment',
                'ordering': ('pk',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentState',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Payment state',
                'verbose_name_plural': 'Payment state',
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('customer_id', models.TextField()),
            ],
            options={
                'verbose_name': 'Stripe customer',
                'verbose_name_plural': 'Stripe customers',
                'ordering': ('pk',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='payment',
            name='state',
            field=models.ForeignKey(to='pay.PaymentState'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set([('object_id', 'content_type')]),
        ),
    ]
