# API Documentation

This document outlines the available API endpoints in the Hospital Management System.

## Authentication

All API endpoints require authentication unless explicitly marked as public.

### Authentication Methods

1. Session Authentication (Web Interface)
2. Token Authentication (API Access)

To obtain an authentication token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

Include the token in request headers:
```
Authorization: Token your_token_here
```

## API Endpoints

### User Management

#### Register User
```
POST /api/register/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "string" (admin|doctor|patient)
}
```

#### User Profile
```
GET /api/profile/
Authorization: Token your_token_here
```

### Patient APIs

#### List Patients
```
GET /api/patients/
Query Parameters:
- search: string
- status: boolean
- doctor_id: integer
```

#### Patient Details
```
GET /api/patients/{id}/
```

#### Create Patient
```
POST /api/patients/
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "symptoms": "string"
}
```

#### Update Patient
```
PUT /api/patients/{id}/
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "symptoms": "string"
}
```

### Doctor APIs

#### List Doctors
```
GET /api/doctors/
Query Parameters:
- department: string
- status: boolean
```

#### Doctor Details
```
GET /api/doctors/{id}/
```

#### Create Doctor
```
POST /api/doctors/
{
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "department": "string",
    "specialization": "string"
}
```

### Appointment APIs

#### List Appointments
```
GET /api/appointments/
Query Parameters:
- doctor_id: integer
- patient_id: integer
- status: string
- date: date
```

#### Create Appointment
```
POST /api/appointments/
{
    "doctor_id": integer,
    "patient_id": integer,
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "description": "string"
}
```

#### Update Appointment Status
```
PATCH /api/appointments/{id}/
{
    "status": "string" (approved|rejected|cancelled)
}
```

### Room Management

#### List Rooms
```
GET /api/rooms/
Query Parameters:
- type: string
- status: string
```

#### Room Details
```
GET /api/rooms/{id}/
```

#### Assign Room
```
POST /api/rooms/assign/
{
    "room_id": integer,
    "patient_id": integer
}
```

### Medical Records

#### Patient Records
```
GET /api/patients/{id}/records/
```

#### Add Medical Record
```
POST /api/patients/{id}/records/
{
    "diagnosis": "string",
    "prescription": "string",
    "notes": "string"
}
```

## Response Formats

### Success Response
```json
{
    "status": "success",
    "data": {
        // Response data
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "errors": [
        // Detailed error messages
    ]
}
```

## Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Rate Limiting

API requests are limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

## Pagination

List endpoints support pagination with these parameters:
- page: Page number (default: 1)
- limit: Items per page (default: 10, max: 100)

Example:
```
GET /api/patients/?page=2&limit=20
```

## Filtering and Sorting

Most list endpoints support:
- Filtering via query parameters
- Sorting via `sort` parameter
- Search via `search` parameter

Example:
```
GET /api/doctors/?department=cardiology&sort=-created_at&search=smith
```

## API Versioning

The API is versioned through URL prefixing:
- Current version: v1
- Base URL: `/api/v1/`

## Development and Testing

### Testing Endpoints
```bash
# Using curl
curl -H "Authorization: Token your_token" http://localhost:8000/api/patients/

# Using httpie
http GET http://localhost:8000/api/patients/ "Authorization: Token your_token"
```

### Postman Collection
A Postman collection is available at `/docs/postman/hospital-api.json`

## Error Handling

The API uses standard HTTP status codes and returns detailed error messages:

```json
{
    "status": "error",
    "code": "INVALID_INPUT",
    "message": "Invalid input data",
    "details": {
        "field": ["Error description"]
    }
}
```

## Security

- All endpoints use HTTPS
- Rate limiting prevents abuse
- Token expiration: 24 hours
- CORS configuration required for external access

## Support

For API support:
- Email: api-support@hospital.com
- Documentation: /docs/api/
- Issue tracker: GitHub Issues 