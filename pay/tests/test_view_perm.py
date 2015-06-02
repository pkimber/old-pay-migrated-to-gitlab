# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from .factories import (
    PaymentPlanHeaderFactory,
    PaymentPlanIntervalFactory,
)


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_payment_plan_header_create(self):
        self.assert_staff_only(reverse('pay.plan.header.create'))

    def test_payment_plan_header_delete(self):
        plan = PaymentPlanHeaderFactory()
        self.assert_staff_only(reverse('pay.plan.header.delete', args=[plan.pk]))

    def test_payment_plan_header_detail(self):
        plan = PaymentPlanHeaderFactory()
        self.assert_staff_only(reverse('pay.plan.header.detail', args=[plan.pk]))

    def test_payment_plan_header_list(self):
        self.assert_staff_only(reverse('pay.plan.header.list'))

    def test_payment_plan_header_update(self):
        plan = PaymentPlanHeaderFactory()
        self.assert_staff_only(reverse('pay.plan.header.update', args=[plan.pk]))

    def test_pay_interval_create(self):
        plan = PaymentPlanHeaderFactory()
        self.assert_staff_only(
            reverse('pay.plan.interval.create', args=[plan.pk])
        )

    def test_pay_interval_update(self):
        interval = PaymentPlanIntervalFactory()
        self.assert_staff_only(
            reverse('pay.plan.interval.update', args=[interval.pk])
        )

    def test_pay_interval_delete(self):
        interval = PaymentPlanIntervalFactory()
        self.assert_staff_only(
            reverse('pay.plan.interval.delete', args=[interval.pk])
        )
