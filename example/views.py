# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView,
    UpdateView,
)

from base.view_utils import BaseMixin

from pay.models import Payment
from pay.views import StripeFormMixin


class HomeView(ListView):

    model = Payment
    template_name = 'example/home.html'


class StripeUpdateView(StripeFormMixin, BaseMixin, UpdateView):

    template_name = 'pay/stripe.html'

    def get_success_url(self):
        return reverse('project.home')
