# -*- coding: utf-8 -*-
"""
Hospital Management – Django views
Updated: 2025-06-02

• Consolidated imports & helpers
• Fixed signup flow, room-management URLs, and CRUD logic
• All template `{% url %}` names now resolve
"""

from datetime import date, timedelta
from django.utils import timezone
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from . import forms, models

# --------------------------------------------------------------------------- #
# Constants & role helpers
# --------------------------------------------------------------------------- #
ADMIN_GROUP = "ADMIN"
DOCTOR_GROUP = "DOCTOR"
PATIENT_GROUP = "PATIENT"


def is_admin(user):   return user.groups.filter(name=ADMIN_GROUP).exists()
def is_doctor(user):  return user.groups.filter(name=DOCTOR_GROUP).exists()
def is_patient(user): return user.groups.filter(name=PATIENT_GROUP).exists()

# --------------------------------------------------------------------------- #
# Utility: render template ➜ PDF
# --------------------------------------------------------------------------- #
def render_to_pdf(template_src: str, context: dict) -> HttpResponse:
    html = get_template(template_src).render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        resp = HttpResponse(result.getvalue(), content_type="application/pdf")
        resp["Content-Disposition"] = (
            f'attachment; filename="discharge_report_{context.get("patientId","")}.pdf"'
        )
        return resp
    return HttpResponse("Error generating PDF", status=500)

# --------------------------------------------------------------------------- #
# Public / landing views
# --------------------------------------------------------------------------- #
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/index.html")


def role_based_click_view(request, role: str):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, f"hospital/{role}click.html")


adminclick_view   = lambda req: role_based_click_view(req, "admin")   # noqa: E731
doctorclick_view  = lambda req: role_based_click_view(req, "doctor")  # noqa: E731
patientclick_view = lambda req: role_based_click_view(req, "patient") # noqa: E731

# --------------------------------------------------------------------------- #
# Signup helper + thin wrappers
# --------------------------------------------------------------------------- #
def _collect_errors(request, user_form, profile_form):
    for fld, errs in user_form.errors.items():
        for err in errs:
            messages.error(request, f"User {fld}: {err}")
    if profile_form:
        for fld, errs in profile_form.errors.items():
            for err in errs:
                messages.error(request, f"Profile {fld}: {err}")


def signup_view(request, user_form_cls, profile_form_cls, template: str, group_name: str):
    group_name = group_name.upper()

    if request.method == "POST":
        user_form    = user_form_cls(request.POST)
        profile_form = profile_form_cls(request.POST, request.FILES) if profile_form_cls else None
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            try:
                with transaction.atomic():
                    user = user_form.save()
                    if profile_form:
                        profile       = profile_form.save(commit=False)
                        profile.user  = user
                        profile.status = group_name != DOCTOR_GROUP  # doctors need approval
                        profile.save()
                    group, _ = Group.objects.get_or_create(name=group_name)
                    user.groups.add(group)
                messages.success(request, "Registration successful! Please log in.")
                return redirect(reverse(f"{group_name.lower()}login"))
            except Exception as exc:
                messages.error(request, f"Registration error: {exc}")
        else:
            _collect_errors(request, user_form, profile_form)
    else:
        user_form    = user_form_cls()
        profile_form = profile_form_cls() if profile_form_cls else None

    return render(request, template, {
        "userForm": user_form,
        "doctorForm": profile_form,
        "group_name": group_name,
    })


def admin_signup_view(request):
    return signup_view(request, forms.AdminSignupForm, None,
                       "hospital/adminsignup.html", ADMIN_GROUP)


def doctor_signup_view(request):
    return signup_view(request, forms.DoctorUserForm, forms.DoctorForm,
                       "hospital/doctorsignup.html", DOCTOR_GROUP)


def patient_signup_view(request):
    context = {
        'userForm': forms.PatientUserForm(),
        'patientForm': forms.PatientForm(),
        'group_name': PATIENT_GROUP
    }
    
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    patient = patient_form.save(commit=False)
                    patient.user = user
                    patient.status = True
                    patient.save()
                    group, _ = Group.objects.get_or_create(name=PATIENT_GROUP)
                    user.groups.add(group)
                    
                # Auto-login after signup
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, "Registration successful! Welcome to HMS.")
                return redirect('patient-dashboard')
            except Exception as exc:
                messages.error(request, f"Registration error: {exc}")
        else:
            _collect_errors(request, user_form, patient_form)
            context['userForm'] = user_form
            context['patientForm'] = patient_form
    
    return render(request, 'hospital/patientsignup.html', context)

# --------------------------------------------------------------------------- #
# Post-login role router
# --------------------------------------------------------------------------- #
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    if is_doctor(request.user):
        if models.Doctor.objects.filter(user_id=request.user.id, status=True).exists():
            return redirect("doctor-dashboard")
        return render(request, "hospital/doctor_wait_for_approval.html")
    if is_patient(request.user):
        if models.Patient.objects.filter(user_id=request.user.id, status=True).exists():
            return redirect("patient-dashboard")
        return render(request, "hospital/patient_wait_for_approval.html")
    return redirect("home")

