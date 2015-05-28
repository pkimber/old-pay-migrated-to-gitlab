# -*- encoding: utf-8 -*-
import pytest

from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test.client import RequestFactory
from django.utils import timezone

from finance.tests.factories import VatSettingsFactory
from pay.models import (
    PayError,
    Payment,
    PaymentState,
)
from pay.tests.factories import (
    PaymentFactory,
    PaymentLineFactory,
)
from stock.tests.factories import ProductFactory

from example_pay.models import SalesLedger
from example_pay.tests.factories import SalesLedgerFactory


@pytest.mark.django_db
def test_check_can_pay():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    try:
        payment.check_can_pay
        pass
    except PayError:
        assert False, 'payment is due - so can be paid'


@pytest.mark.django_db
def test_check_can_pay_not():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    payment.set_paid()
    with pytest.raises(PayError):
        payment.check_can_pay


@pytest.mark.django_db
def test_check_can_pay_too_early():
    """This should never happen... but test anyway."""
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    payment.created = timezone.now() + relativedelta(hours=+1, minutes=+2)
    payment.save()
    with pytest.raises(PayError):
        payment.check_can_pay


@pytest.mark.django_db
def test_check_can_pay_too_late():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    payment = sales_ledger.create_payment()
    payment.created = timezone.now() + relativedelta(hours=-1, minutes=-3)
    payment.save()
    with pytest.raises(PayError):
        payment.check_can_pay


@pytest.mark.django_db
def test_mail_template_context():
    VatSettingsFactory()
    product = ProductFactory(name='Colour Pencils', price=Decimal('10.00'))
    sales_ledger = SalesLedgerFactory(
        email='test@pkimber.net',
        title='Mr Patrick Kimber',
        product=product,
    )
    payment = sales_ledger.create_payment()
    assert {
        'test@pkimber.net': dict(
            description='Colour Pencils (£10.00 + £2.00 vat)',
            name='Mr Patrick Kimber',
            total='£12.00',
        ),
    } == payment.mail_template_context()


@pytest.mark.django_db
def test_make_payment():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    sales_ledger.create_payment()


@pytest.mark.django_db
def test_no_content_object():
    """Payments must be linked to a content object."""
    VatSettingsFactory()
    with pytest.raises(IntegrityError):
        PaymentFactory()


@pytest.mark.django_db
def test_notification_message():
    VatSettingsFactory()
    payment = PaymentFactory(content_object=SalesLedgerFactory())
    product = ProductFactory(name='Paintbrush')
    PaymentLineFactory(payment=payment, product=product)
    payment.set_paid()
    factory = RequestFactory()
    request = factory.get(reverse('project.home'))
    subject, message = payment.mail_subject_and_message(request)
    assert 'payment received from Mr' in message
    assert 'Paintbrush' in message
    assert 'http://testserver/' in message


@pytest.mark.django_db
def test_set_paid():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory(title='Carol')
    assert not sales_ledger.is_paid
    payment = sales_ledger.create_payment()
    assert not payment.is_paid
    payment.set_paid()
    # refresh
    payment = Payment.objects.get(pk=payment.pk)
    assert payment.is_paid
    # refresh
    sales_ledger = SalesLedger.objects.get(title='Carol')
    assert sales_ledger.is_paid


@pytest.mark.django_db
def test_set_payment_failed():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory(title='Carol')
    assert not sales_ledger.is_paid
    payment = sales_ledger.create_payment()
    assert not payment.is_paid
    payment.set_payment_failed()
    # refresh
    payment = Payment.objects.get(pk=payment.pk)
    assert not payment.is_paid
    sales_ledger = SalesLedger.objects.get(title='Carol')
    assert not sales_ledger.is_paid
    assert PaymentState.FAIL == payment.state.slug


@pytest.mark.django_db
def test_total():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory(
        product=ProductFactory(price=Decimal('2.50')),
        quantity=Decimal('2'),
    )
    payment = sales_ledger.create_payment()
    assert Decimal('6.00') == payment.total


@pytest.mark.django_db
def test_unique_together():
    VatSettingsFactory()
    sales_ledger = SalesLedgerFactory()
    sales_ledger.create_payment()
    with pytest.raises(IntegrityError):
        sales_ledger.create_payment()
