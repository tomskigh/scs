# django library
from django.db import models
from django.urls import reverse

# my models
from registration.models import Patient


# Create your models here.


class Specialization(models.Model):
    type_of_specialization = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, help_text='A short label, generally used in URLs')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('type_of_specialization',)

    def __str__(self):
        return self.type_of_specialization


class Medical(models.Model):
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING,)
    forename = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    consulting_room = models.IntegerField(unique=True)
    nickname = models.CharField(max_length=200, unique=True)
    presence = models.BooleanField(default=True)

    class Meta:
        ordering = ('surname', 'specialization')

    def __str__(self):
        return '{} {}'.format(self.surname, self.forename)

    def get_absolute_url(self):
        return reverse('medical_user_data_change', args=[self.id])


class MedicalVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, related_name='patients')
    doctor = models.ForeignKey(Medical, on_delete=models.DO_NOTHING, related_name='doctors')
    date_of_visit = models.DateField()
    hour_of_visit = models.CharField(max_length=10,)

    def __str__(self):
        frm = (self.doctor.forename,
               self.doctor.surname,
               self.patient.first_name,
               self.patient.last_name,
               self.date_of_visit,
               self.hour_of_visit)
        return 'Dr {} {}, patient: {} {}, date: {}, hour: {}'.format(*frm)

    def get_absolute_url(self):
        return reverse('medical_advice:advice_description', args=[self.doctor.nickname, self.patient.id])