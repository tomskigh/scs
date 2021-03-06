# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-25 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('postal', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=50)),
                ('birthday', models.DateField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('ensured', models.BooleanField(default=True)),
            ],
        ),
    ]
