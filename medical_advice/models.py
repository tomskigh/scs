# django library
from django.db import models

# my models
from medical_visit.models import MedicalVisit


# Create your models here.


class MedicalAdviceDescription(models.Model):
    visit = models.ForeignKey(MedicalVisit, on_delete=models.DO_NOTHING)
    symptoms = models.TextField()
    recommendations = models.TextField()
    prescribed_medicines = models.TextField()
    discount = models.CharField(max_length=5, default='100%')

    def __str__(self):
        frm = (self.visit.doctor.forename,
               self.visit.doctor.surname,
               self.visit.patient.first_name,
               self.visit.patient.last_name,
               self.visit.date_of_visit,
               self.visit.hour_of_visit)
        return 'Dr {} {}, patient: {} {}, date: {}, hour: {}'.format(*frm)