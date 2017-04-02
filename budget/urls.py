from django.conf.urls import url
# from django.views.generic import ListView

from .views import CategoryListView, TransactionListView, CurrentMonthAllListView, PreviousMonthAllListView


urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view()),
    url(r'^transactions/$', TransactionListView.as_view()),
    url(regex=r'^transactions/current_month_all$',
        view=CurrentMonthAllListView.as_view(),
        name='current-month-spending'),
    url(regex=r'^transactions/previous_month_all$',
        view=PreviousMonthAllListView.as_view(),
        name='previous-month-spending'),
]