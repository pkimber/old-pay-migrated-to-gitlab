# -*- encoding: utf-8 -*-
import pytest

from django.db.utils import IntegrityError

from example_pay.tests.factories import SalesLedgerFactory
from pay.models import (
    PaymentPlan,
    PaymentPlanInterval,
)
from stock.tests.factories import ProductCategoryFactory

from pay.tests.factories import (
    PaymentFactory,
    PaymentPlanFactory,
    PaymentPlanHeaderFactory,
    PaymentPlanIntervalFactory,
)


@pytest.mark.django_db
def test_payment_plan_str():
    content_object = SalesLedgerFactory()
    str(PaymentPlanFactory(content_object=content_object))