# --------------------------------------------------------------------------- #
# ADMIN SECTION
# --------------------------------------------------------------------------- #
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('admin-dashboard')
        
    # Get appointments from the last 7 days and upcoming
    recent_appointments = models.Appointment.objects.filter(
        appointmentDate__gte=timezone.now().date() - timedelta(days=7)
    ).order_by('-appointmentDate', '-appointmentTime')[:5]

    # Get pending room requests
    pending_room_requests = models.RoomRequest.objects.filter(status='PENDING')
    
    # Get all rooms
    rooms = models.Room.objects.all()
    
    # Count rooms by type
    room_counts = {
        'ward_count': rooms.filter(room_type='WARD').count(),
        'private_count': rooms.filter(room_type='PRIVATE').count(),
        'icu_count': rooms.filter(room_type='ICU').count(),
        'office_count': rooms.filter(room_type='OFFICE').count(),
    }

    stats = {
        "doctors": models.Doctor.objects.all().order_by("-id"),
        "patients": models.Patient.objects.all().order_by("-id"),
        "rooms": rooms.order_by("room_number"),
        "doctorcount": models.Doctor.objects.filter(status=True).count(),
        "pendingdoctorcount": models.Doctor.objects.filter(status=False).count(),
        "patientcount": models.Patient.objects.filter(status=True).count(),
        "pendingpatientcount": models.Patient.objects.filter(status=False).count(),
        "appointmentcount": models.Appointment.objects.all().count(),
        "pendingappointmentcount": models.Appointment.objects.filter(status=False).count(),
        "roomcount": rooms.count(),
        "availableroomcount": rooms.filter(is_occupied=False).count(),
        "appointments": recent_appointments,
        "room_requests": pending_room_requests,
        "pending_room_requests": pending_room_requests.count(),
        **room_counts  # Add room counts by type
    }
    return render(request, "hospital/admin_dashboard.html", stats)

# -- Doctor CRUD ------------------------------------------------------------ #
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_views(request, action=None, pk=None):
    # Get base stats that are needed across actions
    doctor_stats = {
        "doctors": models.Doctor.objects.all().order_by("-id"),
        "doctorcount": models.Doctor.objects.filter(status=True).count(),
        "pendingdoctorcount": models.Doctor.objects.filter(status=False).count(),
        "departments": models.Doctor.objects.values_list('department', flat=True).distinct(),
        "appointmentcount": models.Appointment.objects.all().count(),
    }

    if action == "view":
        return render(request, "hospital/admin_view_doctor.html", 
                     {"doctors": models.Doctor.objects.filter(status=True)})

    if action == "delete":
        doc = get_object_or_404(models.Doctor, id=pk)
        doc.user.delete()
        doc.delete()
        return redirect("admin-view-doctor")

    if action == "update":
        doc = get_object_or_404(models.Doctor, id=pk)
        user = doc.user
        if request.method == "POST":
            uform = forms.DoctorUserUpdateForm(request.POST, instance=user)
            dform = forms.DoctorForm(request.POST, request.FILES, instance=doc)
            if uform.is_valid() and dform.is_valid():
                try:
                    with transaction.atomic():
                        user = uform.save()
                        doctor = dform.save(commit=False)
                        doctor.user = user
                        doctor.status = True
                        doctor.save()
                    messages.success(request, "Doctor information updated successfully!")
                    return redirect("admin-view-doctor")
                except Exception as e:
                    messages.error(request, f"Error updating doctor: {str(e)}")
            else:
                for field, errors in uform.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                for field, errors in dform.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            uform = forms.DoctorUserUpdateForm(instance=user)
            dform = forms.DoctorForm(instance=doc)
        return render(request, "hospital/admin_update_doctor.html",
                      {"userForm": uform, "doctorForm": dform})

    if action == "add":
        if request.method == "POST":
            uform = forms.DoctorUserForm(request.POST)
            dform = forms.DoctorForm(request.POST, request.FILES)
            if uform.is_valid() and dform.is_valid():
                usr = uform.save(commit=False); usr.set_password(usr.password); usr.save()
                doc = dform.save(commit=False); doc.user = usr; doc.status = True; doc.save()
                Group.objects.get_or_create(name=DOCTOR_GROUP)[0].user_set.add(usr)
                return redirect("admin-view-doctor")
        else:
            uform, dform = forms.DoctorUserForm(), forms.DoctorForm()
        return render(request, "hospital/admin_add_doctor.html",
                      {"userForm": uform, "doctorForm": dform})

    if action == "approve":
        docs = models.Doctor.objects.filter(status=False)
        return render(request, "hospital/admin_approve_doctor.html", {"doctors": docs})

    if action == "approve-doctor":
        doc = get_object_or_404(models.Doctor, id=pk)
        doc.status = True; doc.save()
        return redirect("admin-approve-doctor")

    if action == "reject":
        doc = get_object_or_404(models.Doctor, id=pk)
        doc.user.delete(); doc.delete()
        return redirect("admin-approve-doctor")

    if action == "specialisation":
        docs = models.Doctor.objects.filter(status=True)
        return render(request, "hospital/admin_view_doctor_specialisation.html",
                      {"doctors": docs})

    # Default view (admin_doctor.html)
    return render(request, "hospital/admin_doctor.html", doctor_stats)

