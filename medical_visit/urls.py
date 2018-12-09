# django library
from django.urls import path

# my views
from medical_visit import views


app_name='medical_visit'

urlpatterns = [
    path('medical-add/', views.MedicalAddView.as_view(), name='medical_add_view'),
    path('medical-staff/<int:patient_id>/<slug:spec>/', views.MedicalView.as_view(), name='medical_staff_view'),
    path('visit-date-register/<int:patient_id>/<slug:spec>/<int:medical_id>/', views.VisitDateView.as_view(), name='visit_date_register'),
    path('visit-hour-register/<int:patient_id>/<slug:spec>/<int:medical_id>/<date_of_visit>/', views.VisitHourView.as_view(), name='visit_hour_register'),
    path('visit-delete/<int:patient_id>/', views.VisitDeleteView.as_view(), name='visit_delete'),
    ]
