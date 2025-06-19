# System Diagrams

## Context Diagram

```mermaid
graph TD
    %% Style Definitions
    classDef entity fill:,stroke:#333,stroke-width:1.5px;
    classDef system fill:,stroke:#000,stroke-width:2px;
    classDef flow font-style: italic, font-size: 12px;

    %% External Entities
    P[Patient]:::entity
    D[Doctor]:::entity
    A[Admin]:::entity

    %% Central System
    OpenMed([Hospital Information System]):::system

    %% Data Flows: Patient
    P -->|Register / Login| OpenMed
    P -->|Book Appointment| OpenMed
    P -->|View Medical Records| OpenMed
    P -->|View Bill / Make Payment| OpenMed
    P -->|Contact Messages| OpenMed
    OpenMed -->|Notifications / Confirmations| P

    %% Data Flows: Doctor
    D -->|Manage Patients| OpenMed
    D -->|Accept / Reject Appointments| OpenMed
    D -->|Update Records| OpenMed
    OpenMed -->|Reminders / Schedules| D

    %% Data Flows: Admin
    A -->|System Management| OpenMed
    A -->|Discharge / Assign Rooms| OpenMed
    A -->|Generate Reports / Billing| OpenMed
    OpenMed -->|Logs / Notifications| A

```


## Data Flow Diagram (Level 0)

```mermaid
---
config:
  layout: elk
---
flowchart TD
    Patient(("Patient")) -- Register/Login/Update --> P1["1 User Management"]
    P1 -- User Data/Responses --> Patient & Doctor(("Doctor")) & Admin(("Admin"))
    Patient -- Search/View/Book Appt --> P2["2 Appointment System"]
    P2 -- Appt Data/Confirmations --> Patient
    Patient -- Access Medical Records --> P3["3 Patient Management"]
    P3 -- Medical Data --> Patient & Doctor & Admin
    Patient -- Request Room --> P4["4 Room Management"]
    P4 -- Room Data --> Patient & Admin
    Patient -- Receive Notifications --> P5["5 Communication Services"]
    P5 -- Send Notifications --> Patient
    Patient -- Request Bill --> P6["6 Bill Generating System"]
    P6 -- Bill Data/Invoice --> Patient
    Doctor -- Manage Profile/Appointments/Records --> P1
    Doctor -- View/Manage Appointments --> P2
    P2 -- Appt Data --> Doctor & Admin
    Doctor -- Add/View Patient Records --> P3
    Admin -- Manage Users/Doctors/Patients --> P1
    Admin -- Manage Appointments --> P2
    Admin -- Manage Patient Data --> P3
    Admin -- Manage Rooms --> P4
    Admin -- Manage Communication --> P5
    P5 -- Notifications --> Admin
    Admin -- Manage Bills --> P6
    P6 -- Billing Data --> Admin
    P1 <--> DB1[("User DB")]
    P2 <--> DB2[("Medical DB")]
    P3 <--> DB2
    P4 <--> DB2
    P5 <--> DB4[("Audit Logs")]
    P6 <--> DB3[("Billing DB")] & FS["File Store"]

```
## Data Flow Diagram (Level 1)
# 1. User Management
```mermaid
graph TD
    Patient((Patient))
    Doctor((Doctor))
    Admin((Admin))
    
    P1_1[1.1 User Registration]
    P1_2[1.2 User Login Authentication]
    P1_3[1.3 Profile Management]
    P1_4[1.4 Access Control]

    DB1[(User DB)]

    Patient -->|Register| P1_1
    Doctor -->|Register| P1_1
    Admin -->|Manage Users| P1_1
    P1_1 -->|Store User Data| DB1
    P1_1 -->|Registration Confirmation| Patient
    P1_1 -->|Registration Confirmation| Doctor

    Patient -->|Login| P1_2
    Doctor -->|Login| P1_2
    P1_2 -->|Authenticate| DB1
    P1_2 -->|Login Response Success/Fail| Patient
    P1_2 -->|Login Response Success/Fail| Doctor

    Patient -->|Update Profile| P1_3
    Doctor -->|Update Profile| P1_3
    P1_3 -->|Update Profile Data| DB1
    P1_3 -->|Profile Update Confirmation| Patient
    P1_3 -->|Profile Update Confirmation| Doctor

    P1_4 -->|Verify Permissions| DB1

```

