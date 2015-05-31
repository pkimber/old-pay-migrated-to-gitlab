# -*- encoding: utf-8 -*-
import pytest

from .factories import PaymentPlanIntervalFactory


@pytest.mark.django_db
def test_str():
    str(PaymentPlanIntervalFactory())
