# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import PaymentListView


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=PaymentListView.as_view(),
        name='pay.list'
        ),
)
