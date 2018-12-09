# django library
from django.contrib import admin

# my models
from account.models import Profile, ProfessionalGroup

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'group']


@admin.register(ProfessionalGroup)
class ProfessionalGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
