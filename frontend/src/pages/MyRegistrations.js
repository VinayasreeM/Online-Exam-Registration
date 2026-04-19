import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registrationsAPI } from '../services/api';
import api from '../services/api';

const MyRegistrations = () => {
  const navigate = useNavigate();
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(null);

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

  const downloadAdmitCard = async (registrationId) => {
    setDownloading(registrationId);
    try {
      const response = await api.get(`/admit-card/${registrationId}`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `AdmitCard_REG${String(registrationId).padStart(4, '0')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Failed to download admit card. Please try again.');
    } finally {
      setDownloading(null);
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
                    {reg.status === 'confirmed' && (
                      <button
                        className="btn btn-primary"
                        onClick={() => downloadAdmitCard(reg.registration_id)}
                        disabled={downloading === reg.registration_id}
                      >
                        {downloading === reg.registration_id ? 'Downloading...' : '⬇ Admit Card'}
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
