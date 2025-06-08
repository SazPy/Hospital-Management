# Hospital Management System - Use Cases and Sequence Diagrams

## Core Use Cases

### Admin Use Cases

| Use Case | Preconditions | Actions |
|----------|---------------|----------|
| Doctor Management | Admin is logged in | View, add, update, delete doctors; approve/reject registrations; view specializations & departments; track appointments; manage offices |
| Patient Management | Admin is logged in | View, add, update patients; approve/reject registrations; view details & appointments; manage discharge; track history; assign rooms |
| Room Management | Admin is logged in | View, add, update rooms; assign/change rooms; process requests; view occupancy; manage room types; track availability; handle maintenance |
| Appointment Management | Admin is logged in | View, schedule, approve/reject, cancel, reschedule appointments; view details, statistics, history; manage emergency appointments |
| System Administration | Admin is logged in | Manage user accounts; view statistics & audit logs; handle contact messages; monitor performance; configure departments & system parameters; backup |
| Billing Management | Admin is logged in | Generate bills; calculate charges; process doctor fees & medicine costs; handle additional charges & refunds; view payment history; generate reports |

### Doctor Use Cases

| Use Case | Preconditions | Actions |
|----------|---------------|----------|
| Patient Management | Doctor is logged in & approved | View/search assigned patients; view details, appointments, history; update medical records; add notes; handle emergencies; request tests |
| Appointment Management | Doctor is logged in & approved | View, approve/reject, cancel, reschedule appointments; set availability hours; manage follow-ups; view history & set priorities |
| Room Management | Doctor is logged in & approved | Request room/change for patients; specify room requirements; track request status; view available rooms & occupancy; manage office hours |
| Medical Records Management | Doctor is logged in & approved | Create/update patient records, diagnoses; prescribe meds; add notes; upload images; document allergies, vitals, lab results, procedures, prescriptions |
| Profile Management | Doctor is logged in & approved | Update personal info, contact details; manage specializations & working hours; view stats, performance metrics; manage notifications |

### Patient Use Cases

| Use Case | Preconditions | Actions |
|----------|---------------|----------|
| Appointment Management | Patient is logged in & approved | Book, view, cancel, reschedule appointments; search/view doctors; track status; view history; rate doctors; set reminders |
| Medical Records | Patient is logged in & approved | View medical history, prescriptions, treatment details; access discharge summary; track medications; download reports; view billing history |
| Room Management | Patient is logged in & approved | View assigned room/details/charges; request room change; track requests; submit feedback |
| Profile Management | Patient is logged in & approved | Update personal/contact/insurance/emergency info; manage notifications; view medical profile, treatment history, billing status |
| Communication | Patient is logged in & approved | Contact hospital; submit feedback/issues; request information; view announcements & doctor responses; track message history |

## Sequence Diagrams

### 1. Patient Registration and Approval

```mermaid
sequenceDiagram
    actor Patient
    participant UI
    participant Controller
    participant DB
    participant Admin
    participant Email

    Patient->>UI: Access registration page
    UI->>Controller: Show registration form
    Patient->>UI: Submit registration details
    UI->>Controller: Validate input
    Controller->>DB: Create patient account
    DB-->>Controller: Account created
    Controller->>Email: Send verification email
    Email-->>Patient: Receive verification
    
    Admin->>UI: View pending registrations
    UI->>Controller: Get pending list
    Controller->>DB: Fetch pending patients
    DB-->>Controller: Patient list
    Controller-->>UI: Display pending list
    
    Admin->>UI: Approve/Reject patient
    UI->>Controller: Update status
    Controller->>DB: Update patient status
    DB-->>Controller: Status updated
    Controller->>Email: Send approval notification
    Email-->>Patient: Receive approval
```

### 2. Doctor Appointment Workflow

```mermaid
sequenceDiagram
    actor Patient
    participant UI
    participant Controller
    participant DB
    participant Doctor
    participant Notification

    Patient->>UI: Search available doctors
    UI->>Controller: Get doctor list
    Controller->>DB: Query doctors
    DB-->>Controller: Doctor list
    Controller-->>UI: Display doctors
    
    Patient->>UI: Select doctor & book
    UI->>Controller: Submit appointment
    Controller->>DB: Create appointment
    DB-->>Controller: Appointment created
    Controller->>Notification: Notify doctor
    
    Doctor->>UI: View appointment request
    UI->>Controller: Get appointment details
    Controller->>DB: Fetch appointment
    DB-->>Controller: Appointment data
    
    Doctor->>UI: Approve/Reject
    UI->>Controller: Update status
    Controller->>DB: Save decision
    Controller->>Notification: Notify patient
    Notification-->>Patient: Receive notification
```

### 3. Room Assignment Process

```mermaid
sequenceDiagram
    actor Doctor
    participant UI
    participant Controller
    participant DB
    participant Admin
    participant Patient

    Doctor->>UI: Request room
    UI->>Controller: Submit request
    Controller->>DB: Create room request
    DB-->>Controller: Request created
    Controller->>Admin: Notify new request
    
    Admin->>UI: View room requests
    UI->>Controller: Get request details
    Controller->>DB: Fetch requests
    DB-->>Controller: Request data
    
    Admin->>UI: Check room availability
    UI->>Controller: Query available rooms
    Controller->>DB: Get room status
    DB-->>Controller: Available rooms
    
    Admin->>UI: Assign room
    UI->>Controller: Update assignment
    Controller->>DB: Save room assignment
    Controller->>DB: Update room status
    DB-->>Controller: Assignment saved
    
    Controller->>Doctor: Notify approval
    Controller->>Patient: Notify room assignment
```

### 4. Medical Record Management

