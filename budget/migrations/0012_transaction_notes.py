# Generated by Django 2.0.2 on 2018-02-17 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_auto_20180216_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='notes',
            field=models.CharField(default='', max_length=255, verbose_name='Note'),
            preserve_default=False,
        ),
    ]