# -- Patient CRUD ----------------------------------------------------------- #
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_views(request, action=None, pk=None):
    if action == "view":
        if pk:
            pat = get_object_or_404(models.Patient, id=pk, status=True)
            return render(request, "hospital/admin_patient_detail.html", {"patient": pat})
        pats = models.Patient.objects.filter(status=True).select_related("room")
        return render(request, "hospital/admin_view_patient.html", {"patients": pats})

    if action == "delete":
        pat = get_object_or_404(models.Patient, id=pk)
        pat.user.delete(); pat.delete()
        return redirect("admin-view-patient")

    if action == "update":
        pat = get_object_or_404(models.Patient, id=pk)
        user = pat.user
        if request.method == "POST":
            uform = forms.PatientUserUpdateForm(request.POST, instance=user)
            pform = forms.PatientForm(request.POST, request.FILES, instance=pat)
            if uform.is_valid() and pform.is_valid():
                try:
                    with transaction.atomic():
                        user = uform.save()
                        patient = pform.save(commit=False)
                        patient.user = user
                        patient.status = True
                        patient.save()
                    messages.success(request, "Patient information updated successfully!")
                    return redirect("admin-view-patient")
                except Exception as e:
                    messages.error(request, f"Error updating patient: {str(e)}")
            else:
                for field, errors in uform.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                for field, errors in pform.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            uform = forms.PatientUserUpdateForm(instance=user)
            pform = forms.PatientForm(instance=pat)
        return render(request, "hospital/admin_update_patient.html",
                    {"userForm": uform, "patientForm": pform})

    if action == "add":
        if request.method == "POST":
            uform = forms.PatientUserForm(request.POST)
            pform = forms.PatientForm(request.POST, request.FILES)
            if uform.is_valid() and pform.is_valid():
                usr = uform.save(commit=False)
                usr.set_password(usr.password)
                usr.save()
                pat = pform.save(commit=False)
                pat.user = usr
                pat.status = True
                # Make doctor assignment optional
                doctor = pform.cleaned_data.get('assignedDoctorId')
                if doctor:
                    pat.assignedDoctorId = doctor.id
                pat.save()
                Group.objects.get_or_create(name=PATIENT_GROUP)[0].user_set.add(usr)
                return redirect("admin-view-patient")
        else:
            uform = forms.PatientUserForm()
            pform = forms.PatientForm()
        return render(request, "hospital/admin_add_patient.html",
                    {"userForm": uform, "patientForm": pform})

    if action == "approve":
        pats = models.Patient.objects.filter(status=False)
        return render(request, "hospital/admin_approve_patient.html", {"patients": pats})

    if action == "approve-patient":
        pat = get_object_or_404(models.Patient, id=pk)
        pat.status = True
        pat.save()
        return redirect("admin-approve-patient")

    if action == "reject":
        pat = get_object_or_404(models.Patient, id=pk)
        pat.user.delete()
        pat.delete()
        return redirect("admin-approve-patient")

    if action == "discharge":
        pats = models.Patient.objects.filter(status=True)
        return render(request, "hospital/admin_discharge_patient.html", {"patients": pats})

    if action == "discharge-patient":
        return handle_discharge_patient(request, pk)

    # Default view - add context data for cards
    total_patients = models.Patient.objects.filter(status=True).count()
    pending_patients = models.Patient.objects.filter(status=False).count()
    total_appointments = models.Appointment.objects.filter(status=True).count()
    discharged_patients = models.PatientDischargeDetails.objects.count()
    
    # Room statistics
    total_rooms = models.Room.objects.count()
    occupied_rooms = models.Room.objects.filter(is_occupied=True).count()
    available_rooms = total_rooms - occupied_rooms
    
    # Recent patients
    recent_patients = models.Patient.objects.filter(
        status=True
    ).select_related('room').order_by('-admitDate')[:5]
    
    context = {
        'total_patients': total_patients,
        'pending_patients': pending_patients,
        'total_appointments': total_appointments,
        'discharged_patients': discharged_patients,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'recent_patients': recent_patients,
    }
    
    return render(request, "hospital/admin_patient.html", context)

# --------------------------------------------------------------------------- #
# Discharge helper
# --------------------------------------------------------------------------- #
def handle_discharge_patient(request, pk):
    pat = get_object_or_404(models.Patient, id=pk)
    if not pat.assignedDoctorId:
        messages.error(request, "Cannot discharge patient without an assigned doctor. Please assign a doctor first.")
        return redirect("admin-discharge-patient")

    days = (date.today() - pat.admitDate).days
    doc  = get_object_or_404(User, id=pat.assignedDoctorId)

    ctx = {
        "patientId": pk,
        "name":     pat.get_name,
        "mobile":   pat.mobile,
        "address":  pat.address,
        "symptoms": pat.symptoms,
        "admitDate": pat.admitDate,
        "todayDate": date.today(),
        "day":       days,
        "assignedDoctorName": doc.first_name,
    }

    if request.method == "POST":
        fees = {
            "roomCharge":   int(request.POST["roomCharge"]) * days,
            "doctorFee":    int(request.POST["doctorFee"]),
            "medicineCost": int(request.POST["medicineCost"]),
            "OtherCharge":  int(request.POST["OtherCharge"]),
        }
        fees["total"] = sum(fees.values())
        ctx.update(fees)

        models.PatientDischargeDetails.objects.create(
            patientId=pk,
            patientName=pat.get_name,
            assignedDoctorName=doc.first_name,
            address=pat.address,
            mobile=pat.mobile,
            symptoms=pat.symptoms,
            admitDate=pat.admitDate,
            releaseDate=date.today(),
            daySpent=days,
            medicineCost=fees["medicineCost"],
            roomCharge=fees["roomCharge"],
            doctorFee=fees["doctorFee"],
            OtherCharge=fees["OtherCharge"],
            total=fees["total"],
        )
        return render(request, "hospital/patient_final_bill.html", ctx)

    return render(request, "hospital/patient_generate_bill.html", ctx)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def update_patient_doctor(patient, doctor, request=None):
    """Update patient's assigned doctor when an appointment is approved."""
    if patient and doctor:
        patient.assignedDoctorId = doctor.user.id
        patient.save()
        if request:
            messages.info(request, f"Patient's assigned doctor has been updated to Dr. {doctor.get_name}")

