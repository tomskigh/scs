# django library
from django.urls import path

# my views
from registration import views

app_name='registartion'

urlpatterns = [
    path('register/', views.PatientListView.as_view(), name='register'),
    path('send-email/', views.SendEmailView.as_view(), name='send_email'),
    path('add-patient/', views.PatientAddView.as_view(), name='add_patient'),
    path('patient/<int:patient_id>/', views.PatientDetailView.as_view(), name='register_patient_detail'),
    path('patient/change-data/<int:patient_id>/', views.patient_data_change, name='change_data_patient'),
    path('medical-presence/<slug:spec>/', views.MedicalPresentView.as_view(), name='medical_presence'),
]
