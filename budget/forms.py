from django import forms

from .models import Transaction, SavingsTransaction


class SavingsTransactionForm(forms.ModelForm):

    class Meta:
        model = SavingsTransaction
        fields = ('saving', 'store', 'amount', 'transaction_date', 'payment_method', 'notes')


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')


class CurrentMonthAll(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')
