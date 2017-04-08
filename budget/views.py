import datetime

# from django.shortcuts import render
from django.views.generic import ListView

from . import models as mymodels
# from .models import Order


class CategoryListView(ListView):
    model = mymodels.Category


class TransactionListView(ListView):
    model = mymodels.Transaction
    # paginate_by = 10
    ordering = '-purchase_date'


class CurrentMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the current month """
        return mymodels.Transaction.objects.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        )

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        kwargs = super().get_context_data(**kwargs)
        kwargs['filter'] = 'current'
        return kwargs


class PreviousMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the previous month """
        return mymodels.Transaction.objects.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month - 1
        )

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        kwargs = super().get_context_data(**kwargs)
        catg = mymodels.Category.objects.all()
        kwargs['filter'] = 'previous'
        kwargs['categories'] = catg
        return kwargs