# --------------------------------------------------------------------------- #
# Appointment admin-side
# --------------------------------------------------------------------------- #
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_appointment_views(request, action=None, pk=None):
    if action == "view":
        apps = models.Appointment.objects.filter(status=True)
        return render(request, "hospital/admin_view_appointment.html",
                      {"appointments": apps})

    if action == "add":
        if request.method == "POST":
            form = forms.AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.status = True  # Auto-approve when admin creates
                appointment.save()
                # Update patient's assigned doctor
                update_patient_doctor(appointment.patient, appointment.doctor, request)
                messages.success(request, 'Appointment scheduled successfully!')
                return redirect("admin-view-appointment")
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = forms.AppointmentForm()
        
        context = {
            "appointmentForm": form,
            "today": date.today().isoformat()  # For date input min attribute
        }
        return render(request, "hospital/admin_add_appointment.html", context)

    if action == "approve":
        apps = models.Appointment.objects.filter(status=False)
        return render(request, "hospital/admin_approve_appointment.html",
                      {"appointments": apps})

    if action == "approve-appointment":
        app = get_object_or_404(models.Appointment, id=pk)
        app.status = True
        app.save()
        # Update patient's assigned doctor
        update_patient_doctor(app.patient, app.doctor, request)
        messages.success(request, 'Appointment approved successfully!')
        return redirect("admin-approve-appointment")

    if action == "reject":
        app = get_object_or_404(models.Appointment, id=pk)
        app.delete()
        messages.success(request, 'Appointment rejected successfully!')
        return redirect("admin-approve-appointment")

    if action == "details":
        app = get_object_or_404(models.Appointment, id=pk)
        return render(request, "hospital/admin_appointment_details.html",
                      {"appointment": app})

    if action == "delete":
        app = get_object_or_404(models.Appointment, id=pk)
        app.delete()
        messages.success(request, "Appointment cancelled successfully")
        return redirect("admin-view-appointment")

    # Default view - add context data for cards
    context = {
        'appointmentcount': models.Appointment.objects.filter(status=True).count(),
        'pendingappointmentcount': models.Appointment.objects.filter(status=False).count(),
        'doctorcount': models.Doctor.objects.filter(status=True).count(),
        # Get today's appointments
        'today_appointments': models.Appointment.objects.filter(
            appointmentDate=date.today(),
            status=True
        ).count(),
        # Get recent appointments
        'recent_appointments': models.Appointment.objects.filter(
            status=True
        ).order_by('-appointmentDate', '-appointmentTime')[:5]
    }
    return render(request, "hospital/admin_appointment.html", context)

