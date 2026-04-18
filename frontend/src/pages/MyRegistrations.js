import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registrationsAPI } from '../services/api';

const MyRegistrations = () => {
  const navigate = useNavigate();
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRegistrations();
  }, []);

  const fetchRegistrations = async () => {
    try {
      const response = await registrationsAPI.getMyRegistrations();
      setRegistrations(response.data);
    } catch (error) {
      console.error('Error fetching registrations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading registrations...</div>;
  }

  return (
    <div className="container">
      <h1>My Registrations</h1>
      
      {registrations.length === 0 ? (
        <div className="card">
          <p>You haven't registered for any exams yet.</p>
          <button className="btn btn-primary" onClick={() => navigate('/exams')}>
            Browse Exams
          </button>
        </div>
      ) : (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>Registration ID</th>
                <th>Exam Name</th>
                <th>Subject</th>
                <th>Exam Date</th>
                <th>Status</th>
                <th>Registration Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {registrations.map((reg) => (
                <tr key={reg.registration_id}>
                  <td>{reg.registration_id}</td>
                  <td>{reg.exam.exam_name}</td>
                  <td>{reg.exam.subject}</td>
                  <td>{new Date(reg.exam.exam_date).toLocaleDateString()}</td>
                  <td>
                    <span className={`badge badge-${reg.status === 'confirmed' ? 'success' : 'warning'}`}>
                      {reg.status}
                    </span>
                  </td>
                  <td>{new Date(reg.registration_date).toLocaleDateString()}</td>
                  <td>
                    {reg.status === 'pending' && (
                      <button
                        className="btn btn-success"
                        onClick={() => navigate(`/payment/${reg.registration_id}`)}
                      >
                        Pay Now
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default MyRegistrations;
