from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ..core.database import get_db
from ..models.models import Payment, Registration, Student
from ..schemas.schemas import PaymentCreate, PaymentResponse
from ..api.dependencies import get_current_student

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
def make_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    # Check if registration exists and belongs to current student
    registration = db.query(Registration).filter(
        Registration.registration_id == payment_data.registration_id,
        Registration.student_id == current_student.student_id
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    # Check if payment already exists
    existing_payment = db.query(Payment).filter(
        Payment.registration_id == payment_data.registration_id
    ).first()
    
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already made for this registration"
        )
    
    # Simulate payment processing
    transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
    
    # Create payment
    payment = Payment(
        registration_id=payment_data.registration_id,
        amount=payment_data.amount,
        payment_status="completed",
        transaction_id=transaction_id
    )
    db.add(payment)
    
    # Update registration status
    registration.status = "confirmed"
    
    db.commit()
    db.refresh(payment)
    
    return payment

@router.get("/my-payments", response_model=List[PaymentResponse])
def get_my_payments(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    payments = db.query(Payment).join(Registration).filter(
        Registration.student_id == current_student.student_id
    ).all()
    return payments

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    payment = db.query(Payment).join(Registration).filter(
        Payment.payment_id == payment_id,
        Registration.student_id == current_student.student_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment
