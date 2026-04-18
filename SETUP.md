# Setup Instructions

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

## Database Setup

1. Install PostgreSQL and create a database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE exam_registration;

# Exit PostgreSQL
\q
```

2. Run the schema:

```bash
psql -U postgres -d exam_registration -f database/schema.sql
```

## Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```bash
copy .env.example .env
```

5. Update `.env` with your database credentials:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/exam_registration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Run the backend server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The application will open at: http://localhost:3000

## Testing the Application

### Create Admin Account

1. Go to http://localhost:3000/register
2. Select "Admin" tab
3. Fill in the form:
   - Username: admin
   - Email: admin@example.com
   - Password: admin123
   - Full Name: Admin User
4. Click Register
5. Login with admin credentials

### Create Student Account

1. Go to http://localhost:3000/register
2. Select "Student" tab
3. Fill in the form:
   - Username: student1
   - Email: student1@example.com
   - Password: student123
   - Full Name: John Doe
   - Branch: Computer Science
   - Year: 3
4. Click Register
5. Login with student credentials

### Admin Workflow

1. Login as admin
2. Go to "Manage Exams"
3. Click "Add New Exam"
4. Fill in exam details
5. View registrations and students

### Student Workflow

1. Login as student
2. View available exams
3. Click "Register" on an exam
4. Complete payment
5. View registration status

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### CORS Error

- Verify backend is running on port 8000
- Check CORS settings in `backend/app/main.py`

### Port Already in Use

Backend:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

Frontend:
```bash
# Change port in package.json or use:
PORT=3001 npm start
```

## Production Deployment

### Backend

1. Set environment variables
2. Use production database
3. Set strong SECRET_KEY
4. Use production WSGI server:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

1. Build production bundle:

```bash
npm run build
```

2. Serve with nginx or any static file server

### Security Checklist

- [ ] Change SECRET_KEY
- [ ] Use HTTPS
- [ ] Enable CORS only for trusted domains
- [ ] Use strong passwords
- [ ] Regular database backups
- [ ] Update dependencies regularly
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Enable logging and monitoring
