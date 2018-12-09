"""my_thesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

# django library
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# my views
from mainboard import views


urlpatterns = [

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('index/', views.IndexView.as_view(), name='index'),
    path('medicals-presence/', views.MedicalsPresenceView.as_view(), name='medicals_presence'),
    path('account/', include('account.urls')),
    path('registration/', include('registration.urls', namespace='registrations')),
    path('medical-visit/', include('medical_visit.urls', namespace='medical_visit')),
    path('medical-advice/', include('medical_advice.urls', namespace='medical_advice')),

    # password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'account/password_reset_form.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'account/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html'), name = 'password_reset_complete'),
]
