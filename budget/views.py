import datetime
import re

from django.views.generic import ListView
from django.db.models import Sum

from . import models as mymodels


class CategoryListView(ListView):
    model = mymodels.Category


class TransactionListView(ListView):
    model = mymodels.Transaction
    ordering = '-purchase_date'

    def get_queryset(self):
        queryset = mymodels.Transaction.objects.all()

        if self.request.GET.get('filter'):
            selection = self.request.GET.get('filter')
            if selection == 'All':
                return queryset
            else:
                return queryset.filter(category__name=selection)
        else:
            return queryset


class CurrentMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the current month """
        queryset = super(CurrentMonthAllListView, self).get_queryset().filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month)
        return queryset

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        context = super().get_context_data(**kwargs)

        # Get current month Category amounts
        current_month_trans = mymodels.Transaction.objects\
            .filter(purchase_date__month=datetime.datetime.now().month)\
            .filter(purchase_date__year=datetime.datetime.now().year)
        cat_spending = {}
        cats = mymodels.Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=current_month_trans)

        if self.request.GET.get('filter'):
            # Selected filter value
            q = self.request.GET.get('filter')
            context['input'] = q

            # Queryset for graph
            cat_set = current_month_trans.filter(category__name=q).values('store__name') \
                .order_by('store__name').distinct().annotate(Sum('amount'))
            context['filter_graph_set'] = cat_set

        context['filter'] = 'current'
        context['categories'] = cat_spending

        return context


class PreviousMonthAllListView(TransactionListView):

    def get_queryset(self):
        """ Show only Transactions for the previous month """
        queryset = super(PreviousMonthAllListView, self).get_queryset().filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month - 1)

        return queryset

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        context = super().get_context_data(**kwargs)

        # Get previous month Category amounts
        previous_month_trans = mymodels.Transaction.objects \
            .filter(purchase_date__month=datetime.datetime.now().month - 1) \
            .filter(purchase_date__year=datetime.datetime.now().year)
        cat_spending = {}
        cats = mymodels.Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=previous_month_trans)

        if self.request.GET.get('filter'):
            # Selected filter value
            q = self.request.GET.get('filter')
            context['input'] = q

            # Queryset for graph
            cat_set = previous_month_trans.filter(category__name=q).values('store__name') \
                .order_by('store__name').distinct().annotate(Sum('amount'))
            context['filter_graph_set'] = cat_set

        context['filter'] = 'previous'
        context['categories'] = cat_spending

        return context


class ThreePreviousMonthsAllListView(TransactionListView):

    def get_queryset(self):
        """ Show Transactions for the previous 3 months """
        queryset = super(ThreePreviousMonthsAllListView, self).get_queryset().filter(
            purchase_date__month__gt=datetime.datetime.now().month - 3)

        return queryset

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        context = super().get_context_data(**kwargs)
        # Filter value
        q = self.request.GET.get('filter')
        context['input'] = q

        # Get last three months Category amounts
        three_month_trans = mymodels.Transaction.objects \
            .filter(purchase_date__month__gt=datetime.datetime.now().month - 3)
        cat_spending = {}
        cats = mymodels.Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=three_month_trans)

        context['filter'] = 'pastthree'
        context['categories'] = cat_spending

        return context


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
