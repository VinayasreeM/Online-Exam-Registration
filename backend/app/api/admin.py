from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Exam, Registration, Student, Payment, Admin
from ..schemas.schemas import (
    ExamCreate, ExamUpdate, ExamResponse,
    RegistrationReport, StudentResponse
)
from ..api.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

# Exam Management
@router.post("/exams", response_model=ExamResponse)
def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    exam = Exam(**exam_data.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam

@router.put("/exams/{exam_id}", response_model=ExamResponse)
def update_exam(
    exam_id: int,
    exam_data: ExamUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    update_data = exam_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exam, field, value)
    
    db.commit()
    db.refresh(exam)
    return exam

@router.delete("/exams/{exam_id}")
def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    # Delete related payments first, then registrations, then exam
    registrations = db.query(Registration).filter(Registration.exam_id == exam_id).all()
    for reg in registrations:
        db.query(Payment).filter(Payment.registration_id == reg.registration_id).delete()
    db.query(Registration).filter(Registration.exam_id == exam_id).delete()
    
    db.delete(exam)
    db.commit()
    return {"message": "Exam deleted successfully"}

@router.get("/exams", response_model=List[ExamResponse])
def get_all_exams_admin(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    exams = db.query(Exam).all()
    return exams


# Student Management
@router.get("/students", response_model=List[StudentResponse])
def get_all_students(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    students = db.query(Student).all()
    return students

@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

# Registration Management
@router.get("/registrations", response_model=List[RegistrationReport])
def get_all_registrations(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    registrations = db.query(
        Registration.registration_id,
        Student.name.label("student_name"),
        Student.email.label("student_email"),
        Exam.exam_name,
        Exam.subject,
        Exam.exam_date,
        Registration.status,
        Payment.payment_status,
        Registration.registration_date
    ).join(Student).join(Exam).outerjoin(Payment).all()
    
    return [
        RegistrationReport(
            registration_id=r.registration_id,
            student_name=r.student_name,
            student_email=r.student_email,
            exam_name=r.exam_name,
            subject=r.subject,
            exam_date=r.exam_date,
            status=r.status,
            payment_status=r.payment_status,
            registration_date=r.registration_date
        )
        for r in registrations
    ]

@router.get("/registrations/exam/{exam_id}", response_model=List[RegistrationReport])
def get_registrations_by_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    registrations = db.query(
        Registration.registration_id,
        Student.name.label("student_name"),
        Student.email.label("student_email"),
        Exam.exam_name,
        Exam.subject,
        Exam.exam_date,
        Registration.status,
        Payment.payment_status,
        Registration.registration_date
    ).join(Student).join(Exam).outerjoin(Payment).filter(
        Registration.exam_id == exam_id
    ).all()
    
    return [
        RegistrationReport(
            registration_id=r.registration_id,
            student_name=r.student_name,
            student_email=r.student_email,
            exam_name=r.exam_name,
            subject=r.subject,
            exam_date=r.exam_date,
            status=r.status,
            payment_status=r.payment_status,
            registration_date=r.registration_date
        )
        for r in registrations
    ]
