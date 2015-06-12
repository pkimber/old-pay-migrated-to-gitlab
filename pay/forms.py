# -*- encoding: utf-8 -*-
from django import forms

from .models import Payment


class PayLaterForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ()


class StripeForm(forms.ModelForm):

    stripeToken = forms.CharField()

    class Meta:
        model = Payment
        fields = ()
