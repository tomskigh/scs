# django.core
from django.contrib import admin

# my models
from medical_advice.models import MedicalAdviceDescription

# Register your models here.


@admin.register(MedicalAdviceDescription)
class MedicalAdviceDescriptionAdmin(admin.ModelAdmin):
    list_display = ('visit',)
    list_filter = ('id',)
    ordering = ['-id']
    exclude = ['symptoms', 'recommendations', 'prescribed_medicines', 'discount']
