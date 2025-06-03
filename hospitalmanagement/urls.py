from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

# -------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),

    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'), name='logout'),

    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),

    # Doctor URLs - using consolidated view
    path('admin-doctor', views.admin_doctor_views, name='admin-doctor'),
    path('admin-view-doctor', views.admin_doctor_views, {'action': 'view'}, name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.admin_doctor_views, {'action': 'delete'},
         name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.admin_doctor_views, {'action': 'update'}, name='update-doctor'),
    path('admin-add-doctor', views.admin_doctor_views, {'action': 'add'}, name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_doctor_views, {'action': 'approve'}, name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.admin_doctor_views, {'action': 'approve-doctor'}, name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.admin_doctor_views, {'action': 'reject'}, name='reject-doctor'),
    path('admin-view-doctor-specialisation', views.admin_doctor_views, {'action': 'specialisation'},
         name='admin-view-doctor-specialisation'),

    # Patient URLs - using consolidated view
    path('admin-patient', views.admin_patient_views, name='admin-patient'),
    path('admin-view-patient', views.admin_patient_views, {'action': 'view'}, name='admin-view-patient'),
    path('admin-view-patient/<int:pk>/', views.admin_patient_views, {'action': 'view-detail'}, name='admin-view-patient-detail'),
    path('delete-patient-from-hospital/<int:pk>', views.admin_patient_views, {'action': 'delete'},
         name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.admin_patient_views, {'action': 'update'}, name='update-patient'),
    path('admin-add-patient', views.admin_patient_views, {'action': 'add'}, name='admin-add-patient'),
    path('admin-approve-patient', views.admin_patient_views, {'action': 'approve'}, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.admin_patient_views, {'action': 'approve-patient'}, name='approve-patient'),
    path('reject-patient/<int:pk>', views.admin_patient_views, {'action': 'reject'}, name='reject-patient'),
    path('admin-discharge-patient', views.admin_patient_views, {'action': 'discharge'}, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.admin_patient_views, {'action': 'discharge-patient'},
         name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),

    # Appointment URLs - using consolidated view
    path('admin-appointment', views.admin_appointment_views, name='admin-appointment'),
    path('admin-view-appointment', views.admin_appointment_views, {'action': 'view'}, name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_appointment_views, {'action': 'add'}, name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_appointment_views, {'action': 'approve'},
         name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.admin_appointment_views, {'action': 'approve-appointment'},
         name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.admin_appointment_views, {'action': 'reject'}, name='reject-appointment'),

    # Room Management URLs
    path('admin-rooms/', views.admin_room_management, {'action': 'view'}, name='admin-rooms'),
    path('admin-add-room/', views.admin_room_management, {'action': 'add'}, name='admin-add-room'),
    path('admin-room/<int:patient_id>/assign/', views.admin_room_management, {'action': 'assign'}, name='admin-assign-room'),
    path('admin-room/<int:patient_id>/change/', views.admin_room_management, {'action': 'change'}, name='admin-change-room'),
    path('admin-room/<int:patient_id>/discharge/', views.admin_room_management, {'action': 'discharge'}, name='admin-discharge-from-room'),
    path('admin-room/<int:room_id>/details/', views.admin_room_management, {'action': 'details'}, name='admin-room-details'),
]

# ---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('search', views.doctor_patient_views, {'action': 'search'}, name='search'),

    path('doctor-patient', views.doctor_patient_views, name='doctor-patient'),
    path('doctor-view-patient', views.doctor_patient_views, {'action': 'view'}, name='doctor-view-patient'),
    path('doctor-view-discharge-patient', views.doctor_patient_views, {'action': 'discharged'},
         name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_views, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_appointment_views, {'action': 'view'}, name='doctor-view-appointment'),
    path('doctor-pending-appointments', views.doctor_appointment_views, {'action': 'pending'}, name='doctor-pending-appointments'),
    path('doctor-approve-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'approve'}, name='doctor-approve-appointment'),
    path('doctor-reject-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'reject'}, name='doctor-reject-appointment'),
    path('doctor-delete-appointment', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment'),
    path('doctor-delete-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment-pk'),
]

# ---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_views, name='patient-appointment'),
    path('patient-book-appointment', views.patient_appointment_views, {'action': 'book'},
         name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_appointment_views, {'action': 'view'},
         name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_appointment_views, {'action': 'view-doctors'},
         name='patient-view-doctor'),
    path('searchdoctor', views.patient_appointment_views, {'action': 'search-doctors'}, name='searchdoctor'),
    path('patient-discharge', views.patient_appointment_views, {'action': 'discharge'}, name='patient-discharge'),
]

# Add static and media file serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
