# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from .factories import PaymentPlanFactory


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_pay_create(self):
        self.assert_staff_only(reverse('pay.plan.create'))

    def test_pay_detail(self):
        plan = PaymentPlanFactory()
        self.assert_staff_only(reverse('pay.plan.detail', args=[plan.pk]))

    def test_pay_list(self):
        self.assert_staff_only(reverse('pay.plan.list'))

    def test_pay_update(self):
        plan = PaymentPlanFactory()
        self.assert_staff_only(reverse('pay.plan.update', args=[plan.pk]))
