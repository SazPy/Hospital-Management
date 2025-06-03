# Hospital Management System

A comprehensive hospital management system built with Django that helps manage doctors, patients, appointments, and room allocations.

## Features

- User Management (Admin, Doctors, Patients)
- Appointment Scheduling
- Patient Records Management
- Room Management
- Discharge Summary Generation
- Doctor Specialization Management

## Setup Instructions

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser

## User Types

1. Admin
   - Manage doctors and patients
   - Approve/reject appointments
   - Manage rooms
   - Generate discharge summaries

2. Doctors
   - View assigned patients
   - Manage appointments
   - View patient history

3. Patients
   - Book appointments
   - View appointment status
   - View assigned doctors
   - Access medical records

## Project Structure

- `hospital/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `forms.py` - Form definitions
  - `admin.py` - Admin interface configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request 