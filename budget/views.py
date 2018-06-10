import datetime
import re

from django.views.generic import ListView
from django.db.models import Sum
from django.shortcuts import render, redirect

from .models import Category, Transaction, SavingsTransaction, Savings
from .forms import SavingsTransactionForm


class CategoryListView(ListView):
    model = Category


class TransactionListView(ListView):
    model = Transaction
    ordering = '-purchase_date'

    def get_queryset(self):
        queryset = Transaction.objects.all()

        if self.request.GET.get('transactionMonth'):
            month_year = self.request.GET.get('transactionMonth').split('/')
            queryset = queryset.filter(purchase_date__month=month_year[0]).filter(purchase_date__year=month_year[1])

        if self.request.GET.get('filter'):
            selection = self.request.GET.get('filter')
            if selection == 'All':
                return queryset
            else:
                return queryset.filter(category__name=selection)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('transactionMonth'):
            # Get selected month transactions
            month_year = self.request.GET.get('transactionMonth')
            context['monthYear'] = month_year
            month_year_split = month_year.split('/')
            monthly_transactions = Transaction.objects \
                .filter(purchase_date__month=month_year_split[0]) \
                .filter(purchase_date__year=month_year_split[1])

        else:
            # Get current month transactions
            monthly_transactions = Transaction.objects\
                .filter(purchase_date__month=datetime.datetime.now().month)\
                .filter(purchase_date__year=datetime.datetime.now().year)

        cat_spending = {}
        cats = Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=monthly_transactions)

        if self.request.GET.get('filter'):
            # Selected category filter value
            q = self.request.GET.get('filter')
            context['category'] = q

            # Queryset for graph
            cat_set = monthly_transactions.filter(category__name=q).values('store__name') \
                .order_by('store__name').distinct().annotate(Sum('amount'))
            context['filter_graph_set'] = cat_set

        context['filter'] = 'current'
        context['categories'] = cat_spending

        return context


class CurrentSavingsTransactionListView(ListView):
    model = SavingsTransaction
    ordering = '-transaction_date'

    def get_queryset(self):
        """ Show all SavingsTransactions """
        queryset = SavingsTransaction.objects.all()

        if self.request.GET.get('filter'):
            selection = self.request.GET.get('filter')
            if selection == 'All':
                return queryset
            else:
                return queryset.filter(saving__name=selection)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        """ Transform queryset """
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('filter'):
            # Selected filter value
            q = self.request.GET.get('filter')
            context['input'] = q

        context['filter'] = 'current'
        context['savings'] = Savings.objects.all()

        return context


def spending(category, trans):

    budget_amount = int(Category.objects.get(name=category).budget_amount)
    spent = re.findall("\d+\.\d+", str(trans
                                       .filter(category__in=Category.objects.filter(name=category))
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


def savings_post(request):
    if request.method == "POST":
        form = SavingsTransactionForm(request.POST)

        if form.is_valid():
            form_update = form.save(commit=False)
            form_update.amount = form_update.amount * -1
            form_update.save()

            return redirect('savings-new')
    else:
        form = SavingsTransactionForm()

    return render(request, 'budget/savings_transaction.html', {'form': form})
