from django.contrib import admin
from .models import Store, Transaction, Category, Savings

admin.site.register(Store)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Savings)
