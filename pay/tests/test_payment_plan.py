# -*- encoding: utf-8 -*-
import pytest

from pay.models import (
    PaymentPlan,
    PaymentPlanInterval,
)
from stock.tests.factories import ProductCategoryFactory

from .factories import (
    PaymentPlanFactory,
    PaymentPlanIntervalFactory,
)


@pytest.mark.django_db
def test_plan_str():
    str(PaymentPlanFactory())


@pytest.mark.django_db
def test_interval_str():
    str(PaymentPlanIntervalFactory())


@pytest.mark.django_db
def test_current():
    PaymentPlanIntervalFactory(plan=PaymentPlanFactory(slug='c1'))
    PaymentPlanIntervalFactory(
        plan=PaymentPlanFactory(slug='c2'), deleted=True
    )
    PaymentPlanIntervalFactory(plan=PaymentPlanFactory(slug='c3'))
    assert ['c1', 'c3'] == [
        p.plan.slug for p in PaymentPlanInterval.objects.current()
    ]
