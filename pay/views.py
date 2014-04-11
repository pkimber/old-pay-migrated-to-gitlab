# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import FormView

from braces.views import LoginRequiredMixin
from paypal.standard.forms import PayPalPaymentsForm

from base.view_utils import BaseMixin

from .forms import StripeForm


class PayPalFormView(LoginRequiredMixin, BaseMixin, FormView):

    form_class = PayPalPaymentsForm
    template_name = 'pay/paypal.html'

    def get_initial(self):
        return dict(
            business=settings.PAYPAL_RECEIVER_EMAIL,
            amount='10.01',
            currency_code='GBP',
            item_name='Cycle Routes around Hatherleigh',
            invoice='0001',
            notify_url="https://www.example.com" + reverse('paypal-ipn'),
            return_url="https://www.example.com/your-return-location/",
            cancel_return="https://www.example.com/your-cancel-location/",
        )


class StripeFormView(LoginRequiredMixin, BaseMixin, FormView):

    form_class = StripeForm
    template_name = 'pay/stripe.html'

    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        context.update(dict(
            key=settings.STRIPE_PUBLISH_KEY,
        ))
        return context

    def form_valid(self, form):
        return super(StripeFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('project.home')
