import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminAPI } from '../services/api';
import './Dashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalExams: 0,
    totalStudents: 0,
    totalRegistrations: 0,
    confirmedRegistrations: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [examsRes, studentsRes, registrationsRes] = await Promise.all([
        adminAPI.getAllExams(),
        adminAPI.getAllStudents(),
        adminAPI.getAllRegistrations(),
      ]);
      
      setStats({
        totalExams: examsRes.data.length,
        totalStudents: studentsRes.data.length,
        totalRegistrations: registrationsRes.data.length,
        confirmedRegistrations: registrationsRes.data.filter(r => r.status === 'confirmed').length,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Total Exams</h3>
          <div className="stat-number">{stats.totalExams}</div>
          <button className="btn btn-primary" onClick={() => navigate('/admin/exams')}>
            Manage Exams
          </button>
        </div>
        
        <div className="dashboard-card">
          <h3>Total Students</h3>
          <div className="stat-number">{stats.totalStudents}</div>
          <button className="btn btn-primary" onClick={() => navigate('/admin/students')}>
            View Students
          </button>
        </div>
        
        <div className="dashboard-card">
          <h3>Total Registrations</h3>
          <div className="stat-number">{stats.totalRegistrations}</div>
          <button className="btn btn-primary" onClick={() => navigate('/admin/registrations')}>
            View Registrations
          </button>
        </div>
        
        <div className="dashboard-card">
          <h3>Confirmed</h3>
          <div className="stat-number">{stats.confirmedRegistrations}</div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
