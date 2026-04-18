from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Registration, Exam, Student
from ..schemas.schemas import RegistrationCreate, RegistrationResponse
from ..api.dependencies import get_current_student

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.post("/", response_model=RegistrationResponse)
def register_for_exam(
    registration_data: RegistrationCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Check if exam exists
    exam = db.query(Exam).filter(Exam.exam_id == registration_data.exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    
    if not exam.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exam is not active"
        )
    
    # Check if already registered
    existing_registration = db.query(Registration).filter(
        Registration.student_id == current_student.student_id,
        Registration.exam_id == registration_data.exam_id
    ).first()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this exam"
        )
    
    # Create registration
    registration = Registration(
        student_id=current_student.student_id,
        exam_id=registration_data.exam_id,
        status="pending"
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    
    return registration

@router.get("/my-registrations", response_model=List[RegistrationResponse])
def get_my_registrations(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    registrations = db.query(Registration).filter(
        Registration.student_id == current_student.student_id
    ).all()
    return registrations

@router.get("/{registration_id}", response_model=RegistrationResponse)
def get_registration_status(
    registration_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    registration = db.query(Registration).filter(
        Registration.registration_id == registration_id,
        Registration.student_id == current_student.student_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    return registration
