import datetime

from django.db import models
# from django.utils import timezone


class Store(models.Model):
    name = models.CharField("Store", unique=True, max_length=255)

    class Meta:
        ordering = ['name']

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


class Transaction(models.Model):
    store = models.ForeignKey(Store)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateField("Purchase Date", blank=True, null=False)
    category = models.ForeignKey(Category)
    payment_method = models.ForeignKey(PaymentMethod)

    class Meta:
        ordering = ['-purchase_date']

class Savings(models.Model):
    name = models.CharField("Savings Category", unique=True, max_length=255)
    amount_saved = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'savings'

    def __str__(self):
        return self.name

    def monthly_savings(self):
        pass
