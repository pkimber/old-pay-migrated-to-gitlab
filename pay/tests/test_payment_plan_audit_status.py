# -*- encoding: utf-8 -*-
import pytest

from pay.models import PaymentPlanAuditStatus


@pytest.mark.django_db
def test_payment_plan_audit_status():
    str(PaymentPlanAuditStatus.objects.first())
