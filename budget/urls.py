from django.conf.urls import url
from django.views.generic import ListView

from .views import CategoryListView, TransactionListView


urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view()),
    url(r'^transactions/$', TransactionListView.as_view()),
]