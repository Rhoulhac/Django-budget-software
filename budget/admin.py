from django.contrib import admin
from .models import Store, Transaction, Category, Savings, PaymentMethod

admin.site.register(Store)
admin.site.register(PaymentMethod)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget_amount')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('purchase_date_and_store', 'category', 'amount', 'payment_method')
    list_filter = ('category', 'store', 'payment_method')

    def purchase_date_and_store(self, obj):
        return f'{obj.purchase_date.strftime("%b %d")} - {obj.store}'
    purchase_date_and_store.short_description = 'Date and Store'


class SavingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budgeted_amount', 'amount_saved')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Savings, SavingsAdmin)
admin.site.register(Transaction, TransactionAdmin)
