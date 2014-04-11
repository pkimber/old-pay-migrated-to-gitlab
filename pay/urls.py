# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    include,
    patterns,
    url,
)

from .views import (
    PayPalFormView,
    StripeFormView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^paypal/$',
        view=PayPalFormView.as_view(),
        name='paypal.form'
        ),
    url(regex=r'^stripe/$',
        view=StripeFormView.as_view(),
        name='stripe.form'
        ),
    url(regex=r'^paypal/',
        view=include('paypal.standard.ipn.urls'),
        ),
)
