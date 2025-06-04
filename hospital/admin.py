from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Room,RoomRequest
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
    list_display = ['room_number', 'room_type', 'capacity', 'is_occupied', 'floor']
    list_filter = ['room_type', 'is_occupied']
    search_fields = ['room_number', 'description']
admin.site.register(Room, RoomAdmin)

admin.site.register(RoomRequest)
