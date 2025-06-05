from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, Room, RoomRequest, PatientRecord, ContactMessage  # Direct model imports help with IDEs/autocomplete
from datetime import date


# ==============================
# Base User Forms
# ==============================
class BaseUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class BaseUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password (optional)'}),
        required=False,
        help_text="Leave blank to keep current password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        required=False,
        help_text="Enter the same password as above to confirm"
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't validate username uniqueness for the current user
        if self.instance:
            self.fields['username'].validators = [
                v for v in self.fields['username'].validators 
                if not hasattr(v, 'code') or v.code != 'unique' 
                or (hasattr(v, 'code') and v.code == 'unique' and v.queryset.exclude(pk=self.instance.pk))
            ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if bool(password1) != bool(password2):
            raise forms.ValidationError("Please fill in both password fields or leave them both empty.")
        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ==============================
# Admin Forms
# ==============================
class AdminSignupForm(BaseUserForm):
    pass


# ==============================
# Doctor Forms
# ==============================
class DoctorUserForm(BaseUserForm):
    pass

class DoctorUserUpdateForm(BaseUserUpdateForm):
    pass

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'address', 'mobile', 'profile_pic']
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address',
                'rows': 3,
                'required': True
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number',
                'pattern': '[0-9]{10}',
                'title': 'Please enter a valid 10-digit mobile number',
                'required': True
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number should contain only digits")
        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number should be 10 digits long")
        return mobile


# ==============================
# Patient Forms
# ==============================
class PatientUserForm(BaseUserForm):
    pass

class PatientUserUpdateForm(BaseUserUpdateForm):
    pass

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'symptoms', 'profile_pic']
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address',
                'rows': 3,
                'required': True
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number',
                'pattern': '[0-9]{10}',
                'title': 'Please enter a valid 10-digit mobile number',
                'required': True
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the symptoms',
                'rows': 3,
                'required': True
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number should contain only digits")
        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number should be 10 digits long")
        return mobile


# ==============================
# Appointment Forms
# ==============================
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointmentDate', 'appointmentTime', 'description']
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'placeholder': 'Select Doctor'
            }),
            'patient': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'placeholder': 'Select Patient'
            }),
            'appointmentDate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'appointmentTime': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter appointment details...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active doctors and patients
        self.fields['doctor'].queryset = Doctor.objects.filter(status=True).order_by('department', 'user__first_name')
        self.fields['patient'].queryset = Patient.objects.filter(status=True).order_by('user__first_name')
        
        # Customize labels
        self.fields['doctor'].label = "Select Doctor"
        self.fields['patient'].label = "Select Patient"
        
        # Add help text
        self.fields['doctor'].help_text = "Choose from available doctors"
        self.fields['patient'].help_text = "Choose from registered patients"
        
        # Override the default __str__ display in dropdowns
        self.fields['doctor'].label_from_instance = lambda obj: f"Dr. {obj.get_name} ({obj.department})"
        self.fields['patient'].label_from_instance = lambda obj: f"{obj.get_name} (ID: {obj.id})"


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
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room number',
                'required': True
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'required': True
            }),
            'floor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter floor number/name',
                'value': '1st'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter room description (optional)'
            })
        }
        labels = {
            'room_number': 'Room Number',
            'room_type': 'Room Type',
            'capacity': 'Room Capacity',
            'floor': 'Floor',
            'description': 'Description'
        }
        help_texts = {
            'room_number': 'Unique identifier for the room',
            'room_type': 'Type of room (Ward, Private, ICU, or Office)',
            'capacity': 'Maximum number of patients',
            'floor': 'Floor where the room is located',
            'description': 'Additional details about the room'
        }

    def clean_room_number(self):
        room_number = self.cleaned_data.get('room_number')
        if Room.objects.filter(room_number=room_number).exists():
            raise forms.ValidationError('A room with this number already exists')
        return room_number

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 1:
            raise forms.ValidationError('Capacity must be at least 1')
        return capacity


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


class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['diagnosis', 'prescription', 'notes', 'images']
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter diagnosis details'
            }),
            'prescription': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter prescription details'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any additional notes'
            }),
            'images': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
