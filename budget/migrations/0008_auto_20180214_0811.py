# Generated by Django 2.0.2 on 2018-02-14 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0007_transaction_payment_method'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-purchase_date']},
        ),
    ]
