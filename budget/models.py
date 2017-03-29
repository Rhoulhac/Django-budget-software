import datetime

from django.db import models
# from django.utils import timezone


class Store(models.Model):
    name = models.CharField("Store", unique=True, max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Budget Category", unique=True, max_length=255)
    budget_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField("Payment Method", unique=True, max_length=255)

    def __str__(self):
        return self.name


class TransactionQueryset(models.QuerySet):

    def current_monthly_spending(self):
        monthly_list = []
        query = self.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        )
        for q in query:
            monthly_list.append({
                'purchase_date': q.purchase_date,
                'amount': q.amount,
                'store': q.store,
                'category': q.category,
                'payment_method': q.payment_method,
            })
        return monthly_list

    def previous_monthly_spending(self):
        prev_monthly_list = []
        query = self.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month - 1
        )
        for q in query:
            prev_monthly_list.append({
                'purchase_date': q.purchase_date,
                'amount': q.amount,
                'store': q.store,
                'category': q.category,
                'payment_method': q.payment_method,
            })
        return prev_monthly_list

    def previous_years_monthly_spending(self):
        return self.filter(
            purchase_date__year=datetime.datetime.now().year - 1,
            purchase_date__month=datetime.datetime.now().month
        )

    def current_monthly_spending_by_category(self, category):
        return self.filter(
            category=category,
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        )


class Transaction(models.Model):
    store = models.ForeignKey(Store)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateField("Purchase Date", blank=True, null=False)
    category = models.ForeignKey(Category)
    payment_method = models.ForeignKey(PaymentMethod)

    objects = TransactionQueryset().as_manager()

    def last_year_monthly(self):
        pass


class Savings(models.Model):
    name = models.CharField("Savings Category", unique=True, max_length=255)
    amount_saved = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'savings'

    def __str__(self):
        return self.name

    def monthly_savings(self):
        pass
