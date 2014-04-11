# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    include,
    patterns,
    url,
)

from .views import AskForMoneyView


urlpatterns = patterns(
    '',
    url(regex=r'^ask/$',
        view=AskForMoneyView.as_view(),
        name='pay.ask'
        ),
    url(regex=r'^paypal/',
        view=include('paypal.standard.ipn.urls'),
        ),
)
