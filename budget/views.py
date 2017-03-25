# from django.shortcuts import render
from django.views.generic import ListView

from . import models as mymodels
# from .models import Order


class CategoryListView(ListView):
    model = mymodels.Category


class TransactionListView(ListView):
    model = mymodels.Transaction
    paginate_by = 10
    ordering = '-created_date'
    # ordering = '-modified_date'
