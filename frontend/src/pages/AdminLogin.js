import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { authService } from '../services/auth';
import './Auth.css';

const AdminLogin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      // Use email as the username field since backend now supports email login
      const response = await authAPI.login({
        username: formData.email,
        password: formData.password,
      });
      const { access_token, role, user_id } = response.data;
      if (role !== 'admin') {
        setError('This account does not have admin privileges.');
        setLoading(false);
        return;
      }
      authService.setToken(access_token);
      authService.setUserRole(role);
      authService.setUserId(user_id);
      navigate('/admin/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <span style={{ fontSize: '48px' }}>🔐</span>
          <h2 style={{ marginTop: '8px', color: '#667eea' }}>Admin Portal</h2>
          <p style={{ color: '#888', fontSize: '14px' }}>Sign in with your admin credentials</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your admin email"
              required
              autoFocus
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Signing in...' : 'Login'}
          </button>
        </form>

        <p className="auth-link" style={{ marginTop: '20px' }}>
          Not an admin? <span onClick={() => navigate('/login')}>Student Login</span>
        </p>
      </div>
    </div>
  );
};

export default AdminLogin;
