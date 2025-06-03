from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment  # Direct model imports help with IDEs/autocomplete
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
    assignedDoctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True),
        empty_label="Select Doctor",
        to_field_name="user_id",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'symptoms', 'profile_pic']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
