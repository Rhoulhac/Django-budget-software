from django.urls import path

from .views import CategoryListView, TransactionListView, CurrentMonthAllListView, \
    PreviousMonthAllListView, ThreePreviousMonthsAllListView, savings_post


urlpatterns = [
    path('', CurrentMonthAllListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('transactions/', TransactionListView.as_view()),
    path('transactions/current_month_all', CurrentMonthAllListView.as_view(), name='current-month-spending'),
    path('transactions/previous_month_all', PreviousMonthAllListView.as_view(), name='previous-month-spending'),
    path('transactions/three_previous_months', ThreePreviousMonthsAllListView.as_view(), name='three-previous-months-spending'),
    path('savings/transaction/new', savings_post, name='savings-new')
]