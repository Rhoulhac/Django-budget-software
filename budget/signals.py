from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Savings, SavingsTransaction


@receiver(post_save, sender=SavingsTransaction)
def update_total(sender, instance, created, **kwargs):
    if created:
        savings = Savings.objects.get(name=instance.saving)
        savings.total += instance.amount
        savings.save()
