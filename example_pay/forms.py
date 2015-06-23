# -*- encoding: utf-8 -*-
from django import forms

from .models import (
    CardRefresh,
    SalesLedger,
)


class CardRefreshForm(forms.ModelForm):

    class Meta:
        model = CardRefresh
        fields = ()


class SalesLedgerForm(forms.ModelForm):

    class Meta:
        model = SalesLedger
        fields = ()
