from django.db import models


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
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateField("Purchase Date", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    notes = models.CharField("Note", max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return f'{self.purchase_date} {self.category} - {self.store}'


class Savings(models.Model):
    name = models.CharField("Savings Category", unique=True, max_length=255)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_budgeted_amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = 'savings'

    def __str__(self):
        return self.name

    def monthly_savings(self):
        pass
