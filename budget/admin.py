from django.contrib import admin
from .models import Store, Transaction, Category, Savings, PaymentMethod

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Savings)
admin.site.register(PaymentMethod)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('purchase_date', 'amount', 'store', 'category', 'payment_method')


admin.site.register(Transaction, TransactionAdmin)
