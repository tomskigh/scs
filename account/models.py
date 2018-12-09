# django library
from django.db import models
from django.conf import settings


# Create your models here.


class ProfessionalGroup(models.Model):
    name = models.CharField(max_length=50, db_index=True, help_text='Name of professional group')
    slug = models.SlugField(max_length=70, db_index=True, unique=True, help_text='A short label, generally used in URLs')


    def __str__(self):
        return '{}'.format(self.slug)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(ProfessionalGroup, on_delete=models.CASCADE)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return '{}'.format(self.user)
