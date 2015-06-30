# -*- encoding: utf-8 -*-
import pytest

from pay.models import PaymentType


@pytest.mark.django_db
def test_payment_type_payment():
    assert True == PaymentType.objects.payment.amount


@pytest.mark.django_db
def test_payment_type_payment_plan():
    assert False == PaymentType.objects.payment_plan.amount


@pytest.mark.django_db
def test_payment_type_refresh_card():
    assert False == PaymentType.objects.refresh_card.amount
