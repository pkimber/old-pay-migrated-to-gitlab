# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    PaymentAuditListView,
    PaymentListView,
    PaymentPlanCreateView,
    PaymentPlanDeleteView,
    PaymentPlanDetailView,
    PaymentPlanIntervalCreateView,
    PaymentPlanIntervalDeleteView,
    PaymentPlanIntervalUpdateView,
    PaymentPlanListView,
    PaymentPlanUpdateView,
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
    url(regex=r'^plan/$',
        view=PaymentPlanListView.as_view(),
        name='pay.plan.list'
        ),
    url(regex=r'^plan/create/$',
        view=PaymentPlanCreateView.as_view(),
        name='pay.plan.create'
        ),
    url(regex=r'^plan/(?P<pk>\d+)/$',
        view=PaymentPlanDetailView.as_view(),
        name='pay.plan.detail'
        ),
    url(regex=r'^plan/(?P<pk>\d+)/delete/$',
        view=PaymentPlanDeleteView.as_view(),
        name='pay.plan.delete'
        ),
    url(regex=r'^plan/(?P<pk>\d+)/update/$',
        view=PaymentPlanUpdateView.as_view(),
        name='pay.plan.update'
        ),
    url(regex=r'^plan/(?P<pk>\d+)/interval/create/$',
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
