# Generated by Django 2.0.5 on 2018-07-29 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_advice', '0006_remove_medicaladvicedescription_antibiotic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaladvicedescription',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medical_visit.MedicalVisit'),
        ),
    ]
