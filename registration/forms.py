# django library
from django import forms
from datetimewidget.widgets import DateWidget

# my models
from registration.models import Patient


dateOptions = {'format': 'yyyy-mm-dd', 'autoclose': 'true', 'showMeridian': 'false', 'weekStart': 1, 'todayBtn': 'true'}


class PatientForm(forms.ModelForm):
    first_name = forms.CharField(label='Forename')
    last_name = forms.CharField(label='Surname')

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'postal', 'city', 'street', 'phone', 'birthday', 'email', 'ensured')
        widgets = {'birthday': DateWidget(options=dateOptions, bootstrap_version=3),
                   'city': forms.TextInput(attrs={'id':'cities'})}
