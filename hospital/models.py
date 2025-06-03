from django.db import models
from django.contrib.auth.models import User


# Add this at the top of your models (before any model classes)
class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


departments = [('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')]


class Doctor(BaseModel):  # Changed from models.Model to BaseModel
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


class Patient(BaseModel):  # Changed from models.Model to BaseModel
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.symptoms + ")"


class Appointment(BaseModel):  # Changed from models.Model to BaseModel
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)


class PatientDischargeDetails(BaseModel):  # Changed from models.Model to BaseModel
    patientId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    assignedDoctorName = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)
    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)
    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)


class Room(BaseModel):  # Changed from models.Model to BaseModel
    ROOM_TYPES = [
        ('General', 'General Ward'),
        ('Private', 'Private Room'),
        ('ICU', 'Intensive Care Unit'),
        ('CCU', 'Cardiac Care Unit'),
        ('Pediatric', 'Pediatric Ward'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='General')
    capacity = models.PositiveIntegerField(default=1)
    is_occupied = models.BooleanField(default=False)
    current_patient = models.PositiveIntegerField(null=True, blank=True)
    floor = models.PositiveIntegerField(default=1)
    wing = models.CharField(max_length=10, blank=True, null=True)
    maintenance_required = models.BooleanField(default=False)

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Room {self.room_number} ({self.room_type}) - {status}"