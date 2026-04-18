# System Architecture

## Overview

The Online Exam Registration System follows a three-tier architecture with clear separation of concerns:

1. **Presentation Layer** (Frontend - React)
2. **Application Layer** (Backend - FastAPI)
3. **Data Layer** (Database - PostgreSQL)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Pages   │  │Components│  │ Services │  │   Auth   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP/REST API (JWT)
                            │
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   API    │  │  Models  │  │ Schemas  │  │   Core   │   │
│  │  Routes  │  │   ORM    │  │Validation│  │ Security │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                      SQLAlchemy ORM
                            │
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │ Students │  │  Exams   │  │Payments  │   │
│  │  Admins  │  │  Regs    │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Architecture

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Navbar.js       # Navigation bar
│   │   └── ProtectedRoute.js # Route protection
│   ├── pages/              # Page components
│   │   ├── Home.js         # Landing page
│   │   ├── Login.js        # Authentication
│   │   ├── Register.js     # User registration
│   │   ├── Dashboard.js    # Student dashboard
│   │   ├── Exams.js        # Exam listing
│   │   ├── MyRegistrations.js
│   │   ├── Payment.js      # Payment processing
│   │   ├── AdminDashboard.js
│   │   ├── ManageExams.js  # Admin exam management
│   │   ├── AdminRegistrations.js
│   │   └── AdminStudents.js
│   ├── services/           # API integration
│   │   ├── api.js          # Axios configuration
│   │   └── auth.js         # Auth utilities
│   └── App.js              # Main app component
```

### Backend Architecture

```
backend/
├── app/
│   ├── api/                # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   ├── exams.py        # Exam routes
│   │   ├── registrations.py
│   │   ├── payments.py
│   │   ├── admin.py        # Admin routes
│   │   └── dependencies.py # Route dependencies
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration
│   │   ├── security.py     # JWT & password hashing
│   │   └── database.py     # Database connection
│   ├── models/             # Database models
│   │   └── models.py       # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   │   └── schemas.py      # Request/response models
│   └── main.py             # Application entry point
```

### Database Schema

```
users (Authentication)
├── id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
├── password_hash
├── role (student/admin)
└── created_at

students (Student Profiles)
├── student_id (PK)
├── user_id (FK → users.id)
├── name
├── email
├── branch
├── year
└── created_at

admins (Admin Profiles)
├── admin_id (PK)
├── user_id (FK → users.id)
├── name
├── email
└── created_at

exams (Exam Information)
├── exam_id (PK)
├── exam_name
├── subject
├── exam_date
├── duration
├── total_marks
├── fee
├── is_active
└── created_at

registrations (Exam Registrations)
├── registration_id (PK)
├── student_id (FK → students.student_id)
├── exam_id (FK → exams.exam_id)
├── status (pending/confirmed/cancelled)
├── registration_date
└── UNIQUE(student_id, exam_id)

payments (Payment Records)
├── payment_id (PK)
├── registration_id (FK → registrations.registration_id)
├── amount
├── payment_status (pending/completed/failed)
├── payment_date
└── transaction_id
```

## Security Architecture

### Authentication Flow

1. User submits credentials
2. Backend validates credentials
3. Backend generates JWT token
4. Frontend stores token in localStorage
5. Frontend includes token in all API requests
6. Backend validates token for protected routes

### Authorization

- Role-based access control (RBAC)
- Student role: Access to exams, registrations, payments
- Admin role: Full access to manage system

### Security Measures

- Password hashing using bcrypt
- JWT token-based authentication
- HTTPS recommended for production
- Input validation using Pydantic
- SQL injection prevention via ORM
- CORS configuration
- Unique constraints to prevent duplicate registrations

## Data Flow

### Student Registration Flow

```
1. Student → Register Page
2. Submit Form → POST /auth/register/student
3. Backend → Hash Password
4. Backend → Create User & Student Records
5. Backend → Return Success
6. Frontend → Redirect to Login
```

### Exam Registration Flow

```
1. Student → View Exams
2. GET /exams → Backend → Return Active Exams
3. Student → Click Register
4. POST /registrations → Backend
5. Backend → Validate (no duplicate, exam active)
6. Backend → Create Registration (status: pending)
7. Frontend → Redirect to Payment
8. POST /payments → Backend
9. Backend → Process Payment (simulated)
10. Backend → Update Registration (status: confirmed)
11. Frontend → Show Success
```

### Admin Exam Management Flow

```
1. Admin → Login
2. Admin → Manage Exams
3. GET /admin/exams → Backend → Return All Exams
4. Admin → Add/Edit/Delete Exam
5. POST/PUT/DELETE /admin/exams/{id}
6. Backend → Validate Admin Role
7. Backend → Perform Operation
8. Backend → Return Updated Data
```

## API Endpoints

### Authentication
- POST /auth/register/student
- POST /auth/register/admin
- POST /auth/login

### Student Endpoints
- GET /exams
- POST /registrations
- GET /registrations/my-registrations
- POST /payments
- GET /payments/my-payments

### Admin Endpoints
- POST /admin/exams
- PUT /admin/exams/{id}
- DELETE /admin/exams/{id}
- GET /admin/exams
- GET /admin/students
- GET /admin/registrations

## Technology Stack

### Frontend
- React 18.2
- React Router 6.20
- Axios 1.6
- CSS3 (Custom styling)

### Backend
- FastAPI 0.104
- SQLAlchemy 2.0
- Pydantic 2.5
- Python-Jose (JWT)
- Passlib (Password hashing)
- Uvicorn (ASGI server)

### Database
- PostgreSQL 12+
- Relational schema with foreign keys
- Indexes for performance

## Scalability Considerations

1. **Database**: Use connection pooling
2. **Backend**: Horizontal scaling with load balancer
3. **Frontend**: CDN for static assets
4. **Caching**: Redis for session management
5. **File Storage**: S3 for documents/certificates
6. **Monitoring**: Application performance monitoring
7. **Logging**: Centralized logging system

## Future Enhancements

1. Email notifications
2. PDF certificate generation
3. Real payment gateway integration
4. Exam schedule calendar
5. Student performance analytics
6. Bulk exam upload
7. Export reports to Excel/PDF
8. Two-factor authentication
9. Password reset functionality
10. Mobile responsive improvements
