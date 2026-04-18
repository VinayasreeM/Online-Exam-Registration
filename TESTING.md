# Testing Guide

## Test Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

### Student Accounts
- Username: `student1` | Password: `student123` | Email: `student1@example.com`
- Username: `student2` | Password: `student123` | Email: `student2@example.com`
- Username: `student3` | Password: `student123` | Email: `student3@example.com`

## Manual Testing Scenarios

### 1. User Registration

#### Test Case 1.1: Student Registration
1. Navigate to http://localhost:3000/register
2. Select "Student" tab
3. Fill in form:
   - Username: testuser1
   - Email: testuser1@example.com
   - Password: test123
   - Name: Test User
   - Branch: Computer Science
   - Year: 2
4. Click "Register"
5. Expected: Success message, redirect to login

#### Test Case 1.2: Duplicate Username
1. Try registering with existing username
2. Expected: Error message "Username already registered"

#### Test Case 1.3: Admin Registration
1. Select "Admin" tab
2. Fill in admin details
3. Expected: Admin account created successfully

### 2. User Login

#### Test Case 2.1: Valid Login
1. Navigate to http://localhost:3000/login
2. Enter valid credentials
3. Expected: Redirect to appropriate dashboard

#### Test Case 2.2: Invalid Credentials
1. Enter wrong password
2. Expected: Error message "Incorrect username or password"

#### Test Case 2.3: Role-Based Redirect
1. Login as student → Dashboard
2. Login as admin → Admin Dashboard

### 3. Student Workflow

#### Test Case 3.1: View Exams
1. Login as student
2. Navigate to "Exams"
3. Expected: List of active exams displayed

#### Test Case 3.2: Register for Exam
1. Click "Register" on an exam
2. Expected: Registration created, redirect to payment

#### Test Case 3.3: Duplicate Registration Prevention
1. Try registering for same exam twice
2. Expected: Error "Already registered for this exam"

#### Test Case 3.4: Payment Processing
1. Navigate to payment page
2. Click "Pay Now"
3. Expected: Payment successful, registration confirmed

#### Test Case 3.5: View Registrations
1. Navigate to "My Registrations"
2. Expected: List of all registrations with status

### 4. Admin Workflow

#### Test Case 4.1: View Dashboard
1. Login as admin
2. Expected: Statistics displayed (exams, students, registrations)

#### Test Case 4.2: Create Exam
1. Navigate to "Manage Exams"
2. Click "Add New Exam"
3. Fill in exam details:
   - Name: Test Exam
   - Subject: Testing
   - Date: Future date
   - Duration: 120
   - Marks: 100
   - Fee: 50.00
4. Click "Create Exam"
5. Expected: Exam created, appears in list

#### Test Case 4.3: Update Exam
1. Click "Edit" on an exam
2. Modify details
3. Click "Update Exam"
4. Expected: Exam updated successfully

#### Test Case 4.4: Delete Exam
1. Click "Delete" on an exam
2. Confirm deletion
3. Expected: Exam removed from list

#### Test Case 4.5: View All Registrations
1. Navigate to "Registrations"
2. Expected: All student registrations displayed

#### Test Case 4.6: View All Students
1. Navigate to "Students"
2. Expected: All registered students displayed

### 5. Security Testing

#### Test Case 5.1: Protected Routes
1. Logout
2. Try accessing /dashboard directly
3. Expected: Redirect to login

#### Test Case 5.2: Role-Based Access
1. Login as student
2. Try accessing /admin/dashboard
3. Expected: Redirect to home

#### Test Case 5.3: Token Expiration
1. Login and wait for token expiration (30 minutes)
2. Try making API request
3. Expected: Redirect to login

### 6. Edge Cases

#### Test Case 6.1: Empty Exam List
1. Admin deletes all exams
2. Student views exams
3. Expected: "No exams available" message

#### Test Case 6.2: Payment for Confirmed Registration
1. Try paying for already confirmed registration
2. Expected: Message "Already paid"

