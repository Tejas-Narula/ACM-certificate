from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# Workshop Schemas
class WorkshopBase(BaseModel):
    title: str
    date: str
    description: Optional[str] = None
    level: str = "Beginner"
    instructor: str
    image: Optional[str] = None


class WorkshopCreate(WorkshopBase):
    pass


class WorkshopUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    instructor: Optional[str] = None
    image: Optional[str] = None


class WorkshopResponse(WorkshopBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Certificate Schemas
class CertificateBase(BaseModel):
    recipient_name: str
    email: EmailStr
    workshop_name: str
    issue_date: str
    skills: List[str]
    instructor: str


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(BaseModel):
    recipient_name: Optional[str] = None
    workshop_name: Optional[str] = None
    issue_date: Optional[str] = None
    skills: Optional[List[str]] = None
    instructor: Optional[str] = None


class CertificateResponse(BaseModel):
    id: str
    code: str
    recipient_name: str
    email: str
    workshop_name: str
    issue_date: str
    skills: List[str]
    instructor: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CertificateVerifyResponse(BaseModel):
    """Response for certificate verification (public)"""
    id: str
    code: str
    recipient_name: str
    workshop_name: str
    issue_date: str
    skills: List[str]
    instructor: str
    is_verified: bool

    class Config:
        from_attributes = True


# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Bulk Certificate Creation
class BulkCertificateCreate(BaseModel):
    workshop_id: str
    certificates: List[CertificateCreate]


# Response Schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
