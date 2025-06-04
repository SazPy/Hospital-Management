from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Room
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'capacity', 'is_occupied', 'floor', 'wing', 'maintenance_required')
    list_filter = ('room_type', 'is_occupied', 'maintenance_required')
    search_fields = ('room_number', 'wing')
admin.site.register(Room, RoomAdmin)
