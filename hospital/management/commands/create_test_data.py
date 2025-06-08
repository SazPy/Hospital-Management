from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from hospital.models import Doctor, Patient, Appointment, Room
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creates test data for the hospital management system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create groups if they don't exist
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        patient_group, _ = Group.objects.get_or_create(name='Patient')

        # Create test doctors
        doctors_data = [
            {
                'username': 'dr.smith',
                'email': 'dr.smith@example.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'department': 'Cardiologist',
                'mobile': '1234567890',
                'address': '123 Medical Center Dr',
                'status': True
            },
            {
                'username': 'dr.jones',
                'email': 'dr.jones@example.com',
                'first_name': 'Emily',
                'last_name': 'Jones',
                'department': 'Dermatologist',
                'mobile': '0987654321',
                'address': '456 Hospital Ave',
                'status': True
            },
            {
                'username': 'dr.wilson',
                'email': 'dr.wilson@example.com',
                'first_name': 'Robert',
                'last_name': 'Wilson',
                'department': 'Neurologist',
                'mobile': '5432167890',
                'address': '789 Clinic St',
                'status': True
            }
        ]

        created_doctors = []
        for doc_data in doctors_data:
            # Create User account if it doesn't exist
            user, created = User.objects.get_or_create(
                username=doc_data['username'],
                defaults={
                    'email': doc_data['email'],
                    'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name']
                }
            )
            if created:
                user.set_password('test123')
                user.save()
            user.groups.add(doctor_group)

            # Create Doctor profile
            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'mobile': doc_data['mobile'],
                    'department': doc_data['department'],
                    'status': doc_data['status'],
                    'address': doc_data['address']
                }
            )
            created_doctors.append(doctor)
            self.stdout.write(f'{"Created" if created else "Found"} doctor: {user.get_full_name()}')

        # Create test patients
        patients_data = [
            {
                'username': 'patient1',
                'email': 'patient1@example.com',
                'first_name': 'Alice',
                'last_name': 'Brown',
                'symptoms': 'Chest pain, shortness of breath',
                'mobile': '1112223333',
                'address': '321 Patient Lane'
            },
            {
                'username': 'patient2',
                'email': 'patient2@example.com',
                'first_name': 'Bob',
                'last_name': 'Taylor',
                'symptoms': 'Skin rash, itching',
                'mobile': '4445556666',
                'address': '654 Recovery Road'
            },
            {
                'username': 'patient3',
                'email': 'patient3@example.com',
                'first_name': 'Carol',
                'last_name': 'White',
                'symptoms': 'Headache, dizziness',
                'mobile': '7778889999',
                'address': '987 Wellness Way'
            }
        ]

        created_patients = []
        for patient_data in patients_data:
            # Create User account if it doesn't exist
            user, created = User.objects.get_or_create(
                username=patient_data['username'],
                defaults={
                    'email': patient_data['email'],
                    'first_name': patient_data['first_name'],
                    'last_name': patient_data['last_name']
                }
            )
            if created:
                user.set_password('test123')
                user.save()
            user.groups.add(patient_group)

            # Create Patient profile
            patient, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    'mobile': patient_data['mobile'],
                    'symptoms': patient_data['symptoms'],
                    'status': True,
                    'address': patient_data['address']
                }
            )
            created_patients.append(patient)
            self.stdout.write(f'{"Created" if created else "Found"} patient: {user.get_full_name()}')

        # Create test rooms
        room_types = ['Ward', 'Private', 'ICU']
        floors = [1, 2, 3]
        wings = ['A', 'B', 'C']
        
        for i in range(10):
            room, created = Room.objects.get_or_create(
                room_number=f"{random.choice(floors)}{random.choice(wings)}{str(i+1).zfill(2)}",
                defaults={
                    'room_type': random.choice(room_types),
                    'capacity': random.choice([1, 2, 4]),
                    'floor': random.choice(floors),
                    'wing': random.choice(wings),
                    'is_occupied': random.choice([True, False]),
                    'maintenance_required': random.choice([True, False])
                }
            )
            self.stdout.write(f'{"Created" if created else "Found"} room: {room.room_number}')

        # Create test appointments
        current_time = timezone.now()
        appointment_statuses = ['Pending', 'Confirmed', 'Completed']
        
        for i in range(5):
            appointment_time = current_time + timedelta(days=i, hours=random.randint(1, 8))
            doctor = random.choice(created_doctors)
            patient = random.choice(created_patients)
            
            appointment, created = Appointment.objects.get_or_create(
                doctor=doctor,
                patient=patient,
                appointmentDate=appointment_time.date(),
                appointmentTime=appointment_time.time(),
                defaults={
                    'description': f"Follow-up appointment for {patient.symptoms}",
                    'status': True if random.choice(['Confirmed', 'Completed']) == 'Confirmed' else False,
                    'doctorName': f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
                    'patientName': f"{patient.user.first_name} {patient.user.last_name}"
                }
            )
            self.stdout.write(f'{"Created" if created else "Found"} appointment: {appointment.patientName} with {appointment.doctorName}')

        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user: admin (password: admin123)')
        else:
            self.stdout.write('Found existing admin user')

        self.stdout.write(self.style.SUCCESS('Successfully created test data')) 