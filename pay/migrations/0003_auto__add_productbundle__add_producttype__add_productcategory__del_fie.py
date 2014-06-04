# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductBundle'
        db.create_table('pay_productbundle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pay.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('pay', ['ProductBundle'])

        # Adding M2M table for field bundle on 'ProductBundle'
        m2m_table_name = db.shorten_name('pay_productbundle_bundle')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productbundle', models.ForeignKey(orm['pay.productbundle'], null=False)),
            ('product', models.ForeignKey(orm['pay.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productbundle_id', 'product_id'])

        # Adding model 'ProductType'
        db.create_table('pay_producttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('pay', ['ProductType'])

        # Adding model 'ProductCategory'
        db.create_table('pay_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('product_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pay.ProductType'])),
        ))
        db.send_create_signal('pay', ['ProductCategory'])

        # we need a product type before we can create a product
        try:
            product_type = orm['pay.ProductType'].objects.get(pk=1)
        except ObjectDoesNotExist:
            product_type = orm['pay.ProductType'].objects.create(
                name='demo',
                slug='demo',
            )
        # we need a product category before we can add a category to the product table.
        try:
            product_category = orm['pay.ProductCategory'].objects.get(pk=1)
        except ObjectDoesNotExist:
            product_category = orm['pay.ProductCategory'].objects.create(
                name='demo',
                slug='demo',
                product_type=product_type,
            )

        # Deleting field 'Product.title'
        db.delete_column('pay_product', 'title')

        # Adding field 'Product.name'
        db.add_column('pay_product', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Product.category'.  The category is created by default (see above).
        db.add_column('pay_product', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['pay.ProductCategory']),
                      keep_default=False)

        # Adding field 'Product.legacy'
        db.add_column('pay_product', 'legacy',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProductBundle'
        db.delete_table('pay_productbundle')

        # Removing M2M table for field bundle on 'ProductBundle'
        db.delete_table(db.shorten_name('pay_productbundle_bundle'))

        # Deleting model 'ProductType'
        db.delete_table('pay_producttype')

        # Deleting model 'ProductCategory'
        db.delete_table('pay_productcategory')

        # Adding field 'Product.title'
        db.add_column('pay_product', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Product.name'
        db.delete_column('pay_product', 'name')

        # Deleting field 'Product.category'
        db.delete_column('pay_product', 'category_id')

        # Deleting field 'Product.legacy'
        db.delete_column('pay_product', 'legacy')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pay.payment': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'Payment', 'unique_together': "(('object_id', 'content_type'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pay.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pay.PaymentState']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url_failure': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pay.paymentstate': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PaymentState'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'pay.product': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pay.ProductCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'pay.productbundle': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductBundle'},
            'bundle': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'u+'", 'to': "orm['pay.Product']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pay.Product']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'pay.productcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'product_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pay.ProductType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'pay.producttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ProductType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'pay.stripecustomer': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'StripeCustomer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'customer_id': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['pay']
