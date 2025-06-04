# Hospital Management System

A comprehensive hospital management system built with Django that streamlines healthcare facility operations by managing doctors, patients, appointments, and room allocations.

![Hospital Management System](static/screenshots/dashboard.png)

## 🌟 Key Features

- **Multi-User System**
  - Role-based access control (Admin, Doctor, Patient)
  - Secure authentication and authorization
  - Custom dashboards for each user type

- **Patient Management**
  - Patient registration and records
  - Medical history tracking
  - Appointment scheduling
  - Discharge management
  - Digital medical records

- **Doctor Management**
  - Doctor registration and profiles
  - Specialization tracking
  - Appointment management
  - Patient assignment

- **Appointment System**
  - Online booking
  - Approval workflow
  - Schedule management
  - Email notifications
  - Appointment history

- **Room Management**
  - Room allocation
  - Occupancy tracking
  - Room types and capacity
  - Patient assignment

- **Administrative Tools**
  - User approval system
  - Report generation
  - System monitoring
  - Settings management

## 📋 Prerequisites

- Python 3.8 or higher
- Django 5.0 or higher
- SQLite (default) or PostgreSQL
- Modern web browser

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hospital-management.git
   cd hospital-management
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

5. **Initialize database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

## 📚 Documentation

Detailed documentation is available in the [docs](docs/) directory:

- [User Guide](docs/user-guide.md)
  - [Admin Manual](docs/admin-guide.md)
  - [Doctor Manual](docs/doctor-guide.md)
  - [Patient Manual](docs/patient-guide.md)
- [Developer Guide](docs/developer-guide.md)
  - [Setup Guide](docs/setup-guide.md)
  - [API Documentation](docs/api-docs.md)
  - [Database Schema](docs/database-schema.md)
- [Contributing Guide](docs/contributing.md)
- [Deployment Guide](docs/deployment.md)

## 🏗️ Project Structure

```
hospital-management/
├── hospital/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   └── admin.py             # Admin interface
├── templates/               # HTML templates
│   └── hospital/           # App-specific templates
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── img/               # Images
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── manage.py             # Django management
```

## 🔒 Security

- Built-in Django security features
- CSRF protection
- Password hashing
- Session security
- XSS prevention
- SQL injection protection

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django Team
- Bootstrap Team
- All contributors 