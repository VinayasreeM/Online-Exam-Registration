import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Online Exam Registration System</h1>
        <p className="subtitle">
          Streamline your exam registration process with our modern, secure platform
        </p>
        
        <div className="features">
          <div className="feature-card">
            <h3>For Students</h3>
            <ul>
              <li>Browse available exams</li>
              <li>Easy registration process</li>
              <li>Secure online payment</li>
              <li>Track registration status</li>
            </ul>
            <button className="btn btn-primary" onClick={() => navigate('/register')}>
              Get Started
            </button>
          </div>
          
          <div className="feature-card">
            <h3>For Administrators</h3>
            <ul>
              <li>Manage exams efficiently</li>
              <li>View all registrations</li>
              <li>Generate reports</li>
              <li>Monitor student data</li>
            </ul>
            <button className="btn btn-primary" onClick={() => navigate('/admin/login')}>
              Admin Portal
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
