from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Numeric, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    student = relationship("Student", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    
    __table_args__ = (
        CheckConstraint("role IN ('student', 'admin')", name='check_role'),
    )

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    branch = Column(String(50))
    year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="student")
    registrations = relationship("Registration", back_populates="student")
    
    __table_args__ = (
        CheckConstraint("year >= 1 AND year <= 4", name='check_year'),
    )

class Admin(Base):
    __tablename__ = "admins"
    
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="admin")


class Exam(Base):
    __tablename__ = "exams"
    
    exam_id = Column(Integer, primary_key=True, index=True)
    exam_name = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    exam_date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    fee = Column(Numeric(10, 2), default=300.00)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    registrations = relationship("Registration", back_populates="exam")

class Registration(Base):
    __tablename__ = "registrations"
    
    registration_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.exam_id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='pending')
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    
    student = relationship("Student", back_populates="registrations")
    exam = relationship("Exam", back_populates="registrations")
    payment = relationship("Payment", back_populates="registration", uselist=False)
    
    __table_args__ = (
        UniqueConstraint('student_id', 'exam_id', name='unique_student_exam'),
        CheckConstraint("status IN ('pending', 'confirmed', 'cancelled')", name='check_status'),
    )

class Payment(Base):
    __tablename__ = "payments"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.registration_id", ondelete="CASCADE"), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String(20), default='pending')
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    transaction_id = Column(String(100))
    
    registration = relationship("Registration", back_populates="payment")
    
    __table_args__ = (
        CheckConstraint("payment_status IN ('pending', 'completed', 'failed')", name='check_payment_status'),
    )
