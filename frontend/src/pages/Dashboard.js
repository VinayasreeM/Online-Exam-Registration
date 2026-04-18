import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { examsAPI, registrationsAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [exams, setExams] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [examsRes, registrationsRes] = await Promise.all([
        examsAPI.getAllExams(),
        registrationsAPI.getMyRegistrations(),
      ]);
      setExams(examsRes.data);
      setRegistrations(registrationsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1>Student Dashboard</h1>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Available Exams</h3>
          <div className="stat-number">{exams.length}</div>
          <button className="btn btn-primary" onClick={() => navigate('/exams')}>
            View All Exams
          </button>
        </div>
        
        <div className="dashboard-card">
          <h3>My Registrations</h3>
          <div className="stat-number">{registrations.length}</div>
          <button className="btn btn-primary" onClick={() => navigate('/my-registrations')}>
            View Registrations
          </button>
        </div>
        
        <div className="dashboard-card">
          <h3>Confirmed</h3>
          <div className="stat-number">
            {registrations.filter(r => r.status === 'confirmed').length}
          </div>
        </div>
        
        <div className="dashboard-card">
          <h3>Pending</h3>
          <div className="stat-number">
            {registrations.filter(r => r.status === 'pending').length}
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Recent Registrations</h2>
        {registrations.length === 0 ? (
          <p>No registrations yet. Register for an exam to get started!</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Exam Name</th>
                <th>Subject</th>
                <th>Exam Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {registrations.slice(0, 5).map((reg) => (
                <tr key={reg.registration_id}>
                  <td>{reg.exam.exam_name}</td>
                  <td>{reg.exam.subject}</td>
                  <td>{new Date(reg.exam.exam_date).toLocaleDateString()}</td>
                  <td>
                    <span className={`badge badge-${reg.status === 'confirmed' ? 'success' : 'warning'}`}>
                      {reg.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
