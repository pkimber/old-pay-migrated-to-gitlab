# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

from finance.models import VatSettings
from stock.models import Product
from pay.models import (
    default_payment_state,
    Payment,
    PaymentLine,
    PaymentState,
    PaymentType,
)
from pay.service import (
    PAYMENT_CARD_REFRESH,
    PAYMENT_LATER,
    PAYMENT_THANKYOU,
)


class ExampleCardRefresh(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    payment_state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Example Card Refresh'
        verbose_name_plural = 'Example Card Refresh'

    def __str__(self):
        return '{}'.format(self.email)

    def allow_pay_later(self):
        return False

    def create_payment(self):
        """Example card refresh (payment type 'card_refresh')

        Note: Must be called from within a transaction.

        """
        return Payment.objects.create_payment(
            PaymentType.objects.refresh_card,
            self.name,
            self.email,
            self
        )

    def get_absolute_url(self):
        """just for testing."""
        return reverse('project.home')

    @property
    def mail_template_name(self):
        return PAYMENT_CARD_REFRESH

    def set_payment_state(self, payment_state):
        self.payment_state = payment_state
        self.save()


class SalesLedgerManager(models.Manager):

    def create_sales_ledger(self, email, title, product, quantity):
        obj = self.model(
            email=email,
            title=title,
            product=product,
            quantity=quantity,
        )
        obj.save()
        return obj


class SalesLedger(models.Model):
    """List of prices."""

    email = models.EmailField()
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    payment_state = models.ForeignKey(
        PaymentState,
        default=default_payment_state,
    )
    objects = SalesLedgerManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Sales ledger'
        verbose_name_plural = 'Sales ledger'

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        """just for testing."""
        return reverse('project.home')

    def allow_pay_later(self):
        return False

    def create_payment(self):
        """Example payment.

        Note: Must be called from within a transaction.

        """
        payment = Payment.objects.create_payment(
            PaymentType.objects.payment,
            self.title,
            self.email,
            self
        )
        vat_settings = VatSettings.objects.settings()
        PaymentLine.objects.create_payment_line(
            payment=payment,
            product=self.product,
            quantity=self.quantity,
            units='each',
            vat_code=vat_settings.standard_vat_code,
        )
        return payment

    @property
    def is_paid(self):
        paid = PaymentState.objects.get(slug=PaymentState.PAID)
        return self.payment_state == paid

    @property
    def can_pay(self):
        due = PaymentState.objects.get(slug=PaymentState.DUE)
        return self.payment_state == due

    @property
    def mail_template_name(self):
        """Which mail template to use.

        We don't allow pay later (see 'allow_pay_later' above).

        """
        return PAYMENT_THANKYOU

    def set_payment_state(self, payment_state):
        self.payment_state = payment_state
        self.save()
