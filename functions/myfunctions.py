# standard library
import random
import threading
import unicodedata
from pathlib import Path
from barcode import generate
from smtplib import SMTPConnectError
from datetime import date, timedelta

# django library
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mass_mail
from django.core.management import call_command
from django.shortcuts import HttpResponseRedirect

# my models
from registration.models import Patient
from medical_visit.models import Medical, MedicalVisit
from medical_advice.models import MedicalAdviceDescription


# Create your functions here


# create backup all files
def backup():
    # path to backup
    path = Path('backup_json\db.json')
    try:
        with open(path, 'w') as jsonfile:
            call_command('dumpdata', indent=4, stdout=jsonfile)
    except FileNotFoundError as err:
        print('\nSomething wrong... Error: {}'.format(err))

    for model, path in settings.FIXTURE_DIRS.items():
        try:
            with open(path, 'w') as jf:
                call_command('dumpdata', model, indent=4, stdout=jf)
        except FileNotFoundError as err:
            print('\nSomething wrong... Error: {}'.format(err))


# return list of visit of hours
def visits_list(**kwargs):
        visit_list = MedicalVisit.objects.filter(**kwargs).order_by('date_of_visit', 'hour_of_visit')
        visit_list = visit_list.values_list('hour_of_visit', flat=True)
        visit_list = list(visit_list)
        return visit_list


# replace polish diacritical chars on latin and return as lowercase
def diacritical_remover(text):
    if isinstance(text,str):
        result = [char for char in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(char)]

        for i in range(len(text)):
            if result[i] == 'ł':
                result[i] = 'l'
        return ''.join(result)
    else:
        print('Argument must be string type...')


# return dict holiday : date for current year
def holidays(date_visit):
    year=date_visit.year
    a = year%19
    b = int(year/100)
    c = year%100
    d = int(b/4)
    e = b%4
    f = int((b + 8)/25)
    g = int((b - f + 1)/3)
    h = (19*a + b - d - g + 15)%30
    i = int(c/4)
    k = c%4
    l = (32 + 2*e + 2*i - h - k)%7
    m = int((a + 11*h + 22*l)/451)
    p = (h + l - 7*m + 114)%31
    day = int(p + 1)
    month = int((h + l - 7*m + 114)/31)

    holidays = {'New Year':  date(year, 1, 1),
                'Epiphany': date(year, 1, 6),
                'Easter': date(year,month,day),
                'Easter Monday': date(year,month,day)+timedelta(days=1),
                'Labour Day': date(year,5,1),
                'Feast of the constitution third of May': date(year,5,3),
                'Descent of the Holy Spirit': date(year,month,day)+timedelta(days=49),
                "God's Body": date(year,month,day)+timedelta(days=60),
                'Assumption of the Blessed Virgin Mary': date(year,8,15),
                'All Saints Day': date(year,11,1),
                'Independence Day': date(year,11,11),
                'Christmas-first day': date(year,12,25),
                'Christmas-second day': date(year,12,26)}

    return holidays

# asynchronic absence e-mail sender class
class EmailThread(threading.Thread):

    def __init__(self, datatuple):
        super(EmailThread, self).__init__()
        self.datatuple = datatuple

    def run (self):
        send_mass_mail(self.datatuple, fail_silently=True)


# sending absence e-mail using EmailThread class
def absence_email(request):
    recipients, datatuple, absence = dict(), tuple(), None
    subject = r'Your medical visit'
    from_email = settings.DEFAULT_FROM_EMAIL

    doctors = Medical.objects.filter(presence=False)
    for doctor in doctors:
        absence = MedicalVisit.objects.filter(doctor_id=doctor.id, date_of_visit=date.today())
        if absence:
            for visit in absence:
                frm = (visit.patient.first_name, visit.patient.last_name, doctor.forename,
                       doctor.surname, doctor.specialization ,visit.hour_of_visit, doctor.consulting_room)
                body ="Dear {} {}\n\nYour medical appointment today is canceled because of doctor's absence.\n\nDoctor: {} {} ({})\nHour of medical visit: {}\nConsulting room: {}\n\nPlease contact registration staff to set new date of medical visit.\n\nSincerely".format(*frm)
                recipients.__setitem__(body,visit.patient.email)

    if recipients:
        try:
            datatuple = tuple([(subject, message, from_email, [to_email,]) for message, to_email in recipients.items()])

            # send all absence e-mail(s) to patients
            email = EmailThread(datatuple)
            email.daemon = True
            email.start()
            email.join()

        except SMTPConnectError:
            return HttpResponseRedirect('registration/register')

        finally:
            for doctor in doctors:
                MedicalVisit.objects.filter(doctor=doctor, date_of_visit=date.today()).delete()

    return render(request, 'registration/absence_email.html', {'recipients': recipients, 'absence': absence})


# generate barcode for medical
def medical_barcode(id):
    path = r'C:\Users\tomsk\Desktop\SM\small_clinic_study\static\images\barcode_med'
    digit = random.randint(11,10**11)
    if len(str(id)) == 1:
        code = str(digit) + '0' + str(id)
        generate('EAN13', code, output=path)
    else:
        code = str(digit) + str(id)
        generate('EAN13', code, output=path)


# return most useful data
def my_context(username, patient_id):
    now = date.today()
    patient = Patient.objects.get(id=patient_id)
    doctor = Medical.objects.get(nickname=username)
    visit = MedicalVisit.objects.get(patient=patient, doctor=doctor, date_of_visit=now)
    medical_barcode(doctor.id)

    context={'now': now,
             'visit': visit,
             'doctor': doctor,
             'patient': patient,}

    if MedicalAdviceDescription.objects.filter(visit=visit).exists():
        advice = MedicalAdviceDescription.objects.get(visit=visit)
        context['advice'] = advice
        medicines = advice.prescribed_medicines.split('\r\n')
        context['medicines'] = medicines

        return context

    else:
        return context
