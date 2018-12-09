# django library
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout

# my models
from medical_visit.models import Medical
from account.models import Profile, ProfessionalGroup

# my forms
from account.forms import UserCreateForm, MedicalUserDataChangeForm

# my functions
from functions.myfunctions import backup


# Create your views here.


# check user is login as admin view
class AdminView(View):

    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            user = request.user.username
            md_id = Medical.objects.order_by('surname').first()
            return render(request, 'account/admin.html', {'user': user, 'md_id': md_id.id})
        else:
            return HttpResponseRedirect('/admin/')


# create new user view
class CreateNewUser(View):

    def get(self, request):
        form = UserCreateForm()
        return render(request,'account/create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            # create profil new user
            Profile.objects.create(user=new_user, group=new_user.group)
            messages.success(request, r'Success! New user ({}) is created...'.format(new_user.username))
        return render(request,'account/create_user.html', {'form': form})


# medical user data change view
class MedicalUserDataChange(View):

    def get(self, request, md_id):
        medical = Medical.objects.get(pk=md_id)
        medicals = Medical.objects.all().order_by('surname')
        user = User.objects.get(username=medical.nickname)
        data = {'first_name':user.first_name, 'last_name':user.last_name,
                'email':user.email, 'is_active':user.is_active, 'is_staff':user.is_staff}
        form = MedicalUserDataChangeForm(initial=data)
        context = {'medicals': medicals, 'form': form, 'md_id': md_id}

        return render(request, 'account/user_change_data.html', context)

    def post(self, request, md_id):
        form = MedicalUserDataChangeForm(data=request.POST)
        medical = Medical.objects.get(pk=md_id)
        medicals = Medical.objects.all()
        user = User.objects.get(username=medical.nickname)

        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            is_staff = cd['is_staff']
            is_active = cd['is_active']

            if user.is_active != is_active or user.is_staff != is_staff or user.email != email:
                user.is_active = is_active
                user.is_staff = is_staff
                user.email = email
                user.save()
                msg = r'Successful update data for medical {}'
                messages.success(request, msg.format(medical,))
            else:
                msg = r'Data for medical {} have not changed...'
                messages.success(request, msg.format(medical,))

            if is_active == False:
                Medical.objects.filter(pk=md_id).update(presence=False)
            else:
                Medical.objects.filter(pk=md_id).update(presence=True)


        return render(request, 'account/user_change_data.html', {'form': form, 'medicals': medicals})


# login view
class UserLoginView(View):

    def post(self, request):

        if request.POST:
            cd = request.POST
            username=cd['username']
            password=cd['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_superuser:
                    messages.warning(request, r'You are a superuser...')
                    return HttpResponseRedirect('/account/admin-site/')
                elif user.is_staff:
                    messages.warning(request, r'You have permission as staff status...')
                    return HttpResponseRedirect('/account/admin-site/')
                elif user.is_active:
                    staff = get_object_or_404(Profile, user=user)

                    if staff.group == ProfessionalGroup.objects.get(slug='medical-staff'):
                        messages.warning(request, r'Good morning dr {}'.format(user.get_full_name()))
                        return HttpResponseRedirect(reverse('medical_advice:advice', kwargs={'username': username}))
                    elif staff.group == ProfessionalGroup.objects.get(slug='registration-department-staff'):
                        return HttpResponseRedirect('/registration/register/')
                    else:
                        messages.warning(request, r'Caution! You have not permission to use to this application...')

            elif username or password:
                messages.warning(request, r'Caution! Username or password are incorrectt...')

            else:
                messages.warning(request, r'Please complete both fields...')

        return render(request, 'mainboard/index.html',)


# password change view
class PasswordChange(View):

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'account/password_change.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = PasswordChangeForm(user=request.user, data=request.POST)

                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.warning(request, r'Successful. User {} has changed password'.format(request.user))
                else:
                    messages.warning(request, r'Error. User {} has not changed password'.format(request.user))
            else:
                form = PasswordChangeForm(user=request.user)
            return render(request, 'account/password_change.html', {'form': form})


# exit application view
class ExitView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            backup()
        return HttpResponseRedirect(r'https://www.google.pl/')
