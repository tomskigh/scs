# django library
from django.contrib import admin

# my models
from medical_visit.models import Specialization, Medical, MedicalVisit


# Register your models here.


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['type_of_specialization', 'slug', 'active']
    prepopulated_fields = {'slug': ('type_of_specialization',)}
    ordering = ['type_of_specialization']


@admin.register(Medical)
class MedicalAdmin(admin.ModelAdmin):
    list_display = ('forename', 'surname', 'nickname', 'presence', 'consulting_room')
    list_filter = ('surname', 'specialization')
    list_editable = ('presence',)
    ordering = ['surname']


@admin.register(MedicalVisit)
class MedicalVisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_of_visit', 'hour_of_visit')
    list_filter = ('patient', 'doctor')
    ordering = ['date_of_visit', 'hour_of_visit']
