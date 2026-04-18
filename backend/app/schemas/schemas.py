from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    branch: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=4)

class StudentCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str
    branch: Optional[str] = None
    year: Optional[int] = Field(None, ge=1, le=4)

class StudentResponse(StudentBase):
    student_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin Schemas
class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class AdminResponse(BaseModel):
    admin_id: int
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

# Exam Schemas
class ExamBase(BaseModel):
    exam_name: str
    subject: str
    exam_date: date
    duration: int
    total_marks: int
    fee: Decimal = Field(default=Decimal("300.00"))

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    exam_name: Optional[str] = None
    subject: Optional[str] = None
    exam_date: Optional[date] = None
    duration: Optional[int] = None
    total_marks: Optional[int] = None
    fee: Optional[Decimal] = None
    is_active: Optional[bool] = None

class ExamResponse(ExamBase):
    exam_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Registration Schemas
class RegistrationCreate(BaseModel):
    exam_id: int

class RegistrationResponse(BaseModel):
    registration_id: int
    student_id: int
    exam_id: int
    status: str
    registration_date: datetime
    exam: ExamResponse
    
    class Config:
        from_attributes = True

# Payment Schemas
class PaymentCreate(BaseModel):
    registration_id: int
    amount: Decimal

class PaymentResponse(BaseModel):
    payment_id: int
    registration_id: int
    amount: Decimal
    payment_status: str
    payment_date: datetime
    transaction_id: Optional[str] = None
    
    class Config:
        from_attributes = True

# Report Schemas
class RegistrationReport(BaseModel):
    registration_id: int
    student_name: str
    student_email: str
    exam_name: str
    subject: str
    exam_date: date
    status: str
    payment_status: Optional[str] = None
    registration_date: datetime
