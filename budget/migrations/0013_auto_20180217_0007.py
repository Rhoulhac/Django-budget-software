# Generated by Django 2.0.2 on 2018-02-17 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_transaction_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Note'),
        ),
    ]
