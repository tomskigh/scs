# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_visit', '0005_auto_20171208_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalvisit',
            name='hour_of_visit',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
