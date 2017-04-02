from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')


class CurrentMonthAll(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')
