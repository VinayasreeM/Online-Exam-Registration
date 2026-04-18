# Online Exam Registration System

A full-stack web application for exam registration built with React, FastAPI, and PostgreSQL.

---

## Prerequisites

Make sure you have these installed before starting:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/download/)

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

---

## Step 2 — Database Setup

1. Open **pgAdmin** or **psql** and create a new database:

```sql
CREATE DATABASE exam_registration;
```

2. Run the schema file to create all tables:

```bash
psql -U postgres -d exam_registration -f database/schema.sql
```

> If psql is not in your PATH, find it at:
> - Windows: `C:\Program Files\PostgreSQL\<version>\bin\psql.exe`
> - Mac/Linux: it should be available directly

---

## Step 3 — Backend Setup

```bash
cd backend
```

Create a virtual environment and activate it:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart pydantic pydantic-settings python-dotenv email-validator bcrypt
```

Create your `.env` file:

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` and update your PostgreSQL password:

```
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/exam_registration
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Create the admin accounts in the database:

```bash
python create_admins.py
```

Start the backend server:

```bash
python -m uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**

---

## Step 4 — Frontend Setup

Open a **new terminal** and go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm start
```

Frontend will open at: **http://localhost:3000**

---

## Step 5 — Using the Application

### Student
- Go to http://localhost:3000
- Click **Register** to create a student account
- Login with your **email or username** + password
- Browse exams, register, and make payments

### Admin
- Go to http://localhost:3000/admin/login
- Login with your admin email and password

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, security, database
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── main.py       # App entry point
│   ├── create_admins.py  # Script to seed admin accounts
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Navbar, ProtectedRoute
│   │   ├── pages/        # All page components
│   │   └── services/     # API and auth utilities
│   └── package.json
└── database/
    └── schema.sql        # Database schema
```

---

## Troubleshooting

**psql not recognized on Windows**

Add PostgreSQL to your PATH or use the full path:
```bash
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d exam_registration -f database/schema.sql
```

**Database connection error**

Make sure PostgreSQL is running and the password in `.env` matches your PostgreSQL password.

**Port already in use**

```bash
# Kill port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Module not found errors**

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Frontend | React, React Router, Axios |
| Backend  | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL          |
| Auth     | JWT, bcrypt         |
