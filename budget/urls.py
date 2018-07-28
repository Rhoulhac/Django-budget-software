from django.urls import path

from .views import CategoryListView, TransactionListView, CurrentSavingsTransactionListView, \
    AllMonthlyTotalsView, savings_post


urlpatterns = [
    path('', AllMonthlyTotalsView.as_view(), name='all-monthly-totals'),
    path('categories/', CategoryListView.as_view()),
    path('transactions/', TransactionListView.as_view(), name='selected-month-spending'),
    path('savings/transactions', CurrentSavingsTransactionListView.as_view(), name='current-month-saving'),
    path('savings/transaction/new', savings_post, name='savings-new')
]
