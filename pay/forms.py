# -*- encoding: utf-8 -*-
from django import forms

from .models import (
    Payment,
    PaymentPlan,
    PaymentPlanInterval,
)


class PayLaterForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ()


class PaymentPlanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'pure-input-1-2', 'rows': 4}
        )

    class Meta:
        model = PaymentPlan
        fields = (
            'slug',
            'name',
        )


class PaymentPlanIntervalForm(forms.ModelForm):

    class Meta:
        model = PaymentPlanInterval
        fields = (
            'days_after',
            'value',
        )


class StripeForm(forms.ModelForm):

    stripeToken = forms.CharField()

    class Meta:
        model = Payment
        fields = ()
