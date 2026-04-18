import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { registrationsAPI, paymentsAPI } from '../services/api';

const Payment = () => {
  const { registrationId } = useParams();
  const navigate = useNavigate();
  const [registration, setRegistration] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchRegistration();
  }, [registrationId]);

  const fetchRegistration = async () => {
    try {
      const response = await registrationsAPI.getRegistrationStatus(registrationId);
      setRegistration(response.data);
    } catch (error) {
      setError('Registration not found');
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    setProcessing(true);
    setError('');
    
    try {
      const paymentData = {
        registration_id: parseInt(registrationId),
        amount: parseFloat(registration.exam.fee),
      };
      
      await paymentsAPI.makePayment(paymentData);
      alert('Payment successful! Your registration is confirmed.');
      navigate('/my-registrations');
    } catch (err) {
      setError(err.response?.data?.detail || 'Payment failed');
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error && !registration) {
    return (
      <div className="container">
        <div className="card">
          <h2>Error</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => navigate('/my-registrations')}>
            Back to Registrations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
        <h2>Payment</h2>
        
        {registration.status === 'confirmed' ? (
          <div>
            <p className="success">This registration has already been paid for.</p>
            <button className="btn btn-primary" onClick={() => navigate('/my-registrations')}>
              Back to Registrations
            </button>
          </div>
        ) : (
          <>
            <div className="payment-details">
              <h3>Exam Details</h3>
              <p><strong>Exam:</strong> {registration.exam.exam_name}</p>
              <p><strong>Subject:</strong> {registration.exam.subject}</p>
              <p><strong>Date:</strong> {new Date(registration.exam.exam_date).toLocaleDateString()}</p>
              <p><strong>Duration:</strong> {registration.exam.duration} minutes</p>
              <hr />
              <h3>Payment Summary</h3>
              <p><strong>Registration Fee:</strong> ₹{parseFloat(registration.exam.fee).toFixed(2)}</p>
              <p><strong>Total Amount:</strong> ₹{parseFloat(registration.exam.fee).toFixed(2)}</p>
            </div>
            
            {error && <div className="error">{error}</div>}
            
            <div style={{ marginTop: '30px' }}>
              <button
                className="btn btn-success"
                onClick={handlePayment}
                disabled={processing}
                style={{ width: '100%', marginBottom: '10px' }}
              >
                {processing ? 'Processing Payment...' : 'Pay Now'}
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => navigate('/my-registrations')}
                style={{ width: '100%' }}
              >
                Cancel
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Payment;
