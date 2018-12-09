# django library
from django.db import models
from django.urls import reverse

# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    postal = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    birthday = models.DateField(null=True)
    email = models.EmailField(null=True, blank=True)
    ensured = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.last_name,self.first_name)

    def save(self, *args, **kwargs):
        for field in ['first_name', 'last_name', 'city', 'street']:
            value = getattr(self, field, False)
            if value:
                setattr(self, field, value.capitalize())
        super(Patient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('registrations:register_patient_detail', args=[self.id])
