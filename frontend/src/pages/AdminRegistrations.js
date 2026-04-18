import React, { useEffect, useState } from 'react';
import { adminAPI } from '../services/api';

const AdminRegistrations = () => {
  const [registrations, setRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRegistrations();
  }, []);

  const fetchRegistrations = async () => {
    try {
      const response = await adminAPI.getAllRegistrations();
      setRegistrations(response.data);
    } catch (error) {
      console.error('Error fetching registrations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1>All Registrations</h1>
      
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Student Name</th>
              <th>Email</th>
              <th>Exam Name</th>
              <th>Subject</th>
              <th>Exam Date</th>
              <th>Status</th>
              <th>Payment</th>
              <th>Registered On</th>
            </tr>
          </thead>
          <tbody>
            {registrations.map((reg) => (
              <tr key={reg.registration_id}>
                <td>{reg.registration_id}</td>
                <td>{reg.student_name}</td>
                <td>{reg.student_email}</td>
                <td>{reg.exam_name}</td>
                <td>{reg.subject}</td>
                <td>{new Date(reg.exam_date).toLocaleDateString()}</td>
                <td>
                  <span className={`badge badge-${reg.status === 'confirmed' ? 'success' : 'warning'}`}>
                    {reg.status}
                  </span>
                </td>
                <td>
                  {reg.payment_status ? (
                    <span className={`badge badge-${reg.payment_status === 'completed' ? 'success' : 'warning'}`}>
                      {reg.payment_status}
                    </span>
                  ) : (
                    <span className="badge badge-danger">Not Paid</span>
                  )}
                </td>
                <td>{new Date(reg.registration_date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminRegistrations;
