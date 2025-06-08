# Deployment Guide

This guide covers deploying the Hospital Management System to various environments.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Nginx or Apache
- SSL certificate
- Domain name
- Linux server (Ubuntu 20.04+ recommended)

## Deployment Options

1. Traditional Server Deployment
2. Docker Deployment
3. Platform as a Service (PaaS)

## 1. Traditional Server Deployment

### Server Setup

1. Update system:
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Install dependencies:
   ```bash
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   sudo apt install supervisor
   ```

3. Create database:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE hospital_db;
   CREATE USER hospital_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
   ```

### Application Setup

1. Create application user:
   ```bash
   sudo useradd -m -s /bin/bash hospital
   sudo su - hospital
   ```

2. Clone repository:
   ```bash
   git clone https://github.com/yourusername/hospital-management.git
   cd hospital-management
   ```

3. Set up virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   nano .env
   ```
   ```env
   DEBUG=False
   SECRET_KEY=your-secure-key
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgres://hospital_user:secure_password@localhost:5432/hospital_db
   STATIC_ROOT=/var/www/hospital/static
   MEDIA_ROOT=/var/www/hospital/media
   ```

5. Initialize application:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Gunicorn Setup

1. Create Gunicorn service:
   ```bash
   sudo nano /etc/supervisor/conf.d/hospital.conf
   ```
   ```ini
   [program:hospital]
   command=/home/hospital/hospital-management/.venv/bin/gunicorn hospitalmanagement.wsgi:application -w 4 -b 127.0.0.1:8000
   directory=/home/hospital/hospital-management
   user=hospital
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/hospital/gunicorn.err.log
   stdout_logfile=/var/log/hospital/gunicorn.out.log
   ```

2. Create log directory:
   ```bash
   sudo mkdir /var/log/hospital
   sudo chown -R hospital:hospital /var/log/hospital
   ```

3. Start Gunicorn:
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start hospital
   ```

### Nginx Setup

1. Create Nginx configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/hospital
   ```
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

       location = /favicon.ico { access_log off; log_not_found off; }

       location /static/ {
           root /var/www/hospital;
       }

       location /media/ {
           root /var/www/hospital;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/hospital /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 2. Docker Deployment

1. Create Dockerfile:
   ```dockerfile
   FROM python:3.8-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .

   CMD ["gunicorn", "hospitalmanagement.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. Create docker-compose.yml:
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       command: gunicorn hospitalmanagement.wsgi:application --bind 0.0.0.0:8000
       volumes:
         - .:/app
         - static_volume:/app/staticfiles
         - media_volume:/app/media
       expose:
         - 8000
       env_file:
         - .env
       depends_on:
         - db
     
     db:
       image: postgres:12
       volumes:
         - postgres_data:/var/lib/postgresql/data
       environment:
         - POSTGRES_DB=hospital_db
         - POSTGRES_USER=hospital_user
         - POSTGRES_PASSWORD=secure_password
     
     nginx:
       image: nginx:latest
       volumes:
         - static_volume:/app/staticfiles
         - media_volume:/app/media
         - ./nginx.conf:/etc/nginx/conf.d/default.conf
       ports:
         - "80:80"
       depends_on:
         - web

   volumes:
     postgres_data:
     static_volume:
     media_volume:
   ```

3. Deploy with Docker:
   ```bash
   docker-compose up -d --build
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py collectstatic
   docker-compose exec web python manage.py createsuperuser
   ```

## 3. PaaS Deployment (Heroku Example)

1. Install Heroku CLI:
   ```bash
   curl https://cli-heroku.com/install.sh | sh
   ```

2. Create Procfile:
   ```
   web: gunicorn hospitalmanagement.wsgi
   release: python manage.py migrate
   ```

3. Configure Heroku:
   ```bash
   heroku create hospital-app
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set SECRET_KEY=your-secure-key
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   heroku config:set DEBUG=False
   ```

4. Deploy to Heroku:
   ```bash
   git push heroku main
   heroku run python manage.py createsuperuser
   ```

## Security Considerations

1. SSL/TLS Configuration
   ```nginx
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
   ssl_prefer_server_ciphers on;
   ssl_session_cache shared:SSL:10m;
   ssl_session_timeout 10m;
   ```

2. File Permissions:
   ```bash
   chmod 600 .env
   chmod 644 manage.py
   find . -type d -exec chmod 755 {} \;
   find . -type f -exec chmod 644 {} \;
   ```

3. Database Backup:
   ```bash
   # Create backup
   pg_dump hospital_db > backup.sql

   # Restore backup
   psql hospital_db < backup.sql
   ```

## Monitoring

1. Install monitoring tools:
   ```bash
   pip install sentry-sdk
   pip install django-prometheus
   ```

2. Configure logging:
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'ERROR',
               'class': 'logging.FileHandler',
               'filename': '/var/log/hospital/django.log',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'ERROR',
               'propagate': True,
           },
       },
   }
   ```

## Maintenance

1. Database maintenance:
   ```bash
   # Vacuum database
   psql hospital_db -c "VACUUM ANALYZE;"
   
   # Reindex database
   psql hospital_db -c "REINDEX DATABASE hospital_db;"
   ```

2. Update application:
   ```bash
   git pull origin main
   source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   sudo supervisorctl restart hospital
   ```

## Troubleshooting

1. Check logs:
   ```bash
   tail -f /var/log/hospital/gunicorn.err.log
   tail -f /var/log/nginx/error.log
   ```

2. Test database connection:
   ```bash
   python manage.py dbshell
   ```

3. Check services:
   ```bash
   sudo systemctl status nginx
   sudo supervisorctl status
   ```

## Backup Strategy

1. Database backups:
   ```bash
   # Daily backups
   0 0 * * * pg_dump hospital_db > /backup/db/hospital_$(date +\%Y\%m\%d).sql

   # Rotate backups (keep last 30 days)
   find /backup/db/ -mtime +30 -delete
   ```

2. Media backups:
   ```bash
   # Weekly media backups
   0 0 * * 0 tar -czf /backup/media/hospital_media_$(date +\%Y\%m\%d).tar.gz /var/www/hospital/media
   ```

## Performance Optimization

1. Enable caching:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. Configure static file serving:
   ```nginx
   location /static/ {
       expires 30d;
       add_header Cache-Control "public, no-transform";
   }
   ```

## Support

For deployment support:
- Check server logs
- Review documentation
- Contact system administrator
- Open support ticket 