import datetime
import re

# from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Sum

from . import models as mymodels
# from .models import Order


class CategoryListView(ListView):
    model = mymodels.Category


class TransactionListView(ListView):
    model = mymodels.Transaction
    ordering = '-purchase_date'


class CurrentMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the current month """
        return mymodels.Transaction.objects.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        ).order_by('-purchase_date')

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        kwargs = super().get_context_data(**kwargs)

        # Get current month Category amounts
        current_month_trans = mymodels.Transaction.objects\
            .filter(purchase_date__month=datetime.datetime.now().month)\
            .filter(purchase_date__year=datetime.datetime.now().year)
        cat_spending = {}
        cats = mymodels.Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=current_month_trans)

        kwargs['filter'] = 'current'
        kwargs['categories'] = cat_spending
        kwargs['displayed_budgets'] = ['Groceries', 'Household', 'Dining', 'Gas (car)', 'Other']

        return kwargs


class PreviousMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the previous month """
        return mymodels.Transaction.objects.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month - 1
        ).order_by('-purchase_date')

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        kwargs = super().get_context_data(**kwargs)

        # Get previous month Category amounts
        previous_month_trans = mymodels.Transaction.objects \
            .filter(purchase_date__month=datetime.datetime.now().month - 1) \
            .filter(purchase_date__year=datetime.datetime.now().year)
        cat_spending = {}
        cats = mymodels.Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=previous_month_trans)

        kwargs['filter'] = 'previous'
        kwargs['categories'] = cat_spending
        kwargs['displayed_budgets'] = ['Groceries', 'Household', 'Dining', 'Gas (car)', 'Other']

        return kwargs


def spending(category, trans):

    budget_amount = int(mymodels.Category.objects.get(name=category).budget_amount)
    spent = re.findall("\d+\.\d+", str(trans
                                       .filter(category__in=mymodels.Category.objects.filter(name=category))
                                       .aggregate(Sum('amount'))))
    if spent:
        spent = float(spent.pop())
        percent = round(spent/budget_amount * 100, 0)
    else:
        spent = 0
        percent = 0

    return {
        'spent': spent,
        'budg_amt': budget_amount,
        'perc': percent
    }
