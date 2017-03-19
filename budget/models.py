import datetime

from django.db import models
# from django.utils import timezone


class Store(models.Model):
    name = models.CharField("Store", unique=True, max_length=255)


class Category(models.Model):
    name = models.CharField("Budget Category", unique=True, max_length=255)
    budget_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class TransactionManager(models.Manager):

    def current_monthly_spending_by_category(self, category):
        return self.filter(
            category=category,
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        )

    def current_monthly_spending(self):
        return self.filter(
            purchase_date__year=datetime.datetime.now().year,
            purchase_date__month=datetime.datetime.now().month
        )


class Transaction(models.Model):
    purchase_date = models.DateField("Purchase Date", blank=True, null=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    store = models.ForeignKey(Store)
    category = models.ForeignKey(Category)

    objects = TransactionManager()

    def __str__(self):
        return self.name

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
