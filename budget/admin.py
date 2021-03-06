from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from .models import Store, Transaction, Category, Savings, PaymentMethod, SavingsTransaction


class MyDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(MyDateTimeFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()

        if today.month == 1:
            last_month = today.replace(year=today.year - 1, month=12, day=1)
        else:
            last_month = today.replace(month=today.month - 1, day=1)

        # Remove unwanted links
        list_links = list(self.links)
        for item in list_links:
            if item[0] in ('Past 7 days', 'No date', 'Has date'):
                list_links.remove(item)
        # Last list item not removed...weird
        if list_links[-1][0] == 'Has date':
            list_links.remove(list_links[-1])
        self.links = tuple(list_links)

        self.links += ((
            (_('Last Month'), {
                self.lookup_kwarg_since: str(last_month),
                self.lookup_kwarg_until: str(today.replace(day=1)),
            }),
        ))


admin.site.register(Store)
admin.site.register(PaymentMethod)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget_amount')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('purchase_date_and_store', 'category', 'amount', 'payment_method', 'notes')
    list_filter = ('category', ('purchase_date', MyDateTimeFilter), 'payment_method', 'store')

    def purchase_date_and_store(self, obj):
        return f'{obj.purchase_date.strftime("%b %d")} - {obj.store}'
    purchase_date_and_store.short_description = 'Transaction'


class SavingsAdmin(admin.ModelAdmin):
    actions = ['add_monthly_budget']
    list_display = ('name', 'total', 'monthly_budgeted_amount')
    ordering = ['-monthly_budgeted_amount']

    def add_monthly_budget(self, request, query_set):
        payment_method = PaymentMethod.objects.get(name='TRANSFER')
        today = datetime.today()

        for category in query_set:
            store = Store.objects.get(name=category.name)

            transaction = SavingsTransaction(
                store=store,
                amount=category.monthly_budgeted_amount,
                transaction_date=today.replace(day=1),
                saving=category,
                payment_method=payment_method,
                notes='Add monthly budget amount'
            )

            transaction.save()
            category.total += category.monthly_budgeted_amount
            category.save()

    add_monthly_budget.short_description = 'Add monthly budgeted amount'


class SavingsTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_date_and_store', 'saving', 'amount', 'payment_method', 'notes')
    list_filter = ('saving', ('transaction_date', MyDateTimeFilter), 'payment_method')

    def transaction_date_and_store(self, obj):
        return f'{obj.transaction_date.strftime("%b %d")} - {obj.store}'
    transaction_date_and_store.short_description = 'Transaction'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Savings, SavingsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SavingsTransaction, SavingsTransactionAdmin)
