# -*- encoding: utf-8 -*-
import pytest

from django.db.utils import IntegrityError

from example_pay.tests.factories import SalesLedgerFactory
from finance.tests.factories import VatSettingsFactory
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
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    str(PaymentPlanFactory(payment=payment))
