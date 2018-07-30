import re
import datetime

from django.views.generic import ListView, TemplateView
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
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
            monthly_transactions = Transaction.objects.all()

        cat_spending = {}
        cats = Category.objects.all()
        for c in cats:
            cat_spending[c.name] = spending(c.name, trans=monthly_transactions)

        if self.request.GET.get('filter'):
            # Selected category filter value
            q = self.request.GET.get('filter')
            category = cat_spending[q]
            category['name'] = q
            context['category'] = category

            # Queryset for graph
            cat_set = monthly_transactions.filter(category__name=q).values('store__name') \
                .order_by('store__name').distinct().annotate(Sum('amount'))
            context['filter_graph_set'] = cat_set

        context['categories'] = cat_spending
        context['background'] = get_colors('0.2')
        context['border'] = get_colors('1')

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


class AllMonthlyTotalsView(TemplateView):
    template_name = 'budget/allmonthlytotals_list.html'
    queryset = Transaction.objects \
        .annotate(month=ExtractMonth('purchase_date'), year=ExtractYear('purchase_date')) \
        .values('month', 'year') \
        .order_by('month', 'year') \
        .annotate(Sum('amount'))

    for month in queryset:
        month['month'] = [datetime.date(1900, month['month'], 1).strftime('%B'), month['month']]

    def get_context_data(self, **kwargs):
        context = ({
            'queryset': self.queryset,
        })
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

    if percent > 100:
        percent = 100

    if percent <= 50:
        color = 'progress-bar-success'
    elif percent <= 90:
        color = 'progress-bar-warning'
    else:
        color = 'progress-bar-danger'

    return {
        'spent': spent,
        'budg_amt': budget_amount,
        'perc': percent,
        'color': color
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


def get_colors(transparency):
    # 12 color options - should be enough
    return [
        f'rgba(127, 191, 63, {transparency})',
        f'rgba(255, 99, 132, {transparency})',
        f'rgba(54, 162, 235, {transparency})',
        f'rgba(255, 206, 86, {transparency})',
        f'rgba(140, 114, 127, {transparency})',
        f'rgba(191, 63, 191, {transparency})',
        f'rgba(153, 102, 255, {transparency})',
        f'rgba(75, 192, 192, {transparency})',
        f'rgba(191, 63, 63, {transparency})',
        f'rgba(227, 225, 93, {transparency})',
        f'rgba(63, 191, 191, {transparency})',
        f'rgba(191, 127, 63, {transparency})',
    ]
