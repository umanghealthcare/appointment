from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('header/',views.header,name='header'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('otp/',views.otp,name='otp'),
    path('change_pass/',views.change_pass,name='change_pass'),
    path('gallery/',views.gallery,name='gallery'),
    path('contact/',views.contact,name='contact'),
    path('blood_bank/',views.blood_bank,name='blood_bank'),
    path('doctor_index/',views.doctor_index,name='doctor_index'),
    path('doctor_profile/',views.doctor_profile,name='doctor_profile'),
    path('doctor_pic_update/',views.doctor_pic_update,name='doctor_pic_update'),
    path('doctor_change_password/',views.doctor_change_password,name='doctor_change_password'),
    path('doctor_profile_update/',views.doctor_profile_update,name='doctor_profile_update'),
    path('ajax/validate_email/',views.validate_signup,name='validate_email'),
    path('doctor/',views.doctor,name='doctor'),
    path('doctor_appointment/<int:pk>',views.doctor_appointment,name='doctor_appointment'),
    path('book_appointment/<int:pk>',views.book_doctor_appointment,name='book_appointment'),
    path('myappointment/',views.myappointment,name='myappointment'),
    path('patient_cancel_appointment/<int:pk>/',views.patient_cancel_appointment,name='patient_cancel_appointment'),
    path('doctor_appointment_schedule/',views.doctor_appointment_schedule,name='doctor_appointment_schedule'),
    path('doctor_cancel_appointment/<int:pk>/',views.doctor_cancel_appointment,name='doctor_cancel_appointment'),
    path('doctor_accepted_appointment/<int:pk>/',views.doctor_accepted_appointment,name='doctor_accepted_appointment'),
    path('pay/<int:pk>/',views.initiate_payment, name='pay'),
    path('callback/',views.callback, name='callback'),
    path('health_profile/',views.health_profile,name='health_profile'),
    path('patient_health_report/<int:pk>/',views.patient_health_report,name='patient_health_report'),
    path('prescription_by_doctor/<int:pk>/',views.prescription_by_doctor,name='prescription_by_doctor'),
    path('prescription_by_doctor_patient/<int:pk>/',views.prescription_by_doctor_patient,name='prescription_by_doctor_patient'),
    path('website/',views.website,name='website'),
]