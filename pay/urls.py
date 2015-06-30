# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    PaymentAuditListView,
    PaymentListView,
    PaymentPlanHeaderCreateView,
    PaymentPlanHeaderDeleteView,
    PaymentPlanHeaderDetailView,
    PaymentPlanHeaderListView,
    PaymentPlanHeaderUpdateView,
    PaymentPlanIntervalCreateView,
    PaymentPlanIntervalDeleteView,
    PaymentPlanIntervalUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=PaymentListView.as_view(),
        name='pay.list'
        ),
    url(regex=r'^audit/$',
        view=PaymentAuditListView.as_view(),
        name='pay.list.audit'
        ),
    url(regex=r'^plan/header/$',
        view=PaymentPlanHeaderListView.as_view(),
        name='pay.plan.header.list'
        ),
    url(regex=r'^plan/header/create/$',
        view=PaymentPlanHeaderCreateView.as_view(),
        name='pay.plan.header.create'
        ),
    url(regex=r'^plan/header/(?P<pk>\d+)/$',
        view=PaymentPlanHeaderDetailView.as_view(),
        name='pay.plan.header.detail'
        ),
    url(regex=r'^plan/header/(?P<pk>\d+)/delete/$',
        view=PaymentPlanHeaderDeleteView.as_view(),
        name='pay.plan.header.delete'
        ),
    url(regex=r'^plan/header/(?P<pk>\d+)/update/$',
        view=PaymentPlanHeaderUpdateView.as_view(),
        name='pay.plan.header.update'
        ),
    url(regex=r'^plan/header/(?P<pk>\d+)/interval/create/$',
        view=PaymentPlanIntervalCreateView.as_view(),
        name='pay.plan.interval.create'
        ),
    url(regex=r'^plan/interval/(?P<pk>\d+)/delete/$',
        view=PaymentPlanIntervalDeleteView.as_view(),
        name='pay.plan.interval.delete'
        ),
    url(regex=r'^plan/interval/(?P<pk>\d+)/update/$',
        view=PaymentPlanIntervalUpdateView.as_view(),
        name='pay.plan.interval.update'
        ),
)