#### Test Case 6.3: Invalid Registration ID
1. Navigate to /payment/99999
2. Expected: Error message

## API Testing with cURL

### Register Student
```bash
curl -X POST http://localhost:8000/auth/register/student \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123",
    "name": "Test User",
    "branch": "CS",
    "year": 2
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

### Get Exams (with token)
```bash
curl -X GET http://localhost:8000/exams/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Register for Exam
```bash
curl -X POST http://localhost:8000/registrations/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "exam_id": 1
  }'
```

### Make Payment
```bash
curl -X POST http://localhost:8000/payments/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": 1,
    "amount": 50.00
  }'
```

## Database Testing

### Verify Constraints

```sql
-- Test unique constraint on student-exam registration
INSERT INTO registrations (student_id, exam_id, status) 
VALUES (1, 1, 'pending');
-- Should fail if already exists

-- Test check constraint on user role
INSERT INTO users (username, email, password_hash, role) 
VALUES ('test', 'test@test.com', 'hash', 'invalid');
-- Should fail

-- Test foreign key constraint
INSERT INTO registrations (student_id, exam_id, status) 
VALUES (999, 1, 'pending');
-- Should fail if student doesn't exist
```

### Verify Relationships

```sql
-- Get student with registrations
SELECT s.name, e.exam_name, r.status
FROM students s
JOIN registrations r ON s.student_id = r.student_id
JOIN exams e ON r.exam_id = e.exam_id;

-- Get registrations with payment status
SELECT r.registration_id, s.name, e.exam_name, p.payment_status
FROM registrations r
JOIN students s ON r.student_id = s.student_id
JOIN exams e ON r.exam_id = e.exam_id
LEFT JOIN payments p ON r.registration_id = p.registration_id;
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test login endpoint
ab -n 1000 -c 10 -p login.json -T application/json \
  http://localhost:8000/auth/login

# Test get exams endpoint
ab -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/exams/
```

## Automated Testing (Future)

### Backend Unit Tests (pytest)
```python
# test_auth.py
def test_register_student():
    response = client.post("/auth/register/student", json={...})
    assert response.status_code == 200

def test_login_success():
    response = client.post("/auth/login", json={...})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_duplicate_registration():
    # Register once
    # Try registering again
    # Assert error
```

### Frontend Tests (Jest/React Testing Library)
```javascript
// Login.test.js
test('renders login form', () => {
  render(<Login />);
  expect(screen.getByText('Login')).toBeInTheDocument();
});

test('shows error on invalid credentials', async () => {
  // Mock API call
  // Submit form
  // Assert error message
});
```

## Test Results Checklist

- [ ] User registration works for both roles
- [ ] Login authentication successful
- [ ] JWT token generated and validated
- [ ] Student can view exams
- [ ] Student can register for exam
- [ ] Duplicate registration prevented
- [ ] Payment processing works
- [ ] Registration status updates
- [ ] Admin can create exams
- [ ] Admin can update exams
- [ ] Admin can delete exams
- [ ] Admin can view all data
- [ ] Protected routes work
- [ ] Role-based access enforced
- [ ] Database constraints enforced
- [ ] API returns proper error messages
- [ ] Frontend displays errors correctly
- [ ] Responsive design works
- [ ] CORS configured properly
- [ ] Password hashing works

## Known Issues / Limitations

1. Payment is simulated (no real gateway)
2. No email notifications
3. No password reset functionality
4. No file upload for documents
5. No pagination for large datasets
6. No search/filter functionality
7. No export to PDF/Excel
8. Token refresh not implemented
9. No rate limiting
10. No comprehensive logging

## Recommendations

1. Add automated test suite
2. Implement integration tests
3. Add end-to-end tests with Selenium/Cypress
4. Set up CI/CD pipeline
5. Add code coverage reporting
6. Implement error tracking (Sentry)
7. Add performance monitoring
8. Create test data generators
9. Document all test cases
10. Regular security audits
