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
    PaymentPlanAuditFactory,
    PaymentPlanHeaderFactory,
    PaymentPlanIntervalFactory,
)


@pytest.mark.django_db
def test_payment_plan_audit_str():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    payment_plan = PaymentPlanFactory(payment=payment)
    str(PaymentPlanAuditFactory(
        payment_plan=payment_plan,
        payment_interval=PaymentPlanIntervalFactory(),
    ))
