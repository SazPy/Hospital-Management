# Setup Guide

This guide provides detailed instructions for setting up the Hospital Management System for development and testing.

## System Requirements

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git
- SQLite3 (included with Python) or PostgreSQL
- A modern web browser (Chrome, Firefox, Safari, or Edge)

### Hardware Requirements
- Minimum 2GB RAM
- 1GB free disk space
- 1GHz processor or better

## Development Environment Setup

### 1. Python Installation

1. Download Python from [python.org](https://python.org)
2. During installation:
   - Check "Add Python to PATH"
   - Enable pip installation
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### 2. Database Setup

#### SQLite (Default)
- No additional setup required
- Included with Python
- Suitable for development

#### PostgreSQL (Optional)
1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE hospital_management;
   CREATE USER hospital_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE hospital_management TO hospital_user;
   ```
3. Update settings.py with PostgreSQL configuration

### 3. Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hospital-management.git
   cd hospital-management
   ```

2. Create and activate virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Environment configuration:
   ```bash
   # Create .env file
   cp .env.example .env

   # Edit with your settings
   # Required variables:
   # SECRET_KEY=your_secret_key
   # DEBUG=True
   # ALLOWED_HOSTS=localhost,127.0.0.1
   # DATABASE_URL=sqlite:///db.sqlite3
   ```

5. Initialize database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```

7. Run development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application:
   - Admin interface: http://127.0.0.1:8000/admin/
   - Main application: http://127.0.0.1:8000/

## Configuration Options

### Email Settings
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

### Static Files
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

### Media Files
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Development Tools

### Recommended IDE
- Visual Studio Code with Python extension
- PyCharm Community/Professional Edition

### VS Code Extensions
- Python
- Django
- GitLens
- SQLite Viewer

### Browser Extensions
- Django Debug Toolbar
- React Developer Tools (if using React components)

## Troubleshooting

### Common Issues

1. Database migrations:
   ```bash
   python manage.py migrate --run-syncdb
   ```

2. Static files not loading:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. Port already in use:
   ```bash
   # Use different port
   python manage.py runserver 8001
   ```

4. Dependencies conflicts:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

### Getting Help
- Check Django documentation
- Search Stack Overflow
- Open an issue on GitHub
- Contact project maintainers

## Next Steps

- Read the [API Documentation](api-docs.md)
- Review the [Database Schema](database-schema.md)
- Check the [Contributing Guide](contributing.md) 