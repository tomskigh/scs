# Generated by Django 2.0.5 on 2018-07-29 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_visit', '0013_auto_20180106_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medical',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='specializations', to='medical_visit.Specialization'),
        ),
        migrations.AlterField(
            model_name='medicalvisit',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='doctors', to='medical_visit.Medical'),
        ),
        migrations.AlterField(
            model_name='medicalvisit',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='patients', to='registration.Patient'),
        ),
    ]
