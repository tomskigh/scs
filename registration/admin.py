# django.core
from django.contrib import admin

# my models
from registration.models import Patient

# Register your models here.


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birthday', 'ensured')
    list_filter = ('last_name',)
    list_editable = ('ensured',)
    ordering = ['last_name']

    fieldsets = [('Patient', {'fields': ('last_name', 'first_name', 'birthday', 'ensured',)}),
                 ('Data', {'classes': ('collapse',), 'fields': ('postal', 'city', 'street', 'phone', 'email')}),]
