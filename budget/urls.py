from django.conf.urls import url

from .views import CategoryListView, TransactionListView, CurrentMonthAllListView, \
    PreviousMonthAllListView, ThreePreviousMonthsAllListView


urlpatterns = [
    url(r'', TransactionListView.as_view()),
    url(r'^categories/$', CategoryListView.as_view()),
    url(r'^transactions/$', TransactionListView.as_view()),
    url(
        regex=r'^transactions/current_month_all$',
        view=CurrentMonthAllListView.as_view(),
        name='current-month-spending'
    ),
    url(
        regex=r'^transactions/previous_month_all$',
        view=PreviousMonthAllListView.as_view(),
        name='previous-month-spending'
    ),
    url(
        regex=r'^transactions/three_previous_months$',
        view=ThreePreviousMonthsAllListView.as_view(),
        name='three-previous-months-spending'
    ),
]