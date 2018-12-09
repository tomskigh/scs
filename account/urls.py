# django library
from django.urls import path

# my views
from account import views


urlpatterns = [

    # admin view
    path('admin-site/', views.AdminView.as_view(), name='admin_site'),

    # create user view
    path('create-user/', views.CreateNewUser.as_view(), name='create_user'),

    # change medical user data
    path('medical-user-data-change/<int:md_id>/', views.MedicalUserDataChange.as_view(), name='medical_user_data_change'),

    # login view
    path('login/', views.UserLoginView.as_view(), name='login'),

    # password change view
    path('password-change/', views.PasswordChange.as_view(), name='password_change'),

    # exit
    path('exit/', views.ExitView.as_view(), name='exit'),

]
