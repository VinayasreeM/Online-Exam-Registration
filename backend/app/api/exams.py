from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import Exam
from ..schemas.schemas import ExamResponse
from ..api.dependencies import get_current_user

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("/", response_model=List[ExamResponse])
def get_all_exams(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    exams = db.query(Exam).filter(Exam.is_active == True).all()
    return exams

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found"
        )
    return exam
