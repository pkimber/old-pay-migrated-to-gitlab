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
            name='Checkout',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Checkout',
                'verbose_name_plural': 'Checkouts',
            },
        ),
        migrations.RenameModel(
            old_name='PaymentState',
            new_name='CheckoutState',
        ),
        migrations.RenameModel(
            old_name='StripeCustomer',
            new_name='Customer',
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='state',
        ),
        migrations.AlterUniqueTogether(
            name='paymentline',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='paymentline',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='paymentline',
            name='product',
        ),
        migrations.RemoveField(
            model_name='paymentline',
            name='vat_code',
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': 'Customers', 'verbose_name': 'Customer', 'ordering': ('pk',)},
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PaymentLine',
        ),
        migrations.AddField(
            model_name='checkout',
            name='customer',
            field=models.ForeignKey(to='pay.Customer'),
        ),
    ]
