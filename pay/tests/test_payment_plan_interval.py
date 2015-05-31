# -*- encoding: utf-8 -*-
import pytest

from pay.models import PaymentPlanInterval
from stock.tests.factories import ProductCategoryFactory
from .factories import PaymentPlanIntervalFactory


@pytest.mark.django_db
def test_str():
    str(PaymentPlanIntervalFactory())


@pytest.mark.django_db
def test_current():
    PaymentPlanIntervalFactory(
        category=ProductCategoryFactory(slug='c1')
    )
    PaymentPlanIntervalFactory(
        category=ProductCategoryFactory(slug='c2'),
        deleted=True,
    )
    PaymentPlanIntervalFactory(
        category=ProductCategoryFactory(slug='c3')
    )
    assert ['c1', 'c3'] == [
        p.category.slug for p in PaymentPlanInterval.objects.current()
    ]
