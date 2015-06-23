# -*- encoding: utf-8 -*-
import pytest

from example_pay.tests.factories import SalesLedgerFactory
from finance.tests.factories import VatSettingsFactory
from pay.tests.helper import check_stripe_checkout


@pytest.mark.django_db
def test_link_to_payment():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    check_stripe_checkout(sales_ledger)
