# standard library
from datetime import date

# django library
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, ListView
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect

# my models
from registration.models import Patient
from medical_visit.models import Medical, Specialization, MedicalVisit

# my forms
from registration.forms import PatientForm
from medical_visit.forms import SpecializationForm

# my functions
from functions.myfunctions import visits_list, absence_email


# Create your views here.


# patient list view
class PatientListView(View):

    def get(self, request):
        doctors = Medical.objects.filter(presence=False)
        patients = Patient.objects.all().order_by('last_name')
        heads = ['name', 'postal', 'city', 'street', 'phone', 'birthday', 'email', 'ensured']
        context = {'heads': heads, 'patients': patients}
        for doctor in doctors:
            visit = MedicalVisit.objects.filter(doctor=doctor, date_of_visit=date.today()).exists()
            if visit:
                context['visit'] = visit
                return render(request, 'registration/patient_list.html', context)

        return render(request, 'registration/patient_list.html', context)


# class PatientListView(ListView):
#     model = Patient
#     ordering = ('last_name')
#
#     def get_context_data(self, **kwargs):
#         heads = ['name', 'postal', 'city', 'street', 'phone', 'birthday', 'email', 'ensured']
#         context = {'heads': heads}
#         for doctor in Medical.objects.filter(presence=False):
#             visit = MedicalVisit.objects.filter(doctor=doctor, date_of_visit=date.today()).exists()
#             if visit:
#                 context['visit'] = visit
#         return super().get_context_data(**context)


# patient detail view
class PatientDetailView(View):

    def get(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        visits = visits_list(patient=patient, date_of_visit__gte=date.today())
        form = SpecializationForm()
        context = {'form': form,
                   'visits': visits,
                   'patient': patient,
                   'patient_id':patient_id}

        return render(request, 'registration/patient_detail.html', context)

    def post(self, request, patient_id):
        form = SpecializationForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            spec = cd['type_of_specialization']
            kwargs = {'patient_id':patient_id, 'spec':spec}
            return HttpResponseRedirect(reverse('medical_visit:medical_staff_view', kwargs=kwargs))

        return render(request, 'registration/patient_detail.html', {'form': form})



# add new patient view+
class PatientAddView(View):

    def get(self, request):
        city_list = Patient.objects.values_list('city', flat=True).distinct()
        cities = list(city_list)
        form = PatientForm()
        context = {'form': form, 'cities': cities}
        return render(request, 'registration/patient_add.html', context)

    def post(self, request):
        form = PatientForm(data=request.POST)

        if form.is_valid():
            new_patient = form.save(commit=False)
            data = form.cleaned_data

            # check new patient in database
            if Patient.objects.all().filter(**data).exists():
                msg = r'Data for patient ({}) are existing in database...'
                messages.error(request, msg.format(data['first_name'],' ',data['last_name']))

            else:
                new_patient.save()
                msg = r'Succesful add new patient ({})'
                messages.success(request, msg.format(data['first_name'],' ',data['last_name']))

        return render(request, 'registration/patient_add.html', {'form': form})


# patient data change view
def patient_data_change(request, patient_id):
    kwargs = {'patient_id':patient_id}
    patient = Patient.objects.get(id=patient_id)
    fields = list(patient.__dict__.keys())[2:]
    old_values = Patient.objects.filter(id=patient_id).values(*fields)[0]

    if request.method == 'POST':
        form = PatientForm(data=request.POST)

        if form.is_valid():
            new_values = form.cleaned_data
            ensured = new_values['ensured']

            if new_values != old_values:
                try:
                    if not ensured:
                        MedicalVisit.objects.filter(patient=patient, date_of_visit__gte=date.today()).delete()
                    Patient.objects.update_or_create(**old_values,defaults=new_values)
                    msg = r'Successful update data for patient {} {}'
                    messages.success(request, msg.format(patient.first_name, patient.last_name))
                except Patient.DoesNotExist:
                    messages.warning(request, r'Somthing wrong... try again!')
            else:
                messages.info(request, r'Nothing to change!')

            return HttpResponseRedirect(reverse('registrations:register_patient_detail', kwargs=kwargs))
    else:
        form = PatientForm(initial=old_values)

    return render(request, 'registration/patient_change.html', {'form': form})


# medicals present view
class MedicalPresentView(View):

    def get(self, request, spec):
        specialization = Specialization.objects.get(slug=spec)
        medicals = Medical.objects.filter(specialization=specialization).order_by('surname',)
        for medical in medicals:
            user = User.objects.get(username=medical.nickname)
            if user.is_active == False:
                medicals = medicals.exclude(pk=medical.id)
        return render(request, 'registration/medical_presence_view.html', {'medicals': medicals, 'spec': spec})

    def post(self, request, spec):

        if request.method == 'POST':
            specialization = Specialization.objects.get(slug=spec)
            medicals = Medical.objects.filter(specialization=specialization).order_by('surname',)
            medical_id_list = request.POST.getlist('presence')

            for medical in medicals:
                if str(medical.id) not in medical_id_list:
                    Medical.objects.filter(id=medical.id).update(presence=False)

                else:
                    Medical.objects.filter(id=medical.id).update(presence=True)

            return HttpResponseRedirect(reverse('registrations:medical_presence', kwargs={'spec': spec}))

        else:
            return HttpResponseRedirect(reverse('registrations:medical_presence', kwargs={'spec': spec}))


# send absence email to patients
class SendEmailView(View):

    def get(self, request):
        return absence_email(request)
