import React, { useEffect, useState } from 'react';
import { adminAPI } from '../services/api';

const ManageExams = () => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingExam, setEditingExam] = useState(null);
  const [formData, setFormData] = useState({
    exam_name: '',
    subject: '',
    exam_date: '',
    duration: '',
    total_marks: '',
    fee: '300',
  });

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      const response = await adminAPI.getAllExams();
      setExams(response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        duration: parseInt(formData.duration),
        total_marks: parseInt(formData.total_marks),
        fee: parseFloat(formData.fee),
      };

      if (editingExam) {
        await adminAPI.updateExam(editingExam.exam_id, data);
        alert('Exam updated successfully!');
      } else {
        await adminAPI.createExam(data);
        alert('Exam created successfully!');
      }

      setShowForm(false);
      setEditingExam(null);
      setFormData({
        exam_name: '',
        subject: '',
        exam_date: '',
        duration: '',
        total_marks: '',
        fee: '300',
      });
      fetchExams();
    } catch (error) {
      alert('Error saving exam: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleEdit = (exam) => {
    setEditingExam(exam);
    setFormData({
      exam_name: exam.exam_name,
      subject: exam.subject,
      exam_date: exam.exam_date,
      duration: exam.duration.toString(),
      total_marks: exam.total_marks.toString(),
      fee: exam.fee.toString(),
    });
    setShowForm(true);
  };

  const handleDelete = async (examId) => {
    if (window.confirm('Are you sure you want to delete this exam?')) {
      try {
        await adminAPI.deleteExam(examId);
        alert('Exam deleted successfully!');
        fetchExams();
      } catch (error) {
        alert('Error deleting exam: ' + (error.response?.data?.detail || 'Unknown error'));
      }
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>Manage Exams</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add New Exam'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>{editingExam ? 'Edit Exam' : 'Add New Exam'}</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Exam Name</label>
              <input
                type="text"
                name="exam_name"
                value={formData.exam_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Subject</label>
              <input
                type="text"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Exam Date</label>
              <input
                type="date"
                name="exam_date"
                value={formData.exam_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Duration (minutes)</label>
              <input
                type="number"
                name="duration"
                value={formData.duration}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Total Marks</label>
              <input
                type="number"
                name="total_marks"
                value={formData.total_marks}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Fee (₹)</label>
              <input
                type="number"
                step="0.01"
                name="fee"
                value={formData.fee}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              {editingExam ? 'Update Exam' : 'Create Exam'}
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>All Exams</h2>
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Exam Name</th>
              <th>Subject</th>
              <th>Date</th>
              <th>Duration</th>
              <th>Marks</th>
              <th>Fee</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {exams.map((exam) => (
              <tr key={exam.exam_id}>
                <td>{exam.exam_id}</td>
                <td>{exam.exam_name}</td>
                <td>{exam.subject}</td>
                <td>{new Date(exam.exam_date).toLocaleDateString()}</td>
                <td>{exam.duration} min</td>
                <td>{exam.total_marks}</td>
                <td>₹{parseFloat(exam.fee).toFixed(2)}</td>
                <td>
                  <span className={`badge badge-${exam.is_active ? 'success' : 'danger'}`}>
                    {exam.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <button
                    className="btn btn-secondary"
                    onClick={() => handleEdit(exam)}
                    style={{ marginRight: '5px' }}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(exam.exam_id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ManageExams;
