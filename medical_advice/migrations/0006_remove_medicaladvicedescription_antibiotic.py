# Generated by Django 2.0.1 on 2018-01-28 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_advice', '0005_medicaladvicedescription_antibiotic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicaladvicedescription',
            name='antibiotic',
        ),
    ]
