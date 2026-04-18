from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings
from ..models.models import User, Student, Admin
from ..schemas.schemas import UserLogin, Token, StudentCreate, AdminCreate, StudentResponse, AdminResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

ADMIN_EMAILS = {
    "24071a6737@vnrvjiet.in",
    "24071a6741@vnrvjiet.in",
    "24071a6743@vnrvjiet.in",
    "24071a6748@vnrvjiet.in",
}

@router.post("/register/student", response_model=StudentResponse)
def register_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    # Block admin emails from registering as student
    if student_data.email.lower().strip() in ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is reserved for admin registration."
        )
    # Check if username exists
    if db.query(User).filter(User.username == student_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == student_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(student_data.password)
    user = User(
        username=student_data.username,
        email=student_data.email,
        password_hash=hashed_password,
        role="student"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create student profile
    student = Student(
        user_id=user.id,
        name=student_data.name,
        email=student_data.email,
        branch=student_data.branch,
        year=student_data.year
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student

@router.post("/register/admin", response_model=AdminResponse)
def register_admin(admin_data: AdminCreate, db: Session = Depends(get_db)):
    # Only allow whitelisted admin emails
    if admin_data.email.lower().strip() not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This email is not authorized for admin registration."
        )
    # Check if username exists
    if db.query(User).filter(User.username == admin_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == admin_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(admin_data.password)
    user = User(
        username=admin_data.username,
        email=admin_data.email,
        password_hash=hashed_password,
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create admin profile
    admin = Admin(
        user_id=user.id,
        name=admin_data.name,
        email=admin_data.email
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    return admin


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Allow login with either username or email
    user = db.query(User).filter(
        (User.username == user_credentials.username) |
        (User.email == user_credentials.username)
    ).first()

    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id
    }
