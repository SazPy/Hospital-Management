from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, Room, RoomRequest  # Direct model imports help with IDEs/autocomplete
from datetime import date


# ==============================
# Base User Form
# ==============================
class BaseUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})


# ==============================
# Admin Signup Form
# ==============================
class AdminSignupForm(BaseUserForm):
    pass


# ==============================
# Doctor Forms
# ==============================
class DoctorUserForm(BaseUserForm):
    pass


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'address', 'mobile', 'profile_pic']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ==============================
# Patient Forms
# ==============================
class PatientUserForm(BaseUserForm):
    pass


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'profile_pic']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ==============================
# Appointment Forms
# ==============================
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointmentDate', 'appointmentTime', 'description', 'status']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'appointmentDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointmentTime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(status=True)
        self.fields['patient'].queryset = Patient.objects.filter(status=True)


class PatientAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True),
        empty_label="Select Doctor",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointmentDate', 'appointmentTime', 'description']
        widgets = {
            'appointmentDate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().isoformat()
            }),
            'appointmentTime': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Please describe your symptoms or reason for visit'
            }),
        }


# ==============================
# Contact Us Form
# ==============================
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'capacity', 'floor', 'description']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['assigned_room', 'response_note']
        widgets = {
            'assigned_room': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'response_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes about the room assignment...',
                'required': True,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.requested_room:
            print(f"Debug - Form init - Instance: {self.instance}")
            print(f"Debug - Form init - Requested room type: {self.instance.requested_room.room_type}")
            
            # Only show available rooms of the requested type
            available_rooms = Room.objects.filter(
                room_type=self.instance.requested_room.room_type,
                is_occupied=False
            )
            print(f"Debug - Form init - Available rooms: {list(available_rooms.values_list('room_number', flat=True))}")
            
            self.fields['assigned_room'].queryset = available_rooms
            self.fields['assigned_room'].empty_label = None  # Remove empty choice
            self.fields['assigned_room'].label = f"Assign {self.instance.requested_room.get_room_type_display()} Room"
            
            # Add help text to show available rooms
            room_count = available_rooms.count()
            self.fields['assigned_room'].help_text = f'{room_count} available {self.instance.requested_room.get_room_type_display()} rooms'
            
            print(f"Debug - Form init - Final queryset: {list(self.fields['assigned_room'].queryset)}")
        else:
            print("Debug - Form init - No instance or no requested room")
