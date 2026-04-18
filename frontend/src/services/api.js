import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  registerStudent: (data) => api.post('/auth/register/student', data),
  registerAdmin: (data) => api.post('/auth/register/admin', data),
  login: (data) => api.post('/auth/login', data),
};

// Exams API
export const examsAPI = {
  getAllExams: () => api.get('/exams/'),
  getExam: (examId) => api.get(`/exams/${examId}`),
};

// Registrations API
export const registrationsAPI = {
  registerForExam: (data) => api.post('/registrations/', data),
  getMyRegistrations: () => api.get('/registrations/my-registrations'),
  getRegistrationStatus: (registrationId) => api.get(`/registrations/${registrationId}`),
};

// Payments API
export const paymentsAPI = {
  makePayment: (data) => api.post('/payments/', data),
  getMyPayments: () => api.get('/payments/my-payments'),
  getPayment: (paymentId) => api.get(`/payments/${paymentId}`),
};

// Admin API
export const adminAPI = {
  // Exams
  createExam: (data) => api.post('/admin/exams', data),
  updateExam: (examId, data) => api.put(`/admin/exams/${examId}`, data),
  deleteExam: (examId) => api.delete(`/admin/exams/${examId}`),
  getAllExams: () => api.get('/admin/exams'),
  
  // Students
  getAllStudents: () => api.get('/admin/students'),
  getStudent: (studentId) => api.get(`/admin/students/${studentId}`),
  
  // Registrations
  getAllRegistrations: () => api.get('/admin/registrations'),
  getRegistrationsByExam: (examId) => api.get(`/admin/registrations/exam/${examId}`),
};

export default api;
