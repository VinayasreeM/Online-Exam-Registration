-- Sample Data for Testing

-- Insert sample admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7dO', 'admin');

INSERT INTO admins (user_id, name, email) VALUES
(1, 'Admin User', 'admin@example.com');

-- Insert sample student users (password: student123)
INSERT INTO users (username, email, password_hash, role) VALUES
('student1', 'student1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7dO', 'student'),
('student2', 'student2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7dO', 'student'),
('student3', 'student3@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg7dO', 'student');

INSERT INTO students (user_id, name, email, branch, year) VALUES
(2, 'John Doe', 'student1@example.com', 'Computer Science', 3),
(3, 'Jane Smith', 'student2@example.com', 'Information Technology', 2),
(4, 'Bob Johnson', 'student3@example.com', 'Electronics', 4);

-- Insert sample exams
INSERT INTO exams (exam_name, subject, exam_date, duration, total_marks, fee, is_active) VALUES
('Mid-Term Examination', 'Data Structures', '2026-03-15', 180, 100, 50.00, true),
('Final Examination', 'Database Management', '2026-05-20', 180, 100, 50.00, true),
('Mid-Term Examination', 'Operating Systems', '2026-03-18', 120, 75, 40.00, true),
('Final Examination', 'Computer Networks', '2026-05-25', 180, 100, 50.00, true),
('Mid-Term Examination', 'Web Development', '2026-03-22', 120, 75, 40.00, true);

-- Insert sample registrations
INSERT INTO registrations (student_id, exam_id, status) VALUES
(1, 1, 'confirmed'),
(1, 2, 'pending'),
(2, 1, 'confirmed'),
(2, 3, 'confirmed'),
(3, 4, 'pending');

-- Insert sample payments
INSERT INTO payments (registration_id, amount, payment_status, transaction_id) VALUES
(1, 50.00, 'completed', 'TXN1234567890AB'),
(3, 50.00, 'completed', 'TXN2345678901BC'),
(4, 40.00, 'completed', 'TXN3456789012CD');

-- Verify data
SELECT 'Users:' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Students:', COUNT(*) FROM students
UNION ALL
SELECT 'Admins:', COUNT(*) FROM admins
UNION ALL
SELECT 'Exams:', COUNT(*) FROM exams
UNION ALL
SELECT 'Registrations:', COUNT(*) FROM registrations
UNION ALL
SELECT 'Payments:', COUNT(*) FROM payments;
