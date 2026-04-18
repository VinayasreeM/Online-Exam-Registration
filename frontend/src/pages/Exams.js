import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { examsAPI, registrationsAPI } from '../services/api';

const Exams = () => {
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [registering, setRegistering] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      const response = await examsAPI.getAllExams();
      setExams(response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (examId) => {
    setRegistering(examId);
    setError('');
    try {
      const response = await registrationsAPI.registerForExam({ exam_id: examId });
      alert('Registration successful! Please proceed to payment.');
      navigate(`/payment/${response.data.registration_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
      alert(err.response?.data?.detail || 'Registration failed');
    } finally {
      setRegistering(null);
    }
  };

  if (loading) {
    return <div className="loading">Loading exams...</div>;
  }

  return (
    <div className="container">
      <h1>Available Exams</h1>
      {error && <div className="error">{error}</div>}
      
      {exams.length === 0 ? (
        <div className="card">
          <p>No exams available at the moment.</p>
        </div>
      ) : (
        <div className="exams-grid">
          {exams.map((exam) => (
            <div key={exam.exam_id} className="card exam-card">
              <h3>{exam.exam_name}</h3>
              <div className="exam-details">
                <p><strong>Subject:</strong> {exam.subject}</p>
                <p><strong>Date:</strong> {new Date(exam.exam_date).toLocaleDateString()}</p>
                <p><strong>Duration:</strong> {exam.duration} minutes</p>
                <p><strong>Total Marks:</strong> {exam.total_marks}</p>
                <p><strong>Fee:</strong> ₹300.00</p>
              </div>
              <button
                className="btn btn-primary"
                onClick={() => handleRegister(exam.exam_id)}
                disabled={registering === exam.exam_id}
              >
                {registering === exam.exam_id ? 'Registering...' : 'Register'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Exams;
