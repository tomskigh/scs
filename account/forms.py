# django library
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# my models
from account.models import ProfessionalGroup



class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Forename')
    last_name = forms.CharField(required=True, label='Surname')
    email = forms.EmailField(label='E-mail address')
    group = forms.ModelChoiceField(queryset=ProfessionalGroup.objects.exclude(slug='medical-staff'),
                                   widget=forms.RadioSelect, empty_label=None, label='Professional group')

    class Meta:
        model = User
        fields = ('username', 'group', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active', 'is_staff')


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.group = self.cleaned_data['group']
        user.is_active = self.cleaned_data['is_active']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user


class MedicalUserDataChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
        widgets = {'first_name': forms.TextInput(attrs={'readonly':'readonly'}),
                   'last_name': forms.TextInput(attrs={'readonly':'readonly'}),
                   'email': forms.EmailInput()}
