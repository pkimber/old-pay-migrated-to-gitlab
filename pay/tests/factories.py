# -*- encoding: utf-8 -*-
from decimal import Decimal

import factory

from finance.models import VatSettings
from pay.models import (
    Payment,
    PaymentLine,
    PaymentPlan,
    PaymentPlanInterval,
)
from stock.tests.factories import (
    ProductCategoryFactory,
    ProductFactory,
)


class PaymentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Payment

    @factory.sequence
    def email(n):
        return '{:02d}@pkimber.net'.format(n)

    @factory.sequence
    def name(n):
        return 'Mr {} Smith'.format(n)


class PaymentLineFactory(factory.django.DjangoModelFactory):
    """Create a payment line.

    To customise::

      payment = PaymentFactory(content_object=SalesLedgerFactory())
      product = ProductFactory(name='Paintbrush')
      PaymentLineFactory(payment=payment, product=product)

    """

    class Meta:
        model = PaymentLine

    payment = factory.SubFactory(PaymentFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = Decimal('1')

    @factory.lazy_attribute
    def vat_code(self):
        return VatSettings.objects.settings().standard_vat_code

    @factory.sequence
    def line_number(n):
        return n


class PaymentPlanFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PaymentPlan

    @factory.sequence
    def name(n):
        return 'plan_{:02d}'.format(n)


class PaymentPlanIntervalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PaymentPlanInterval

    days_after = 10
    #category = factory.SubFactory(ProductCategoryFactory)
    plan = factory.SubFactory(PaymentPlanFactory)
    value = Decimal('99')
