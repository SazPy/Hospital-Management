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

    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
    path('privacy-policy', views.privacy_policy_view, name='privacy-policy'),
    path('terms', views.terms_view, name='terms'),

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
    
    path('admin-profile', views.admin_profile_view, name='admin-profile'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-messages', views.admin_messages_view, name='admin-messages'),
    path('admin-mark-message-read/<int:pk>/', views.admin_mark_message_read, name='admin-mark-message-read'),
    path('admin-delete-message/<int:pk>/', views.admin_delete_message, name='admin-delete-message'),

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
    path('admin-approve-appointment', views.admin_appointment_views, {'action': 'approve'}, name='admin-approve-appointment'),
    path('admin-approve-appointment/<int:pk>', views.admin_appointment_views, {'action': 'approve-appointment'}, name='admin-approve-appointment'),
    path('admin-reject-appointment/<int:pk>', views.admin_appointment_views, {'action': 'reject'}, name='admin-reject-appointment'),
    path('admin-appointment-details/<int:pk>', views.admin_appointment_views, {'action': 'details'}, name='admin-appointment-details'),
    path('admin-delete-appointment/<int:pk>', views.admin_appointment_views, {'action': 'delete'}, name='admin-delete-appointment'),

    # Room Management URLs
    path('admin-add-room/', views.admin_add_room_view, name='admin-add-room'),
    path('admin-rooms/', views.admin_rooms_view, name='admin-rooms'),
    path('admin-room/<int:room_id>/edit/', views.admin_edit_room_view, name='admin-edit-room'),
    path('admin-room/<int:room_id>/delete/', views.admin_delete_room_view, name='admin-delete-room'),
    path('admin-room/<int:patient_id>/assign/', views.admin_room_management, {'action': 'assign'}, name='admin-assign-room'),
    path('admin-room/<int:patient_id>/change/', views.admin_room_management, {'action': 'change'}, name='admin-change-room'),
    path('admin-room/<int:patient_id>/discharge/', views.admin_room_management, {'action': 'discharge'}, name='admin-discharge-from-room'),
    path('admin-room/<int:room_id>/details/', views.admin_room_management, {'action': 'details'}, name='admin-room-details'),
    path('admin-room-requests/', views.admin_room_requests_view, name='admin-room-requests'),
    path('admin-approve-room-request/<int:pk>/', views.admin_approve_room_request, name='admin-approve-room-request'),
    path('admin-deny-room-request/<int:pk>/', views.admin_deny_room_request, name='admin-deny-room-request'),

    # Doctor URLs - using consolidated view
    path('doctor-profile', views.doctor_profile_view, name='doctor-profile'),
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),

    # Patient URLs
    path('patient-profile', views.patient_profile_view, name='patient-profile'),
    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
]

# ---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path('search', views.doctor_patient_views, {'action': 'search'}, name='search'),

    path('doctor-patient', views.doctor_patient_views, {'action': 'view'}, name='doctor-patient'),
    path('doctor-patient/<int:pk>/', views.doctor_patient_views, {'action': 'detail'}, name='doctor-view-patient-detail'),
    path('doctor-view-discharge-patient', views.doctor_patient_views, {'action': 'discharged'},
         name='doctor-view-discharge-patient'),
    path('doctor-update-record/<int:pk>/', views.doctor_patient_views, {'action': 'update_record'}, name='doctor-update-record'),

    path('doctor-appointment', views.doctor_appointment_views, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_appointment_views, {'action': 'view'}, name='doctor-view-appointment'),
    path('doctor-pending-appointments', views.doctor_appointment_views, {'action': 'pending'}, name='doctor-pending-appointments'),
    path('doctor-approve-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'approve'}, name='doctor-approve-appointment'),
    path('doctor-reject-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'reject'}, name='doctor-reject-appointment'),
    path('doctor-delete-appointment', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment'),
    path('doctor-delete-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment-pk'),

    # Doctor Room Management URLs
    path('doctor-request-room/', views.doctor_request_room, name='doctor-request-room'),
    path('doctor-room-requests/', views.doctor_room_requests_view, name='doctor-room-requests'),
]

# ---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path('patient-appointment', views.patient_appointment_views, name='patient-appointment'),
    path('patient-book-appointment', views.patient_appointment_views, {'action': 'book'},
         name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_appointment_views, {'action': 'view'},
         name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_appointment_views, {'action': 'view-doctors'},
         name='patient-view-doctor'),
    path('patient-doctor-specialisation', views.patient_appointment_views, {'action': 'view-doctors', 'view_type': 'specialisation'},
         name='patient-doctor-specialisation'),
    path('searchdoctor', views.patient_appointment_views, {'action': 'search-doctors'}, name='searchdoctor'),
    path('patient-discharge', views.patient_appointment_views, {'action': 'discharge'}, name='patient-discharge'),
]

# Add static and media file serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
