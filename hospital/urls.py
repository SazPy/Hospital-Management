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
] 