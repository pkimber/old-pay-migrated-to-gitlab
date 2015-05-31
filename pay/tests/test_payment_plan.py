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
def test_payment_plan_get_absolute_url():
    obj = PaymentPlanFactory()
    obj.get_absolute_url()


@pytest.mark.django_db
def test_payment_plan_interval_get_absolute_url():
    obj = PaymentPlanIntervalFactory()
    obj.get_absolute_url()


@pytest.mark.django_db
def test_payment_plan_intervals():
    plan = PaymentPlanFactory()
    PaymentPlanIntervalFactory(plan=plan, days_after=3)
    PaymentPlanIntervalFactory(plan=plan, days_after=5, deleted=True)
    PaymentPlanIntervalFactory(plan=plan, days_after=7)
    assert [item.days_after for item in plan.intervals()]


@pytest.mark.django_db
def test_plan_str():
    str(PaymentPlanFactory())


@pytest.mark.django_db
def test_interval_str():
    str(PaymentPlanIntervalFactory())


#@pytest.mark.django_db
#def test_current():
#    PaymentPlanIntervalFactory(plan=PaymentPlanFactory(slug='c1'))
#    PaymentPlanIntervalFactory(
#        plan=PaymentPlanFactory(slug='c2'), deleted=True
#    )
#    PaymentPlanIntervalFactory(plan=PaymentPlanFactory(slug='c3'))
#    assert ['c1', 'c3'] == [
#        p.plan.slug for p in PaymentPlanInterval.objects.current()
#    ]
