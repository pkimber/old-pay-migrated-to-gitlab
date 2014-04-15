# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Payment


class StripeForm(forms.ModelForm):

    stripeToken = forms.CharField()

    class Meta:
        model = Payment
        fields = ()