# --------------------------------------------------------------------------- #
# Room management (admin)
# --------------------------------------------------------------------------- #
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_rooms_view(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('home')
        
    rooms = models.Room.objects.all().order_by('room_number')
    
    # Count rooms by type
    room_counts = {
        'ward_count': rooms.filter(room_type='WARD').count(),
        'private_count': rooms.filter(room_type='PRIVATE').count(),
        'icu_count': rooms.filter(room_type='ICU').count(),
        'office_count': rooms.filter(room_type='OFFICE').count(),
    }
    
    # Get room requests
    room_requests = models.RoomRequest.objects.filter(status='PENDING')\
        .select_related('doctor', 'patient', 'requested_room')\
        .order_by('-request_date')[:5]
    
    context = {
        'rooms': rooms,
        'available_count': rooms.filter(is_occupied=False).count(),
        'occupied_count': rooms.filter(is_occupied=True).count(),
        'room_requests': room_requests,
        **room_counts
    }
    return render(request, 'hospital/admin_rooms.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_room_view(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('home')
        
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room {room.room_number} added successfully!')
            return redirect('admin-rooms')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.RoomForm()
    
    return render(request, 'hospital/admin_add_room.html', {'form': form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_room_management(request, action=None, room_id=None, patient_id=None):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('home')

    if action == "assign":
        pat = get_object_or_404(models.Patient, id=patient_id)
        available = models.Room.objects.filter(is_occupied=False)
        if request.method == "POST":
            room = get_object_or_404(models.Room, id=request.POST.get("room_id"))
            if pat.room:  # free previous
                pat.room.is_occupied = False; pat.room.save()
            room.is_occupied, room.current_patient = True, pat.id
            room.save()
            pat.room = room; pat.save()
            return redirect("admin-view-patient-detail", pk=pat.id)
        return render(request, "hospital/admin_assign_room.html",
                      {"patient": pat, "rooms": available})

    if action == "change":
        pat = get_object_or_404(models.Patient, id=patient_id)
        cur = pat.room
        available = models.Room.objects.filter(
            Q(is_occupied=False) | Q(id=cur.id) if cur else Q(is_occupied=False)
        )
        if request.method == "POST":
            new_room = get_object_or_404(models.Room, id=request.POST.get("room_id"))
            if cur:
                cur.is_occupied = False; cur.save()
            new_room.is_occupied, new_room.current_patient = True, pat.id
            new_room.save()
            pat.room = new_room; pat.save()
            return redirect("admin-view-patient-detail", pk=pat.id)
        return render(request, "hospital/admin_change_room.html",
                      {"patient": pat, "rooms": available, "current_room": cur})

    if action == "details":
        room = get_object_or_404(models.Room, id=room_id)
        pat  = get_object_or_404(models.Patient, id=room.current_patient) if room.current_patient else None
        return render(request, "hospital/admin_room_details.html",
                      {"room": room, "patient": pat})

    if action == "discharge":
        pat = get_object_or_404(models.Patient, id=patient_id)
        room = pat.room
        if room:
            room.is_occupied, room.current_patient = False, None; room.save()
            pat.room = None; pat.save()
        return redirect("admin-view-patient")

    # If no action is specified or action is not recognized, redirect to rooms list
    return redirect('admin-rooms')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_room_requests_view(request):
    # Get all room requests ordered by date
    requests = models.RoomRequest.objects.all().order_by('-request_date')
    return render(request, 'hospital/admin_room_requests.html', {'requests': requests})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_room_request(request, pk):
    room_request = get_object_or_404(models.RoomRequest, id=pk)
    
    # Check available rooms
    available_rooms = models.Room.objects.filter(
        room_type=room_request.requested_room.room_type,
        is_occupied=False
    )
    
    if not available_rooms.exists():
        messages.error(request, f'No available {room_request.requested_room.get_room_type_display()} rooms. Please add more rooms or wait for one to become available.')
        return redirect('admin-room-requests')
    
    if request.method == 'POST':
        form = forms.RoomAssignmentForm(request.POST, instance=room_request)
        if form.is_valid():
            room_request = form.save(commit=False)
            room_request.status = 'APPROVED'
            room_request.response_date = timezone.now()
            room_request.save()
            
            # Update room status
            assigned_room = room_request.assigned_room
            assigned_room.is_occupied = True
            assigned_room.current_patient = room_request.patient.id
            assigned_room.save()
            
            messages.success(request, f'Room request approved. {assigned_room.room_number} has been assigned to {room_request.patient.get_name}.')
            return redirect('admin-room-requests')
    else:
        form = forms.RoomAssignmentForm(instance=room_request)
    
    context = {
        'request': room_request,
        'form': form,
        'available_rooms': available_rooms,
    }
    return render(request, 'hospital/admin_approve_room_request.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_deny_room_request(request, pk):
    room_request = get_object_or_404(models.RoomRequest, id=pk)
    if request.method == 'POST':
        room_request.status = 'DENIED'
        room_request.response_date = timezone.now()
        room_request.response_note = request.POST.get('reason', '')
        room_request.save()
        messages.success(request, 'Room request has been denied.')
        return redirect('admin-room-requests')
    return render(request, 'hospital/admin_deny_room_request.html', {'request': room_request})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_edit_room_view(request, room_id):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('home')
        
    room = get_object_or_404(models.Room, id=room_id)
    
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room {room.room_number} updated successfully!')
            return redirect('admin-rooms')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.RoomForm(instance=room)
    
    return render(request, 'hospital/admin_edit_room.html', {'form': form, 'room': room})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_room_view(request, room_id):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if not is_admin(request.user):
        return redirect('home')
        
    room = get_object_or_404(models.Room, id=room_id)
    
    # Check if room is occupied
    if room.is_occupied:
        messages.error(request, f'Cannot delete room {room.room_number} as it is currently occupied.')
        return redirect('admin-rooms')
        
    # Check if room has any pending requests
    if models.RoomRequest.objects.filter(requested_room=room, status='PENDING').exists():
        messages.error(request, f'Cannot delete room {room.room_number} as it has pending requests.')
        return redirect('admin-rooms')
    
    try:
        room.delete()
        messages.success(request, f'Room {room.room_number} deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting room: {str(e)}')
    
    return redirect('admin-rooms')

# --------------------------------------------------------------------------- #
# DOCTOR SECTION
# --------------------------------------------------------------------------- #
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    doc = models.Doctor.objects.get(user_id=request.user.id)
    
    # Get today's date for filtering
    today = timezone.now().date()
    
    # Get all appointments for this doctor with room requests
    appointments = models.Appointment.objects.filter(
        doctor=doc
    ).prefetch_related(
        'room_requests'
    ).select_related('patient', 'room')
    
    # Get pending room requests
    pending_room_requests = models.RoomRequest.objects.filter(
        doctor=doc,
        status='PENDING'
    ).order_by('-request_date')[:5]
    
    # Calculate statistics
    appointments_today = appointments.filter(
        appointmentDate=today,
        status=True
    ).count()
    
    total_patients = models.Patient.objects.filter(
        status=True,
        assignedDoctorId=request.user.id
    ).count()
    
    pending_appointments = appointments.filter(
        status=False
    ).count()
    
    discharge_patients = models.PatientDischargeDetails.objects.filter(
        assignedDoctorName=request.user.first_name
    ).count()
    
    # Get recent appointments with patients
    recent_appointments = appointments.filter(
        status=True
    ).order_by('-appointmentDate', '-appointmentTime')[:5]
    
    # Get recent patients
    recent_patients = models.Patient.objects.filter(
        status=True,
        assignedDoctorId=request.user.id
    ).order_by('-admitDate')[:5]
    
    return render(request, "hospital/doctor_dashboard.html", {
        "appointments_today": appointments_today,
        "total_patients": total_patients,
        "pending_appointments": pending_appointments,
        "discharge_patients": discharge_patients,
        "appointments": recent_appointments,
        "recent_patients": recent_patients,
        "doctor": doc,
        "pending_room_requests": pending_room_requests.count(),
    })


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_views(request, action=None, pk=None):
    doc = models.Doctor.objects.get(user_id=request.user.id)

    if action == "view" or action is None:  # Handle both view and default case
        pats = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id)
        return render(request, "hospital/doctor_view_patient.html",
                      {"patients": pats, "doctor": doc})

    if action == "detail":
        patient = get_object_or_404(models.Patient, id=pk, assignedDoctorId=request.user.id)
        medical_records = models.PatientRecord.objects.filter(patient=patient).order_by('-date')
        return render(request, "hospital/doctor_view_patient_detail.html",
                     {"patient": patient, "doctor": doc, "medical_records": medical_records})

    if action == "search":
        q = request.GET.get("query", "")
        pats = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id)\
                .filter(Q(symptoms__icontains=q) | Q(user__first_name__icontains=q))
        return render(request, "hospital/doctor_view_patient.html",
                      {"patients": pats, "doctor": doc})

    if action == "discharged":
        dis = models.PatientDischargeDetails.objects.filter(
            assignedDoctorName=request.user.first_name).distinct()
        return render(request, "hospital/doctor_view_discharge_patient.html",
                      {"dischargedpatients": dis, "doctor": doc})

    if action == "update_record":
        patient = get_object_or_404(models.Patient, id=pk, assignedDoctorId=request.user.id)
        if request.method == 'POST':
            form = forms.PatientRecordForm(request.POST, request.FILES)
            if form.is_valid():
                record = form.save(commit=False)
                record.patient = patient
                record.doctor = doc
                record.save()
                messages.success(request, "Patient record updated successfully.")
                return redirect('doctor-patient')
        else:
            form = forms.PatientRecordForm()
        
        context = {
            "doctor": doc,
            "patient": patient,
            "form": form,
            "medical_records": models.PatientRecord.objects.filter(patient=patient).order_by('-created_at')
        }
        return render(request, "hospital/doctor_update_record.html", context)

    # If no action matches, show the patient list
    pats = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id)
    return render(request, "hospital/doctor_view_patient.html",
                  {"patients": pats, "doctor": doc})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_appointment_views(request, action=None, pk=None):
    doc = models.Doctor.objects.get(user_id=request.user.id)

    if action == "view":
        # Show both approved and pending appointments
        apps = models.Appointment.objects.filter(
            doctor=doc,
            appointmentDate__gte=date.today()
        ).order_by("appointmentDate", "appointmentTime")
        pats = models.Patient.objects.filter(
            id__in=apps.values_list("patient", flat=True)
        )
        return render(request, "hospital/doctor_view_appointment.html",
                     {"appointments": zip(apps, pats), "doctor": doc})

    if action == "pending":
        # Show only pending appointments
        apps = models.Appointment.objects.filter(
            doctor=doc,
            status=False
        ).order_by("appointmentDate", "appointmentTime")
        pats = models.Patient.objects.filter(
            id__in=apps.values_list("patient", flat=True)
        )
        return render(request, "hospital/doctor_pending_appointments.html",
                     {"appointments": zip(apps, pats), "doctor": doc})

    if action == "approve":
        app = get_object_or_404(models.Appointment, id=pk, doctor=doc)
        app.status = True
        app.save()
        # Update patient's assigned doctor
        update_patient_doctor(app.patient, doc, request)
        messages.success(request, "Appointment approved successfully!")
        return redirect("doctor-pending-appointments")

    if action == "reject":
        app = get_object_or_404(models.Appointment, id=pk, doctor=doc)
        app.delete()
        messages.success(request, "Appointment rejected successfully!")
        return redirect("doctor-pending-appointments")

    if action == "delete":
        if pk:
            get_object_or_404(models.Appointment, id=pk, doctor=doc).delete()
            messages.success(request, "Appointment deleted successfully!")
        return redirect("doctor-view-appointment")

    return render(request, "hospital/doctor_appointment.html", {"doctor": doc})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_request_room(request):
    if request.method == 'POST':
        try:
            # Get form data
            appointment_id = request.POST.get('appointment_id')
            room_type = request.POST.get('room_type')
            reason = request.POST.get('reason')
            duration = int(request.POST.get('duration', 1))
            
            # Get doctor and appointment
            doctor = models.Doctor.objects.get(user_id=request.user.id)
            appointment = get_object_or_404(models.Appointment, id=appointment_id)
            
            # Find any room of the requested type
            room = models.Room.objects.filter(room_type=room_type).first()
            if not room:
                messages.error(request, f'No {room_type} rooms exist in the system. Please contact admin.')
                return redirect('doctor-dashboard')
            
            # Create the room request
            room_request = models.RoomRequest.objects.create(
                doctor=doctor,
                patient=appointment.patient,
                appointment=appointment,  # Set the appointment
                requested_room=room,
                reason=reason,
                expected_duration=duration
            )
            
            messages.success(request, 'Room request has been submitted successfully.')
            return redirect('doctor-dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating room request: {str(e)}')
            return redirect('doctor-dashboard')
            
    return redirect('doctor-dashboard')

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_room_requests_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    room_requests = models.RoomRequest.objects.filter(doctor=doctor).order_by('-request_date')
    
    context = {
        'doctor': doctor,
        'room_requests': room_requests,
        'pending_count': room_requests.filter(status='PENDING').count(),
        'approved_count': room_requests.filter(status='APPROVED').count(),
        'denied_count': room_requests.filter(status='DENIED').count(),
    }
    return render(request, 'hospital/doctor_room_requests.html', context)

# --------------------------------------------------------------------------- #
# PATIENT SECTION
# --------------------------------------------------------------------------- #
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    pat = models.Patient.objects.get(user_id=request.user.id)
    
    # Get upcoming appointments
    appointments = models.Appointment.objects.filter(
        patient=pat,
        appointmentDate__gte=date.today()
    ).order_by('appointmentDate', 'appointmentTime')
    
    # Calculate days since admission
    admission_days = (date.today() - pat.admitDate).days
    
    # Handle case where patient has no assigned doctor
    if not pat.assignedDoctorId:
        messages.warning(request, "You don't have an assigned doctor yet. Please contact the admin.")
        return render(request, "hospital/patient_dashboard.html", {
            "patient": pat,
            "doctorName": "Not Assigned",
            "doctorMobile": "N/A",
            "doctorAddress": "N/A",
            "symptoms": pat.symptoms,
            "doctorDepartment": "N/A",
            "admitDate": pat.admitDate,
            "appointments": appointments,
            "upcoming_appointments": appointments.count(),
            "total_prescriptions": 0,  # Add prescription count when feature is implemented
            "assigned_doctor": "Not Assigned",
            "admission_days": admission_days
        })
    
    try:
        doc = models.Doctor.objects.get(user_id=pat.assignedDoctorId)
        return render(request, "hospital/patient_dashboard.html", {
            "patient": pat,
            "doctorName": doc.get_name,
            "doctorMobile": doc.mobile,
            "doctorAddress": doc.address,
            "symptoms": pat.symptoms,
            "doctorDepartment": doc.department,
            "admitDate": pat.admitDate,
            "appointments": appointments,
            "upcoming_appointments": appointments.count(),
            "total_prescriptions": 0,  # Add prescription count when feature is implemented
            "assigned_doctor": f"Dr. {doc.get_name}",
            "admission_days": admission_days
        })
    except models.Doctor.DoesNotExist:
        messages.error(request, "Assigned doctor not found. Please contact the admin.")
        return render(request, "hospital/patient_dashboard.html", {
            "patient": pat,
            "doctorName": "Error - Doctor Not Found",
            "doctorMobile": "N/A",
            "doctorAddress": "N/A",
            "symptoms": pat.symptoms,
            "doctorDepartment": "N/A",
            "admitDate": pat.admitDate,
            "appointments": appointments,
            "upcoming_appointments": appointments.count(),
            "total_prescriptions": 0,  # Add prescription count when feature is implemented
            "assigned_doctor": "Not Found",
            "admission_days": admission_days
        })


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_appointment_views(request, action=None, view_type=None):
    pat = models.Patient.objects.get(user_id=request.user.id)

    if action == "book":
        initial = {}
        if request.GET.get('doctor'):
            try:
                doctor = models.Doctor.objects.get(id=request.GET.get('doctor'))
                initial['doctor'] = doctor
            except models.Doctor.DoesNotExist:
                pass
        
        if request.method == "POST":
            form = forms.PatientAppointmentForm(request.POST)
            if form.is_valid():
                app = form.save(commit=False)
                app.patient = pat
                app.doctor = form.cleaned_data['doctor']  # Set the doctor from form
                app.patientName = pat.get_name  # Set names for legacy support
                app.doctorName = app.doctor.get_name
                app.status = False  # Needs approval
                app.save()
                messages.success(request, "Appointment request submitted successfully! Awaiting doctor's approval.")
                return redirect("patient-view-appointment")
            else:
                messages.error(request, "Please fix the errors in the form.")
        else:
            form = forms.PatientAppointmentForm(initial=initial)
        return render(request, "hospital/patient_book_appointment.html",
                     {"appointmentForm": form, "patient": pat})

    if action == "view":
        apps = models.Appointment.objects.filter(patient=pat)
        return render(request, "hospital/patient_view_appointment.html",
                     {"appointments": apps, "patient": pat})

    if action == "view-doctors":
        docs = models.Doctor.objects.filter(status=True).order_by('department')
        # If view_type is not provided in URL, try to get it from GET parameters
        view_type = view_type or request.GET.get('view', 'grid')
        return render(request, "hospital/patient_view_doctor.html",
                     {"patient": pat, "doctors": docs, "view_type": view_type})

    if action == "search-doctors":
        q = request.GET.get("query", "")
        docs = models.Doctor.objects.filter(status=True)\
                .filter(Q(department__icontains=q) | Q(user__first_name__icontains=q))\
                .order_by('department')
        view_type = view_type or request.GET.get('view', 'grid')  # Maintain view type during search
        return render(request, "hospital/patient_view_doctor.html",
                     {"patient": pat, "doctors": docs, "view_type": view_type})

    if action == "discharge":
        det = models.PatientDischargeDetails.objects.filter(patientId=pat.id)\
                                                   .order_by("-id").first()
        if det:
            ctx = {
                "is_discharged": True,
                "patient": pat,
                "patientId": pat.id,
                "patientName": pat.get_name,
                "assignedDoctorName": det.assignedDoctorName,
                "address": pat.address,
                "mobile": pat.mobile,
                "symptoms": pat.symptoms,
                "admitDate": pat.admitDate,
                "releaseDate": det.releaseDate,
                "daySpent": det.daySpent,
                "medicineCost": det.medicineCost,
                "roomCharge": det.roomCharge,
                "doctorFee": det.doctorFee,
                "OtherCharge": det.OtherCharge,
                "total": det.total,
            }
        else:
            ctx = {"is_discharged": False, "patient": pat, "patientId": pat.id}
        return render(request, "hospital/patient_discharge.html", ctx)

    # Default view - patient_appointment.html
    context = {
        'patient': pat,
        'upcoming_appointments': models.Appointment.objects.filter(
            patient=pat,
            appointmentDate__gte=timezone.now().date(),
            status=True
        ).count(),
        'available_doctors': models.Doctor.objects.filter(status=True).count(),
        'emergency_contact': getattr(settings, 'HOSPITAL_EMERGENCY_CONTACT', '911'),
    }
    return render(request, "hospital/patient_appointment.html", context)

# --------------------------------------------------------------------------- #
# Misc static pages
# --------------------------------------------------------------------------- #
def aboutus_view(request):
    return render(request, "hospital/aboutus.html")


def contactus_view(request):
    if request.method == 'POST':
        form = forms.ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contactus')
    else:
        form = forms.ContactMessageForm()
    return render(request, 'hospital/contactus.html', {'form': form})


def privacy_policy_view(request):
    return render(request, "hospital/privacy_policy.html")


def terms_view(request):
    return render(request, "hospital/terms.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_messages_view(request):
    contact_messages = models.ContactMessage.objects.all()
    context = {
        'contact_messages': contact_messages,
        'total_messages': contact_messages.count(),
        'unread_messages': contact_messages.filter(is_read=False).count()
    }
    return render(request, 'hospital/admin_contact_messages.html', context)

@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_mark_message_read(request, pk):
    message = get_object_or_404(models.ContactMessage, id=pk)
    message.is_read = True
    message.save()
    messages.success(request, 'Message marked as read.')
    return redirect('admin-messages')

@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_delete_message(request, pk):
    message = get_object_or_404(models.ContactMessage, id=pk)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('admin-messages')

# --------------------------------------------------------------------------- #
# PDF download after discharge
# --------------------------------------------------------------------------- #
@login_required
def download_pdf_view(request, pk):
    det = models.PatientDischargeDetails.objects.filter(patientId=pk)\
                                               .order_by("-id").first()
    if not det:
        return redirect("patient-discharge")

    ctx = {
        "patientName": det.patientName,
        "assignedDoctorName": det.assignedDoctorName,
        "address": det.address,
        "mobile": det.mobile,
        "symptoms": det.symptoms,
        "admitDate": det.admitDate,
        "releaseDate": det.releaseDate,
        "daySpent": det.daySpent,
        "medicineCost": det.medicineCost,
        "roomCharge": det.roomCharge,
        "doctorFee": det.doctorFee,
        "OtherCharge": det.OtherCharge,
        "total": det.total,
    }
    return render_to_pdf("hospital/download_bill.html", ctx)

# --------------------------------------------------------------------------- #
# Admin Profile
# --------------------------------------------------------------------------- #
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_profile_view(request):
    admin = request.user
    context = {
        'admin': admin,
        'total_doctors': models.Doctor.objects.filter(status=True).count(),
        'total_patients': models.Patient.objects.filter(status=True).count(),
        'total_appointments': models.Appointment.objects.filter(status=True).count(),
        'total_rooms': models.Room.objects.count(),
        'pending_approvals': {
            'doctors': models.Doctor.objects.filter(status=False).count(),
            'patients': models.Patient.objects.filter(status=False).count(),
            'appointments': models.Appointment.objects.filter(status=False).count(),
        }
    }
    return render(request, "hospital/admin_profile.html", context)

# --------------------------------------------------------------------------- #
# Doctor Profile
# --------------------------------------------------------------------------- #
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_profile_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    context = {
        'doctor': doctor,
        'total_patients': models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id).count(),
        'total_appointments': models.Appointment.objects.filter(status=True, doctor=doctor).count(),
        'total_discharged': models.PatientDischargeDetails.objects.filter(assignedDoctorName=request.user.first_name).count(),
        'pending_appointments': models.Appointment.objects.filter(status=False, doctor=doctor).count(),
        'recent_appointments': models.Appointment.objects.filter(
            status=True,
            doctor=doctor,
            appointmentDate__gte=timezone.now().date()
        ).order_by('appointmentDate', 'appointmentTime')[:5],
    }
    return render(request, "hospital/doctor_profile.html", context)

# --------------------------------------------------------------------------- #
# Patient Profile
# --------------------------------------------------------------------------- #
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_profile_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    assigned_doctor = None
    if patient.assignedDoctorId:
        try:
            assigned_doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
        except models.Doctor.DoesNotExist:
            pass

    context = {
        'patient': patient,
        'doctor': assigned_doctor,
        'total_appointments': models.Appointment.objects.filter(patient=patient).count(),
        'upcoming_appointments': models.Appointment.objects.filter(
            patient=patient,
            appointmentDate__gte=timezone.now().date()
        ).count(),
        'recent_appointments': models.Appointment.objects.filter(
            patient=patient
        ).order_by('-appointmentDate', '-appointmentTime')[:5],
        'discharge_details': models.PatientDischargeDetails.objects.filter(
            patientId=patient.id
        ).order_by('-id').first()
    }
    return render(request, "hospital/patient_profile.html", context)

def admin_context_processor(request):
    """Add unread messages count to admin templates context"""
    if request.user.is_authenticated and is_admin(request.user):
        unread_messages_count = models.ContactMessage.objects.filter(is_read=False).count()
        return {'unread_messages_count': unread_messages_count}
    return {}
