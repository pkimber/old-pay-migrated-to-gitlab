# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
)

from base.view_utils import BaseMixin

from pay.models import Payment
from pay.views import (
    PAYMENT_PK,
    StripeFormViewMixin,
)

from .forms import ExampleCheckoutForm
from .models import SalesLedger


class ExampleCheckout(UpdateView):

    model = SalesLedger
    form_class = ExampleCheckoutForm

    def form_valid(self, form):
        super(ExampleCheckout, self).form_valid(form)
        payment = self.object.create_payment()
        payment.content_object = self.object
        payment.url = get_page_thankyou_membership().get_absolute_url()
        payment.url_failure = get_page_payment_sorry().get_absolute_url()
        payment.save()
        self.request.session[PAYMENT_PK] = payment.pk
        return HttpResponseRedirect(
            reverse('pay.stripe', kwargs=dict(pk=payment.pk))
        )

    def get_success_url(self):
        """called by 'form_valid' (above) but the result is not used."""
        return reverse('project.home')


class ExamplePaymentDetailView(DetailView):

    model = Payment


class HomeView(ListView):

    model = SalesLedger
    template_name = 'example/home.html'


class StripeUpdateView(StripeFormViewMixin, BaseMixin, UpdateView):

    template_name = 'pay/stripe.html'

    def get_success_url(self):
        return reverse('project.home')