# 2. Appointment System

```mermaid
graph TD
    Patient((Patient))
    Doctor((Doctor))
    Admin((Admin))

    P2_1[2.1 Choose Doctor]
    P2_2[2.2 Request Appointment]
    P2_3[2.3 Admin Schedule Appointment]
    P2_4[2.4 Doctor Approves/Rejects]
    P2_5[2.5 Appointment Confirmation Notification]

    DB2[(Medical DB)]

    %% Patient Flow
    Patient -->|Search/Select| P2_1
    P2_1 -->|Doctor Info| DB2

    Patient -->|Request Appointment| P2_2
    P2_2 -->|Store Request| DB2
    P2_2 -->|Forward Request| P2_4

    %% Admin Flow
    Admin -->|Create Appointment| P2_3
    P2_3 -->|Store Appointment| DB2
    P2_3 -->|Send Confirmation| P2_5

    %% Doctor Flow
    Doctor -->|Review Request| P2_4
    P2_4 -->|Update Status| DB2
    P2_4 -->|Send Response| P2_5

    %% Final Notification
    P2_5 -->|Notify Patient| Patient
    P2_5 -->|Notify Doctor| Doctor

```

# 3. Patient Management
```memraid
graph TD
    Patient((Patient))
    Doctor((Doctor))
    Admin((Admin))

    P3_1[3.1 Add/Update Medical Record]
    P3_2[3.2 View Medical History]
    P3_3[3.3 Manage Documents]
    P3_4[3.4 Discharge Patient]

    DB2[(Medical DB)]
    FS[File Store]

    %% Doctor Activities
    Doctor -->|Add/Edit Record| P3_1
    P3_1 -->|Store Record| DB2

    Doctor -->|View History| P3_2
    P3_2 -->|Fetch History| DB2
    P3_2 -->|Return Data| Doctor

    Doctor -->|Upload Files| P3_3
    P3_3 -->|Store Files| FS
    P3_3 -->|Confirm Upload| Doctor

    %% Patient View
    Patient -->|View History| P3_2
    P3_2 -->|Return Data| Patient

    Patient -->|View Documents| P3_3
    P3_3 -->|Fetch Files| FS
    P3_3 -->|Return Files| Patient

    %% Admin Discharge
    Admin -->|Discharge Patient| P3_4
    P3_4 -->|Update Discharge Info| DB2
    P3_4 -->|Generate Summary| FS
    P3_4 -->|Confirm Discharge| Admin
    P3_4 -->|Notify Patient| Patient

```

# 4. Room Management
```mermaid
graph TD
    Admin((Admin))
    Doctor((Doctor))

    P4_1[4.1 Allocate/Move Patient to Room]
    P4_2[4.2 Track Room Status]
    P4_3[4.3 Maintain Room Inventory]
    P4_4[4.4 Request Room for Patient]

    DB2[(Medical DB)]

    %% Doctor Requests
    Doctor -->|Request Room for Patient| P4_4
    P4_4 -->|Forward Request| P4_1

    %% Admin Allocates or Moves Patients
    Admin -->|Allocate/Move Patient| P4_1
    P4_1 -->|Update Room Assignment| DB2
    P4_1 -->|Room Assignment Confirmation| Admin

    %% Admin Tracks Room Status
    Admin -->|Track Room Usage| P4_2
    P4_2 -->|Fetch Room Data| DB2
    P4_2 -->|Room Status Info| Admin

    %% Admin Manages Room Inventory
    Admin -->|Update Inventory| P4_3
    P4_3 -->|Store Inventory Info| DB2
    P4_3 -->|Inventory Update Confirmation| Admin

```

# 5. Communication Services
```mermaid
graph TD
    Patient((Patient))
    Doctor((Doctor))
    Admin((Admin))

    P5[5 Communication Services]
    ContactUs[Contact Us Message Submission]

    %% Notifications
    P5 -->|Send Notifications| Patient
    P5 -->|Send Notifications| Doctor
    P5 -->|Send Notifications| Admin

    %% Contact Us Message Flow
    Patient -->|Send Message| ContactUs
    ContactUs -->|Forward to Admin| P5
    P5 -->|Deliver Message| Admin

```

