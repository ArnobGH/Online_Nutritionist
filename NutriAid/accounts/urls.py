from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),

    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('nutritionist-register', nutritionist_register_view, name='nutritionist-register'),
    path('patient-register', patient_register_view, name='patient-register'),

    path('nutritionist-profile/<str:pk>', nutritionist_profile, name='nutritionist-profile'),
    path('patient-profile/<str:pk>', patient_profile, name='patient-profile'),
    path('nutritionist-edit-profile', nutritionist_edit_profile, name='nutritionist-edit-profile'),
    path('patient-edit-profile', patient_edit_profile, name='patient-edit-profile'),

    path('calc/',calculate,name='calc'),
    path('bmi/', biPage,name="bmi"),
    path('result/', bmiresult,name="result"),
    path('bmr/', brPage,name="bmr"),
    path('mbmrres/', mbmrresult,name="mbmrres"),
    path('fbmrres/', fbmrresult,name="fbmrres"),
    path('malebmr/', malebmr,name="malebmr"),
    path('femalebmr/', femalebmr,name="femalebmr"),


    path('contact', contact_view, name='contact'),

    path('nutritionists', nutritionists_list, name='nutritionists'),
    path('appointments/patient-appointments', patient_appointment_home_view, name='patient-appointment-home'),
    path('appointments/nutritionist-appointments', nutritionist_appointment_home_view,
         name='nutritionist-appointment-home'),
    path('appointments/details/<str:pk>', appointment_detail_view, name='appointment-details'),
    path('appointments/make-appointment/<int:pk>', make_appointment_view, name='make-appointment'),
    path('appointments/update/<int:pk>', doctor_appointment_update_view, name='nutritionist-appointment-update'),
    path('update/<int:pk>', patient_appointment_update_view, name='patient-appointment-update'),
    path('appointments/delete/<int:pk>', appointment_delete_view, name='appointment-delete'),
    path('appointments/reject/<int:pk>', appointment_reject_view, name='appointment-reject'),

    path('resetpass/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('resetpass_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('resetpass_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
