# django library
from django.urls import path

# my views
from medical_advice import views

app_name='medical_advice'

urlpatterns = [
    path('advice/<username>/', views.MedicalAdviceView.as_view(), name='advice'),
    path('advice-description/<username>/<int:patient_id>/', views.AdviceDescriptionView.as_view(), name='advice_description'),
    path('medical-prescription/<username>/<int:patient_id>/', views.MedicalPrescriptionDetailView.as_view(), name='medical_prescription_detail'),
    path('medical-prescription/email/pdf/<username>/<int:patient_id>/', views.MedicalPrescriptionSender.as_view(), name='medical_prescription_pdf'),
    ]
