# Quick Reference Guide

## 🚀 Installation Commands

### Database Setup
```bash
# Create database
psql -U postgres -c "CREATE DATABASE exam_registration;"

# Run schema
psql -U postgres -d exam_registration -f database/schema.sql

# Load sample data (optional)
psql -U postgres -d exam_registration -f database/sample_data.sql
```

### Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔗 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🔑 Default Credentials

### Admin Account
```
Username: admin
Password: admin123
Email: admin@example.com
```

### Student Accounts
```
Username: student1
Password: student123
Email: student1@example.com

Username: student2
Password: student123
Email: student2@example.com
```

## 📝 Common Tasks

### Create New Student
```bash
curl -X POST http://localhost:8000/auth/register/student \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newstudent",
    "email": "new@example.com",
    "password": "password123",
    "name": "New Student",
    "branch": "Computer Science",
    "year": 2
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "student123"
  }'
```

### Get Exams (with token)
```bash
curl -X GET http://localhost:8000/exams/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🗄️ Database Queries

### View all users
```sql
SELECT id, username, email, role FROM users;
```

### View registrations with details
```sql
SELECT 
    r.registration_id,
    s.name as student_name,
    e.exam_name,
    r.status,
    p.payment_status
FROM registrations r
JOIN students s ON r.student_id = s.student_id
JOIN exams e ON r.exam_id = e.exam_id
LEFT JOIN payments p ON r.registration_id = p.registration_id;
```

### Count registrations by status
```sql
SELECT status, COUNT(*) 
FROM registrations 
GROUP BY status;
```

### View upcoming exams
```sql
SELECT exam_name, subject, exam_date 
FROM exams 
WHERE exam_date > CURRENT_DATE 
AND is_active = true
ORDER BY exam_date;
```

## 🐛 Troubleshooting

### Port Already in Use

**Backend (Port 8000)**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 3000)**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### Database Connection Error
```bash
# Check PostgreSQL is running
# Windows
sc query postgresql-x64-14

# Linux
sudo systemctl status postgresql

# Mac
brew services list
```

### CORS Error
Check `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 📦 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/exam_registration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (optional .env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🔄 Reset Database
```bash
# Drop and recreate
psql -U postgres -c "DROP DATABASE IF EXISTS exam_registration;"
psql -U postgres -c "CREATE DATABASE exam_registration;"
psql -U postgres -d exam_registration -f database/schema.sql
psql -U postgres -d exam_registration -f database/sample_data.sql
```

## 📊 Project Commands

### Backend
```bash
# Run server
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --reload --port 8001

# Run tests (if implemented)
pytest

# Check code style
flake8 app/

# Format code
black app/
```

### Frontend
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Check for updates
npm outdated

# Update dependencies
npm update
```

## 🔐 Generate New Secret Key

```python
# Python
import secrets
print(secrets.token_urlsafe(32))
```

```bash
# OpenSSL
openssl rand -hex 32
```

## 📱 API Response Examples

### Successful Login
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "student",
  "user_id": 1
}
```

### Exam List
```json
[
  {
    "exam_id": 1,
    "exam_name": "Mid-Term Examination",
    "subject": "Data Structures",
    "exam_date": "2026-03-15",
    "duration": 180,
    "total_marks": 100,
    "fee": "50.00",
    "is_active": true,
    "created_at": "2026-02-12T10:00:00"
  }
]
```

### Error Response
```json
{
  "detail": "Username already registered"
}
```

## 🎨 UI Routes

### Public Routes
- `/` - Home page
- `/login` - Login page
- `/register` - Registration page

### Student Routes (Protected)
- `/dashboard` - Student dashboard
- `/exams` - Browse exams
- `/my-registrations` - View registrations
- `/payment/:registrationId` - Payment page

### Admin Routes (Protected)
- `/admin/dashboard` - Admin dashboard
- `/admin/exams` - Manage exams
- `/admin/registrations` - View all registrations
- `/admin/students` - View all students

## 🔧 Configuration Files

### Backend
- `backend/requirements.txt` - Python dependencies
- `backend/.env` - Environment variables
- `backend/app/core/config.py` - Application config

### Frontend
- `frontend/package.json` - Node dependencies
- `frontend/src/services/api.js` - API configuration

### Database
- `database/schema.sql` - Database schema
- `database/sample_data.sql` - Test data

## 📈 Performance Tips

1. **Database**: Add indexes on frequently queried columns
2. **Backend**: Use connection pooling
3. **Frontend**: Implement lazy loading for routes
4. **API**: Add caching for static data
5. **Images**: Optimize and use CDN

## 🔍 Useful SQL Queries

### Find students without registrations
```sql
SELECT s.student_id, s.name, s.email
FROM students s
LEFT JOIN registrations r ON s.student_id = r.student_id
WHERE r.registration_id IS NULL;
```

### Revenue report
```sql
SELECT 
    DATE(p.payment_date) as date,
    COUNT(*) as payments,
    SUM(p.amount) as total_revenue
FROM payments p
WHERE p.payment_status = 'completed'
GROUP BY DATE(p.payment_date)
ORDER BY date DESC;
```

### Popular exams
```sql
SELECT 
    e.exam_name,
    COUNT(r.registration_id) as registrations
FROM exams e
LEFT JOIN registrations r ON e.exam_id = r.exam_id
GROUP BY e.exam_id, e.exam_name
ORDER BY registrations DESC;
```

## 🚨 Emergency Commands

### Stop all servers
```bash
# Windows
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# Linux/Mac
pkill -f uvicorn
pkill -f node
```

### Clear browser cache
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete
- Edge: Ctrl+Shift+Delete

### Reset local storage (Frontend)
```javascript
// In browser console
localStorage.clear();
location.reload();
```

## 📞 Support Checklist

Before asking for help:
- [ ] Check error messages in console
- [ ] Verify all services are running
- [ ] Check database connection
- [ ] Verify environment variables
- [ ] Check API documentation
- [ ] Review logs
- [ ] Try with sample data
- [ ] Check CORS settings
- [ ] Verify token is valid
- [ ] Check network tab in browser

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- SQLAlchemy: https://docs.sqlalchemy.org/
- PostgreSQL: https://www.postgresql.org/docs/
- JWT: https://jwt.io/

---

**Keep this guide handy for quick reference!**
