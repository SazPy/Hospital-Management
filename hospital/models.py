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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(null=True)
    appointmentTime = models.TimeField(null=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)  # False for pending, True for approved
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)  # For office visits
    is_admission = models.BooleanField(default=False)  # To distinguish between regular appointments and stays
    admission_days = models.IntegerField(default=0)  # For tracking length of stay
    
    class Meta:
        ordering = ['-appointmentDate', '-appointmentTime']

    def save(self, *args, **kwargs):
        if not self.patientName and self.patient:
            self.patientName = self.patient.get_name
        if not self.doctorName and self.doctor:
            self.doctorName = self.doctor.get_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patientName} - Dr. {self.doctorName} on {self.appointmentDate}"


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


class Room(models.Model):
    ROOM_TYPES = [
        ('WARD', 'Ward'),
        ('PRIVATE', 'Private Room'),
        ('ICU', 'ICU'),
        ('OFFICE', 'Doctor Office'),
    ]
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField(default=1)
    is_occupied = models.BooleanField(default=False)
    current_patient = models.IntegerField(null=True, blank=True)  # Patient ID if occupied
    assigned_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)  # For offices
    description = models.TextField(blank=True)
    floor = models.CharField(max_length=10, default='1st')

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.room_number}"

    class Meta:
        ordering = ['room_number']

class RoomRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='room_requests', null=True, blank=True)
    requested_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='requested_room')
    assigned_room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_room')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)
    response_note = models.TextField(blank=True)
    expected_duration = models.PositiveIntegerField(help_text='Expected stay duration in days', default=1)
    
    def __str__(self):
        return f"Room request for {self.patient} by Dr. {self.doctor}"

class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patient_records')
    date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    images = models.ImageField(upload_to='patient_records/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Record for {self.patient.get_name} by Dr. {self.doctor.get_name} on {self.date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"