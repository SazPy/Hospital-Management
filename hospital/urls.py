from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name=''),
    path('home', views.home_view, name='home'),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),

    # Admin URLs
    path('admin-rooms/', views.admin_rooms_view, name='admin-rooms'),
    path('admin-add-room/', views.admin_add_room_view, name='admin-add-room'),
    path('admin-room-requests/', views.admin_room_requests_view, name='admin-room-requests'),
    path('admin-approve-room-request/<int:pk>/', views.admin_approve_room_request, name='admin-approve-room-request'),
    path('admin-deny-room-request/<int:pk>/', views.admin_deny_room_request, name='admin-deny-room-request'),

    # Admin Appointment URLs
    path('admin-appointment/', views.admin_appointment_views, name='admin-appointment'),
    path('admin-add-appointment/', views.admin_appointment_views, {'action': 'add'}, name='admin-add-appointment'),
    path('admin-view-appointment/', views.admin_appointment_views, {'action': 'view'}, name='admin-view-appointment'),
    path('admin-approve-appointment/', views.admin_appointment_views, {'action': 'approve'}, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>/', views.admin_appointment_views, {'action': 'approve-appointment'}, name='approve-appointment'),
    path('reject-appointment/<int:pk>/', views.admin_appointment_views, {'action': 'reject'}, name='reject-appointment'),

    # Doctor URLs
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('doctor-appointment', views.doctor_appointment_views, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_appointment_views, {'action': 'view'}, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment'),
    path('doctor-delete-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment-pk'),
    path('doctor-pending-appointments', views.doctor_appointment_views, {'action': 'pending'}, name='doctor-pending-appointments'),
    path('doctor-approve-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'approve'}, name='doctor-approve-appointment'),
    path('doctor-reject-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'reject'}, name='doctor-reject-appointment'),
    
    # Doctor Room Management URLs
    path('doctor-request-room/', views.doctor_request_room, name='doctor-request-room'),
    path('doctor-room-requests/', views.doctor_room_requests_view, name='doctor-room-requests'),
    
    # Discharge URLs
    path('admin-discharge-patient', views.admin_patient_views, {'action': 'discharge'}, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.handle_discharge_patient, name='discharge-patient'),
    path('download-pdf/<int:pk>/', views.download_pdf_view, name='download-pdf'),

    # Doctor Patient Management URLs
    path('doctor-patient/', views.doctor_patient_views, name='doctor-patient'),
    path('doctor-view-patient/', views.doctor_patient_views, name='doctor-view-patient'),
    path('doctor-view-patient/search/', views.doctor_patient_views, {'action': 'search'}, name='doctor-search-patient'),
    path('doctor-view-patient/discharged/', views.doctor_patient_views, {'action': 'discharged'}, name='doctor-discharged-patients'),
    path('doctor-update-record/<int:pk>/', views.doctor_patient_views, {'action': 'update_record'}, name='doctor-update-record'),
] 