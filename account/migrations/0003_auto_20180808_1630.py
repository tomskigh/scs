# Generated by Django 2.0.5 on 2018-08-08 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20180729_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.ProfessionalGroup'),
        ),
    ]
