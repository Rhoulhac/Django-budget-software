from django import forms

from .models import Transaction, SavingsTransaction


class SavingsTransactionForm(forms.ModelForm):

    class Meta:
        model = SavingsTransaction
        fields = ('saving', 'store', 'amount', 'transaction_date', 'payment_method', 'notes')
        widgets = {
            'saving': forms.Select(attrs={'class': 'form-control'}),
            'store': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_date': forms.TextInput(attrs={'class': 'form-control datepicker'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')


class CurrentMonthAll(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('store', 'amount', 'purchase_date', 'category', 'payment_method')
