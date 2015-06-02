# -*- encoding: utf-8 -*-
import pytest

from django.db.utils import IntegrityError

from pay.models import (
    PaymentPlan,
    PaymentPlanInterval,
)
from stock.tests.factories import ProductCategoryFactory

from .factories import (
    PaymentPlanHeaderFactory,
    PaymentPlanIntervalFactory,
)


@pytest.mark.django_db
def test_payment_plan_header_get_absolute_url():
    obj = PaymentPlanHeaderFactory()
    obj.get_absolute_url()


@pytest.mark.django_db
def test_payment_plan_header_intervals():
    plan = PaymentPlanHeaderFactory()
    PaymentPlanIntervalFactory(payment_plan_header=plan, days_after=3)
    PaymentPlanIntervalFactory(payment_plan_header=plan, days_after=5, deleted=True)
    PaymentPlanIntervalFactory(payment_plan_header=plan, days_after=7)
    assert [item.days_after for item in plan.intervals()]


@pytest.mark.django_db
def test_payment_plan_header_slug_unique():
    PaymentPlanHeaderFactory(slug='one')
    with pytest.raises(IntegrityError) as excinfo:
        PaymentPlanHeaderFactory(slug='one')
    assert 'UNIQUE constraint failed' in str(excinfo.value)


@pytest.mark.django_db
def test_payment_plan_header_str():
    str(PaymentPlanHeaderFactory())
