from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from schemas import AdminLogin, AdminCreate, TokenResponse, AdminResponse
from auth import create_access_token, authenticate_admin, hash_password
from crud import create_admin, get_admin_by_email
from config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AdminResponse)
def register(admin_data: AdminCreate, db: Session = Depends(get_db)):
    """Register a new admin (only allowed for initial setup)"""
    # In production, you might want to restrict this or require validation
    existing_admin = get_admin_by_email(db, admin_data.email)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    new_admin = create_admin(db, admin_data.email, admin_data.password)
    return new_admin


@router.post("/login", response_model=TokenResponse)
def login(credentials: AdminLogin, db: Session = Depends(get_db)):
    """Login admin and get access token"""
    admin = authenticate_admin(db, credentials.email, credentials.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/init-admin")
def init_admin(db: Session = Depends(get_db)):
    """Initialize default admin (only run once)"""
    existing_admin = get_admin_by_email(db, settings.ADMIN_EMAIL)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already initialized",
        )
    
    admin = create_admin(db, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
    return {
        "success": True,
        "message": "Admin initialized successfully",
        "admin": AdminResponse.from_orm(admin),
    }