# 6. Bill Generating system
```mermaid
graph TD
    %% External Entities
    Patient((Patient))
    Admin((Admin))

    %% From Patient Management (external trigger)
    P3_4[3.4 Discharge Patient]

    %% Billing Subprocesses
    P6_1[6.1 Generate Bill]
    P6_2[6.2 Review & Confirm Bill Details]
    P6_3[6.3 Generate Receipt]

    %% Data Stores
    DB3[(Billing DB)]
    FS[File Store]

    %% Trigger from Discharge
    P3_4 -->|Trigger Billing| P6_1

    %% Patient Flow
    Patient -->|Request Bill| P6_1
    P6_1 -->|Store Bill Data| DB3
    P6_1 -->|Billing Info| Patient

    %% Admin Flow
    Admin -->|Access Bill| P6_2
    P6_2 -->|Fetch & Confirm Details| DB3
    P6_2 -->|Billing Confirmation| Admin
    P6_2 -->|Trigger Receipt Creation| P6_3

    %% Receipt Generation
    P6_3 -->|Save Receipt| FS
    P6_3 -->|Send Receipt| Patient

```
## UI Navigation Tree

```mermaid
graph TD
    Home[Home Page]
    
    %% Main Sections
    Home -->|Login| Auth[Authentication]
    Home -->|About| About[About Us]
    Home -->|Contact| Contact[Contact Us]
    
    %% Authentication Branches
    Auth -->|Admin| AdminAuth[Admin Login]
    Auth -->|Doctor| DoctorAuth[Doctor Login]
    Auth -->|Patient| PatientAuth[Patient Login]
    Auth -->|Forgot| Reset[Password Reset]
    
    %% Admin Section
    AdminDash[Admin Dashboard]
    AdminAuth --> AdminDash
    AdminDash --> AD1[Doctor Management]
    AdminDash --> AD2[Patient Management]
    AdminDash --> AD3[Room Management]
    AdminDash --> AD4[Reports]
    AdminDash --> AD5[Messages]
    AdminDash --> AD6[System Config]
    
    %% Doctor Section
    DoctorDash[Doctor Dashboard]
    DoctorAuth --> DoctorDash
    DoctorDash --> DD1[My Patients]
    DoctorDash --> DD2[Appointments]
    DoctorDash --> DD3[Room Requests]
    DoctorDash --> DD4[Profile]
    DoctorDash --> DD5[Schedule]
    
    %% Patient Section
    PatientDash[Patient Dashboard]
    PatientAuth --> PatientDash
    PatientDash --> PD1[Book Appointment]
    PatientDash --> PD2[My Appointments]
    PatientDash --> PD3[Medical History]
    PatientDash --> PD4[Bills]
    PatientDash --> PD5[Profile]
    PatientDash --> PD6[Documents]
    
    %% Doctor Management
    AD1 --> DM1[View Doctors]
    AD1 --> DM2[Add Doctor]
    AD1 --> DM3[Approve Doctor]
    AD1 --> DM4[Schedule]
    
    %% Patient Management
    AD2 --> PM1[View Patients]
    AD2 --> PM2[Add Patient]
    AD2 --> PM3[Medical Records]
    AD2 --> PM4[Billing]
    
    %% Room Management
    AD3 --> RM1[View Rooms]
    AD3 --> RM2[Assign Room]
    AD3 --> RM3[Maintenance]
    AD3 --> RM4[Room Types]
```


## Data Store Details

```mermaid
graph TD
    subgraph User Data Store
        UD1[Users Table]
        UD2[Roles Table]
        UD3[Permissions Table]
        UD4[Sessions Table]
    end
    
    subgraph Medical Data Store
        MD1[Patient Records]
        MD2[Medical History]
        MD3[Prescriptions]
        MD4[Lab Results]
    end
    
    subgraph Appointment Data Store
        AD1[Appointments]
        AD2[Schedules]
        AD3[Time Slots]
        AD4[Notifications]
    end
    
    subgraph Billing Data Store
        BD1[Bills]
        BD2[Payments]
        BD3[Insurance]
        BD4[Receipts]
    end
    
    subgraph Room Data Store
        RD1[Rooms]
        RD2[Room Types]
        RD3[Assignments]
        RD4[Maintenance]
    end
    
    subgraph Audit Data Store
        AUD1[Access Logs]
        AUD2[Change Logs]
        AUD3[Error Logs]
        AUD4[Security Logs]
    end
```