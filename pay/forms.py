# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class StripeForm(forms.Form):

    stripeToken = forms.CharField()
