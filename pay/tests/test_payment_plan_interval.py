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
def test_payment_plan_interval_get_absolute_url():
    obj = PaymentPlanIntervalFactory()
    obj.get_absolute_url()


@pytest.mark.django_db
def test_payment_plan_interval_str():
    str(PaymentPlanIntervalFactory())


#@pytest.mark.django_db
#def test_current():
#    PaymentPlanIntervalFactory(plan=PaymentPlanHeaderFactory(slug='c1'))
#    PaymentPlanIntervalFactory(
#        plan=PaymentPlanHeaderFactory(slug='c2'), deleted=True
#    )
#    PaymentPlanIntervalFactory(plan=PaymentPlanHeaderFactory(slug='c3'))
#    assert ['c1', 'c3'] == [
#        p.plan.slug for p in PaymentPlanInterval.objects.current()
#    ]
