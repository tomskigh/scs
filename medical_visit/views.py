# standart library
from datetime import datetime, date, time

# django library
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect

# my models
from registration.models import Patient
from account.models import Profile, ProfessionalGroup
from medical_visit.models import Medical, Specialization, MedicalVisit

# my forms
from medical_visit.forms import DateVisitRegisterForm, MedicalAddForm

# my functions
from functions.myfunctions import visits_list, holidays, diacritical_remover


# Create your views here.


# adding new medical view
class MedicalAddView(View):

    def get(self, request):
        conrooms = Medical.objects.values_list('consulting_room', flat=True)
        if conrooms:
            conrooms = max(list(conrooms)) + 1
        else:
            conrooms = 1
        form = MedicalAddForm(initial={'consulting_room': conrooms})

        return render(request, 'medical_visit/medical_add.html', {'form': form})

    def post(self, request):
        kwargs, nickname, password, medical = None, None, None, None

        if len(request.POST) > 1:
            form = MedicalAddForm(data=request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                specialization = cd['specialization']
                forename = cd['forename']
                surname = cd['surname']
                email = cd['email']
                consulting_room = cd['consulting_room']

                kwargs = {'email': email,
                          'surname': surname,
                          'forename': forename,
                          'specialization': specialization,
                          'consulting_room': consulting_room}

                new_medical = Medical.objects.create(**kwargs)

                if new_medical.id:
                    # create credentials for new medicals
                    strid = str(new_medical.id)
                    medical = Medical.objects.get(id=new_medical.id)

                    if new_medical.id > 0 and new_medical.id <= 9:
                        strid = '0' + str(new_medical.id)

                    nickname = ''.join([medical.forename[:2], medical.surname[:2], str(medical.specialization)[:2], strid]).lower()
                    password = ''.join([str(medical.specialization), strid]).lower()
                    nickname = diacritical_remover(nickname)
                    password = diacritical_remover(password)

                    if nickname and password:

                        Medical.objects.filter(id=new_medical.id).update(nickname=nickname)
                        user=User.objects.create_user(username=nickname,
                                                      password=password,
                                                      email=new_medical.email,
                                                      first_name=new_medical.forename,
                                                      last_name=new_medical.surname)
                        group = ProfessionalGroup.objects.get(slug='medical-staff')
                        Profile.objects.create(user=user, group=group)

                kwargs['medical'] = medical
                kwargs['nickname'] = nickname
                kwargs['password'] = password

                return render(request, 'medical_visit/medical_add.html', kwargs)

            else:

                conrooms = Medical.objects.values_list('consulting_room', flat=True)

                return render(request, 'medical_visit/medical_add.html', {'conrooms': max(list(conrooms))})


# medical's register visit view
class MedicalView(View):

    def get(self, request, patient_id, spec):
        specialization = Specialization.objects.get(slug=spec)
        patient = Patient.objects.get(id=patient_id)
        medicals = Medical.objects.filter(specialization=specialization).order_by('surname')
        # li = Medical.objects.filter(email__contains='onet')
        # cs = Medical.objects.filter(consulting_room__gte=7)
        # cg = Medical.objects.filter(consulting_room__gte=2,consulting_room__lte=10)
        for medical in medicals:
            user = User.objects.get(username=medical.nickname)
            if user.is_active == False:
                medicals = medicals.exclude(pk=medical.id)
        visits = visits_list(patient=patient, date_of_visit__gte=date.today())

        if not medicals.exists():
            msg = r'No doctors in selected specialization ({})'
            messages.error(request, msg.format(spec))
            kwargs={'patient_id':patient_id}
            return HttpResponseRedirect(reverse('registrations:register_patient_detail', kwargs=kwargs))
        else:
            context = {'spec': spec,
                       'visits': visits,
                       'patient': patient,
                       'medicals': medicals,
                       'patient_id': patient_id}
            return render(request, 'medical_visit/medical_staff_list.html', context)


    def post(self, request, patient_id, spec):

        if len(request.POST) > 1:
            medical_id = request.POST['medical_id']
            kwargs = {'spec': spec, 'medical_id': medical_id, 'patient_id': patient_id}
            return HttpResponseRedirect(reverse('medical_visit:visit_date_register', kwargs=kwargs))

        else:
            msg = r'Please select doctor name'
            messages.error(request, msg)
            kwargs={'spec': spec, 'patient_id':patient_id}
            return HttpResponseRedirect(reverse('medical_visit:medical_staff_view', kwargs=kwargs))


# booking data visit view
class VisitDateView(View):

    def get(self, request, patient_id, spec, medical_id):
        form = DateVisitRegisterForm()
        patient = Patient.objects.get(id=patient_id)
        medical = Medical.objects.get(id=medical_id)
        visits = visits_list(patient=patient, date_of_visit__gte=date.today())
        context = {'spec': spec,
                   'form': form,
                   'visits': visits,
                   'patient': patient,
                   'medical': medical,
                   'patient_id': patient_id,}
        return render(request, 'medical_visit/visit_date_register.html', context)

    def post(self, request, patient_id, spec, medical_id):
        kwargs={'spec': spec,
                'patient_id': patient_id,
                'medical_id': medical_id}

        if len(request.POST) > 1:
            form = DateVisitRegisterForm(data=request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                date_of_visit = cd['date_of_visit']

                if date_of_visit >= date.today():
                    if date_of_visit.weekday() < 5:
                        if date_of_visit not in holidays(date_of_visit).values():
                            date_of_visit = datetime.strftime(date_of_visit,'%Y-%m-%d')
                            kwargs['date_of_visit'] = date_of_visit
                            return HttpResponseRedirect(reverse('medical_visit:visit_hour_register', kwargs=kwargs))
                        else:
                            msg =r'Selected date is a holiday ({}). Please select correct date!'
                            for key, value in holidays(date_of_visit).items():
                                if value == date_of_visit:
                                    messages.error(request, msg.format(key))
                    else:
                        if date_of_visit.weekday() == 5:
                            msg =r'Selected date is a Saturday... Please select correct date!'
                            messages.error(request, msg)
                        else:
                            msg =r'Selected date is a Sunday... Please select correct date!'
                            messages.error(request, msg)

                else:
                    msg = r"Please select today's or future date..."
                    messages.error(request, msg)

                return HttpResponseRedirect(reverse('medical_visit:visit_date_register', kwargs=kwargs))

            else:
                msg = r'Please select a valid visit date...'
                messages.error(request, msg)

                return HttpResponseRedirect(reverse('medical_visit:visit_date_register', kwargs=kwargs))

# booking hour visit view
class VisitHourView(View):

    def get(self, request, patient_id, spec, medical_id, date_of_visit):
        # hours of visit
        hours, minutes = (8,12), (0,41,20)
        # permanent hours of medical visits list = phomv_list
        phomv_list = [str(time(x,y)) for x in range(*hours) for y in range(*minutes)]
        patient = Patient.objects.get(id=patient_id)
        doctor = Medical.objects.get(id=medical_id)
        doc_visit_list = visits_list(doctor=doctor, date_of_visit=date_of_visit)
        visit_hour_list = visits_list(patient_id=patient_id, date_of_visit=date_of_visit)
        visits = MedicalVisit.objects.filter(patient=patient, date_of_visit=date_of_visit)
        valid_hour_list = {}

        if visits:
            for visit in visits:
                if visit.doctor.id != int(medical_id) and str(visit.doctor.specialization) == spec:
                    visit_hour_list.remove(visit.hour_of_visit)
                    valid_hour_list = set(visit_hour_list + doc_visit_list)
                    valid_hour_list = sorted(list(valid_hour_list))

                else:
                    valid_hour_list = set(visit_hour_list + doc_visit_list)
                    valid_hour_list = sorted(list(valid_hour_list))
        else:
            valid_hour_list = doc_visit_list

        visits = visits_list(patient=patient, date_of_visit__gte=date.today())
        date_of_visit = datetime.strptime(date_of_visit, '%Y-%m-%d')
        date_of_visit = date_of_visit.date()
        context = {'spec': spec,
                   'doctor': doctor,
                   'visits': visits,
                   'patient':patient,
                   'medical_id': medical_id,
                   'patient_id': patient_id,
                   'date_of_visit': date_of_visit,
                   'phomv_list': phomv_list,
                   'valid_hour_list': valid_hour_list,}
        return render(request, 'medical_visit/visit_hour_register.html', context)

    def post(self, request, patient_id, spec, medical_id, date_of_visit):
        date_of_visit = datetime.strptime(date_of_visit, '%Y-%m-%d')
        date_of_visit = date_of_visit.date()
        kwargs={'spec': spec,
                'patient_id':patient_id,
                'medical_id': medical_id,
                'date_of_visit': date_of_visit}

        if len(request.POST) > 1:
            hour_of_visit = request.POST['hour_of_visit']
            patient = Patient.objects.get(id=patient_id)
            doctor = Medical.objects.get(id=medical_id)
            visits = MedicalVisit.objects.filter(patient=patient, date_of_visit=date_of_visit)
            doc_id = None
            data = {'doctor': doctor,
                    'patient': patient,
                    'date_of_visit': date_of_visit,
                    'hour_of_visit': hour_of_visit}

            if not visits.exists():
                MedicalVisit.objects.create(**data)
                msg = r'Successful create new medical visit for {} {}'
                messages.success(request, msg.format(patient.first_name, patient.last_name))
            else:
                for visit in visits:
                    if str(visit.doctor.specialization) == spec:
                        doc_id = visit.doctor.id

                if doc_id:
                    values = {'doctor': doctor, 'hour_of_visit':hour_of_visit}
                    MedicalVisit.objects.filter(doctor_id=doc_id,
                                                patient=patient,
                                                date_of_visit=date_of_visit).update(**values)
                    msg = r'Successful update medical visit for {} {}'
                    messages.success(request, msg.format(patient.first_name, patient.last_name))
                else:
                    MedicalVisit.objects.create(**data)
                    msg = r'Successful create new medical visit for {} {}'
                    messages.success(request, msg.format(patient.first_name, patient.last_name))

            visits = visits_list(patient=patient, date_of_visit__gte=date.today())
            context = {'spec': spec,
                       'visits': visits,
                       'doctor': doctor,
                       'patient': patient,
                       'patient_id': patient_id,
                       'date_of_visit': date_of_visit,
                       'hour_of_visit': hour_of_visit,}
            return render(request, 'medical_visit/visit_hour_register.html', context)

        else:
            msg = r'Please select a visit hour...'
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('medical_visit:visit_hour_register', kwargs=kwargs))


# visit delete view
class VisitDeleteView(View):

    def get(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        visits = MedicalVisit.objects.filter(patient=patient, date_of_visit__gte=date.today())
        visits = visits.order_by('date_of_visit', 'hour_of_visit')
        context =  {'visits': visits,
                    'patient': patient,
                    'patient_id': patient_id}
        return render(request, 'medical_visit/delete_visits.html',context)

    def post(self, request, patient_id):

        if len(request.POST) > 1:
            patient = Patient.objects.get(id=patient_id)
            visits = MedicalVisit.objects.filter(patient=patient, date_of_visit__gte=date.today())
            visits = visits.order_by('date_of_visit', 'hour_of_visit')
            visit_id = request.POST.getlist('visit')

            for id in visit_id:
                instance = MedicalVisit.objects.filter(id=id)
                instance.delete()

            msg = r'Successful delete medical visit(s) for patient {} {}'
            messages.success(request, msg.format(patient.first_name, patient.last_name))
            context = {'visits': visits,
                       'patient': patient,
                       'patient_id': patient_id}
            return render(request, 'medical_visit/delete_visits.html', context)

        else:
            msg = r'Please select a visit(s) to delete...'
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('medical_visit:visit_delete', kwargs={'patient_id':patient_id}))
