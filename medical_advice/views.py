# standart library
from datetime import date
from smtplib import SMTPConnectError

# django library
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

# my models
from medical_visit.models import Medical, MedicalVisit
from medical_advice.models import MedicalAdviceDescription

# my forms
from medical_advice.forms import MedicalAdviceDescriptionForm

#my functions
from functions.myfunctions import my_context

# post_office module
from post_office import mail


# Create your views here


# medical advice view
class MedicalAdviceView(View):

    def get(self, request, username):
        now = date.today()
        doctor = Medical.objects.get(nickname=username)
        visits = MedicalVisit.objects.filter(doctor=doctor, date_of_visit=now).order_by('hour_of_visit')
        paginator = Paginator(visits, 4)
        page = request.GET.get('page')
        visits = paginator.get_page(page)

        if not visits:
            msg = r'No patients are register for today medical advice'
            messages.error(request, msg)
            context={'now': now, 'doctor': doctor}
            return render(request, 'medical_advice/medical_advice.html', context)
        else:
            context = {'now': now, 'doctor': doctor, 'visits': visits}
            return render(request, 'medical_advice/medical_advice.html', context)



# medical advice descriptions view
class AdviceDescriptionView(View):

    def get(self, request, username, patient_id):
        form = MedicalAdviceDescriptionForm()
        context = my_context(username, patient_id)
        context['form'] = form
        #pm = MedicalAdviceDescription.objects.filter(visit__date_of_visit__year=2018)

        return render(request, 'medical_advice/medical_advice_description.html', context)


    def post(self, request, username, patient_id):
        defaults, kwargs = dict(), dict()
        context = my_context(username, patient_id)
        kwargs.__setitem__('visit', context['visit'])

        if len(request.POST) > 1:
            form = MedicalAdviceDescriptionForm(data=request.POST)
            context['form'] = form

            if form.is_valid():
                cd = form.cleaned_data
                data = {'symptoms': cd['symptoms'],
                        'discount': cd['discount'],
                        'recommendations': cd['recommendations'],
                        'prescribed_medicines': cd['prescribed_medicines'],}

                for key, value in data.items():
                    defaults.__setitem__(key, value)

                _, created = MedicalAdviceDescription.objects.update_or_create(defaults=defaults,**kwargs)

                if created:
                    msg = r'Successful add new advice to data base...'
                    messages.success(request, msg)
                else:
                    msg = r'Successfull update exist advice in data base...'
                    messages.success(request, msg)


                context['prescribed_medicines'] = cd['prescribed_medicines']

                return render(request, 'medical_advice/medical_advice_description.html', context)

        return render(request, 'medical_advice/medical_advice_description.html', context)


# medical prescriptions detail view
class MedicalPrescriptionDetailView(View):

    def get(self, request, username, patient_id):
        context = my_context(username, patient_id)

        return render(request, 'medical_advice/medical_prescription_detail.html', context)


# medical prescriptions pdf sender view
class MedicalPrescriptionSender(View):

    def get(self, request, username, patient_id):
        context = my_context(username, patient_id)
        frm = (context['patient'].first_name,
               context['patient'].last_name,
               context['doctor'].forename,
               context['doctor'].surname,
               context['doctor'].specialization,)

        try:
            # sendig e-mail with pdf file attachment
            with open(r'static\email_msg\massage_txt', 'r') as txt, open(r'static\email_msg\massage_html', 'r') as html:
                msg = txt.read()
                html = html.read()
                mail.send(context['patient'].email,
                          subject = r'Your medical prescription',
                          message=msg.format(*frm),
                          html_message=html,
                          headers={'Reply-to': settings.ADMIN_EMAIL},
                          context={'patient': context['patient'], 'doctor': context['doctor']},
                          priority='now',)

                msg = r'Successfull sent e-mail to {} {}'
                messages.success(request, msg.format(context['patient'].first_name, context['patient'].last_name))

        except SMTPConnectError as error:
            messages.error(request, r'Error: {}'.format(error))

        kwargs = {'username': username, 'patient_id': patient_id}
        return HttpResponseRedirect(reverse('medical_advice:medical_prescription_detail', kwargs=kwargs))
