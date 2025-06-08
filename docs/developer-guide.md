# Developer Guide

## Technology Stack

### Backend
- Python 3.8+
- Django 5.0+
- SQLite/PostgreSQL
- Django REST framework (for APIs)

### Frontend
- HTML5/CSS3
- JavaScript/jQuery
- Bootstrap 5
- Font Awesome

### Development Tools
- Git for version control
- VS Code/PyCharm (recommended IDEs)
- Python virtual environment
- Django Debug Toolbar

## Project Structure

```
hospital-management/
├── hospital/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin interface
│   ├── urls.py              # URL routing
│   └── tests/               # Test files
├── templates/               # HTML templates
│   └── hospital/           # App templates
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   └── img/               # Images
├── media/                 # User uploads
├── docs/                  # Documentation
└── manage.py              # Django CLI
```

## Setup Development Environment

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/hospital-management.git
   cd hospital-management
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Database Schema

### Core Models

#### User Model
- Extends Django's AbstractUser
- Additional fields for role management

#### Doctor Model
```python
class Doctor(models.Model):
    user = OneToOneField(User)
    department = CharField()
    status = BooleanField()
    # Other fields...
```

#### Patient Model
```python
class Patient(models.Model):
    user = OneToOneField(User)
    assignedDoctorId = IntegerField()
    status = BooleanField()
    # Other fields...
```

#### Appointment Model
```python
class Appointment(models.Model):
    doctor = ForeignKey(Doctor)
    patient = ForeignKey(Patient)
    appointmentDate = DateField()
    status = BooleanField()
    # Other fields...
```

## Authentication System

### User Types
1. Admin
2. Doctor
3. Patient

### Authentication Flow
1. User submits login form
2. Credentials validated
3. Role checked
4. Redirected to appropriate dashboard

### Middleware
- Authentication middleware
- Role-based access control
- Session management

## Views and Templates

### Class-Based Views
- Use Django's generic views
- Custom mixins for authorization
- Form handling views

### Template Structure
- Base template with common elements
- Role-specific base templates
- Feature-specific templates

### Context Processors
- User role information
- Common data
- Site settings

## Forms and Validation

### Form Classes
- User registration forms
- Appointment forms
- Profile update forms

### Validation
- Client-side validation
- Server-side validation
- Custom validators

## API Documentation

### Endpoints

#### Authentication
```
POST /api/login/
POST /api/logout/
POST /api/register/
```

#### Doctors
```
GET /api/doctors/
POST /api/doctors/
GET /api/doctors/{id}/
PUT /api/doctors/{id}/
```

#### Patients
```
GET /api/patients/
POST /api/patients/
GET /api/patients/{id}/
PUT /api/patients/{id}/
```

#### Appointments
```
GET /api/appointments/
POST /api/appointments/
GET /api/appointments/{id}/
PUT /api/appointments/{id}/
```

## Testing

### Unit Tests
```python
python manage.py test hospital.tests
```

### Test Categories
- Model tests
- View tests
- Form tests
- API tests

### Coverage
```bash
coverage run manage.py test
coverage report
```

## Security

### Implemented Measures
- CSRF protection
- XSS prevention
- SQL injection protection
- Password hashing
- Session security

### Best Practices
- Input validation
- Output escaping
- Secure file uploads
- Rate limiting
- Error handling

## Deployment

### Prerequisites
- Domain name
- SSL certificate
- Production database
- Web server (Nginx/Apache)

### Steps
1. Set production settings
2. Configure web server
3. Set up SSL
4. Configure static files
5. Set up database
6. Deploy application

### Monitoring
- Error logging
- Performance monitoring
- Security auditing
- Backup system

## Version Control

### Branching Strategy
- main: production code
- develop: development code
- feature/*: new features
- hotfix/*: urgent fixes

### Commit Guidelines
- Clear commit messages
- Reference issues
- Keep changes focused
- Follow conventions

## Contributing

### Process
1. Fork repository
2. Create feature branch
3. Write code and tests
4. Submit pull request

### Standards
- PEP 8 compliance
- Documentation
- Test coverage
- Code review

## Troubleshooting

### Common Issues
1. Database migrations
2. Static files
3. Authentication
4. Deployment

### Debug Tools
- Django Debug Toolbar
- Logging
- Error tracking
- Performance profiling

## Resources

### Documentation
- Django docs
- Bootstrap docs
- Project wiki
- API reference

### Tools
- Development tools
- Testing tools
- Deployment tools
- Monitoring tools 