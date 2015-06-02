# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from .factories import (
    PaymentPlanFactory,
    PaymentPlanIntervalFactory,
)


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_pay_create(self):
        self.assert_staff_only(reverse('pay.plan.create'))

    def test_pay_delete(self):
        plan = PaymentPlanFactory()
        self.assert_staff_only(reverse('pay.plan.delete', args=[plan.pk]))

    def test_pay_detail(self):
        plan = PaymentPlanFactory()
        self.assert_staff_only(reverse('pay.plan.detail', args=[plan.pk]))

    def test_pay_list(self):
        self.assert_staff_only(reverse('pay.plan.list'))

    def test_pay_update(self):
        plan = PaymentPlanFactory()
        self.assert_staff_only(reverse('pay.plan.update', args=[plan.pk]))

    def test_pay_interval_create(self):
        plan = PaymentPlanFactory()
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
