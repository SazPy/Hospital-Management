from django.urls import path
from . import views

urlpatterns = [
    # Doctor related urls
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('doctor-appointment', views.doctor_appointment_views, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_appointment_views, {'action': 'view'}, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment'),
    path('doctor-delete-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'delete'}, name='doctor-delete-appointment-pk'),
    path('doctor-pending-appointments', views.doctor_appointment_views, {'action': 'pending'}, name='doctor-pending-appointments'),
    path('doctor-approve-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'approve'}, name='doctor-approve-appointment'),
    path('doctor-reject-appointment/<int:pk>', views.doctor_appointment_views, {'action': 'reject'}, name='doctor-reject-appointment'),
] 