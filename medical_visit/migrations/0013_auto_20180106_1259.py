# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-06 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_visit', '0012_auto_20171226_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalvisit',
            name='date_of_visit',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='medicalvisit',
            name='hour_of_visit',
            field=models.CharField(max_length=10),
        ),
    ]