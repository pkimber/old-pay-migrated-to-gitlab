# -*- encoding: utf-8 -*-
import pytest

from pay.tests.helper import check_payment

from example_pay.tests.factories import SalesLedgerFactory


@pytest.mark.django_db
def test_link_to_payment():
    sales_ledger = SalesLedgerFactory()
    check_payment(sales_ledger)
