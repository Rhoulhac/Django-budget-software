# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 23:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_auto_20170325_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created_date',
        ),
    ]
