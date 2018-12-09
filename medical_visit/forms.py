# standard library
from django import forms
from datetime import date

# django core
from django.core.validators import MinValueValidator

# django_datetime widget
from datetimewidget.widgets import DateWidget

# my models
from medical_visit.models import Medical, Specialization, MedicalVisit



# Create your forms here


dateOptions = {'format': 'yyyy-mm-dd', 'autoclose': 'true', 'showMeridian': 'false', 'weekStart': 1, 'todayBtn': 'true'}


class MedicalAddForm(forms.ModelForm):
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.filter(active=True), label='Specialization')
    email = forms.EmailField(label='E-mail')
    class Meta:
        model = Medical
        fields = ('specialization', 'forename', 'surname', 'email', 'consulting_room')



class SpecializationForm(forms.ModelForm):
    type_of_specialization = forms.ModelChoiceField(queryset=Specialization.objects.filter(active=True),
                                                    widget=forms.RadioSelect,
                                                    empty_label=None,
                                                    label='Choice specialization for proceed registration...')

    class Meta:
        model = Specialization
        fields = ('type_of_specialization',)



class DateVisitRegisterForm(forms.ModelForm):
    date_of_visit = forms.DateField(widget=DateWidget(options=dateOptions, bootstrap_version=3), initial=date.today())

    class Meta:
        model = MedicalVisit
        fields = ('date_of_visit',)