```mermaid
sequenceDiagram
    actor Doctor
    participant UI
    participant Controller
    participant DB
    participant Storage
    participant Patient

    Doctor->>UI: Access patient records
    UI->>Controller: Get patient history
    Controller->>DB: Fetch medical records
    DB-->>Controller: Patient timeline
    Controller-->>UI: Display records
    
    Doctor->>UI: Update record
    UI->>Controller: Submit update
    
    alt Has Images
        Controller->>Storage: Upload images
        Storage-->>Controller: Image URLs
    end
    
    Controller->>DB: Save new record
    DB-->>Controller: Record saved
    Controller-->>UI: Show confirmation
    Controller->>Patient: Notify record update
```

### 5. Patient Discharge Process

```mermaid
sequenceDiagram
    actor Admin
    participant UI
    participant Controller
    participant DB
    participant Billing
    participant Patient

    Admin->>UI: Initiate discharge
    UI->>Controller: Get patient details
    Controller->>DB: Fetch admission data
    DB-->>Controller: Patient records
    
    Controller->>Billing: Calculate charges
    Billing->>DB: Get room charges
    Billing->>DB: Get doctor fees
    Billing->>DB: Get medicine costs
    Billing-->>Controller: Total bill
    
    Controller-->>UI: Display discharge form
    Admin->>UI: Confirm discharge
    
    UI->>Controller: Submit discharge
    Controller->>DB: Create discharge record
    Controller->>DB: Update patient status
    Controller->>DB: Update room status
    
    Controller->>Patient: Send discharge summary
    Controller->>Billing: Generate final bill
    Billing-->>Patient: Receive bill
```

### 6. Emergency Appointment Handling

```mermaid
sequenceDiagram
    actor Patient
    participant UI
    participant Controller
    participant DB
    participant Doctor
    participant Emergency

    Patient->>UI: Request emergency appointment
    UI->>Controller: Submit emergency request
    Controller->>Emergency: Flag as urgent
    
    Emergency->>DB: Find available doctors
    DB-->>Emergency: Doctor list
    Emergency->>Doctor: Send urgent notification
    
    Doctor->>UI: View emergency request
    UI->>Controller: Get request details
    Controller->>DB: Fetch request data
    DB-->>Controller: Request details
    
    Doctor->>UI: Accept emergency
    UI->>Controller: Update status
    Controller->>DB: Save emergency slot
    Controller->>Patient: Send immediate notification
```

### 7. System Monitoring and Reporting

```mermaid
sequenceDiagram
    actor Admin
    participant UI
    participant Controller
    participant DB
    participant Analytics
    participant Reports

    Admin->>UI: Access dashboard
    UI->>Controller: Request statistics
    Controller->>DB: Query system data
    DB-->>Controller: Raw data
    
    Controller->>Analytics: Process metrics
    Analytics-->>Controller: System statistics
    Controller-->>UI: Display dashboard
    
    Admin->>UI: Generate report
    UI->>Controller: Request report type
    Controller->>DB: Fetch report data
    DB-->>Controller: Report data
    
    Controller->>Reports: Generate PDF
    Reports-->>Controller: PDF report
    Controller-->>Admin: Download report
```

### 8. Contact Message Management

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant Controller
    participant DB
    participant Admin
    participant Email

    User->>UI: Submit contact form
    UI->>Controller: Send message
    Controller->>DB: Save message
    Controller->>Email: Send notification
    Email-->>Admin: Notify new message
    
    Admin->>UI: View messages
    UI->>Controller: Get message list
    Controller->>DB: Fetch messages
    DB-->>Controller: Message data
    Controller-->>UI: Display messages
    
    Admin->>UI: Process message
    UI->>Controller: Update status
    Controller->>DB: Mark as processed
    Controller->>Email: Send response
    Email-->>User: Receive response
```

### 9. Profile Management

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant Controller
    participant DB
    participant Storage
    participant Validator

    User->>UI: Access profile
    UI->>Controller: Get profile data
    Controller->>DB: Fetch user details
    DB-->>Controller: User data
    Controller-->>UI: Display profile
    
    User->>UI: Update information
    UI->>Controller: Submit changes
    Controller->>Validator: Validate input
    
    alt Has New Image
        Controller->>Storage: Upload profile pic
        Storage-->>Controller: Image URL
    end
    
    Controller->>DB: Save changes
    DB-->>Controller: Update successful
    Controller-->>UI: Show confirmation
```

### 10. Billing and Payment Processing

```mermaid
sequenceDiagram
    actor Admin
    participant UI
    participant Controller
    participant DB
    participant Billing
    participant Patient

    Admin->>UI: Generate bill
    UI->>Controller: Calculate charges
    Controller->>DB: Get service details
    DB-->>Controller: Service data
    
    Controller->>Billing: Process charges
    Billing->>DB: Get rate card
    Billing-->>Controller: Final amount
    
    Controller-->>UI: Display bill
    Admin->>UI: Confirm bill
    
    UI->>Controller: Save bill
    Controller->>DB: Store bill details
    Controller->>Patient: Send bill notification
    
    Patient->>UI: View bill
    UI->>Controller: Get bill details
    Controller->>DB: Fetch bill
    DB-->>Controller: Bill data
    Controller-->>UI: Show bill details
```

## System Features

### Authentication & Authorization
1. Role-based access control (Admin/Doctor/Patient)
2. Login with username/password
3. Session management
4. Access restrictions based on user role

### Data Management
1. Patient records with medical history
2. Doctor profiles with specializations
3. Room management with types (Ward/Private/ICU/Office)
4. Appointment scheduling system

### Security Features
1. Password hashing
2. CSRF protection
3. Form validation
4. Secure file uploads
5. Audit logging

### User Interface
1. Responsive dashboard for each role
2. Search functionality
3. Sorting and filtering
4. Status tracking
5. Notifications system