import React from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = authService.isAuthenticated();
  const role = authService.getUserRole();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand" onClick={() => navigate('/')}>
          Exam Registration System
        </div>
        <div className="navbar-menu">
          {isAuthenticated ? (
            <>
              {role === 'student' && (
                <>
                  <button onClick={() => navigate('/dashboard')} className="nav-link">
                    Dashboard
                  </button>
                  <button onClick={() => navigate('/exams')} className="nav-link">
                    Exams
                  </button>
                  <button onClick={() => navigate('/my-registrations')} className="nav-link">
                    My Registrations
                  </button>
                </>
              )}
              {role === 'admin' && (
                <>
                  <button onClick={() => navigate('/admin/dashboard')} className="nav-link">
                    Dashboard
                  </button>
                  <button onClick={() => navigate('/admin/exams')} className="nav-link">
                    Manage Exams
                  </button>
                  <button onClick={() => navigate('/admin/registrations')} className="nav-link">
                    Registrations
                  </button>
                  <button onClick={() => navigate('/admin/students')} className="nav-link">
                    Students
                  </button>
                </>
              )}
              <button onClick={handleLogout} className="nav-link logout-btn">
                Logout
              </button>
            </>
          ) : (
            <>
              <button onClick={() => navigate('/login')} className="nav-link">
                Student Login
              </button>
              <button onClick={() => navigate('/register')} className="nav-link">
                Register
              </button>
              <button onClick={() => navigate('/admin/login')} className="nav-link" style={{ background: '#667eea', color: 'white' }}>
                Admin Portal
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
