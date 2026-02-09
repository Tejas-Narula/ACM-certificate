from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Admin
from schemas import (
    CertificateCreate,
    CertificateResponse,
    CertificateVerifyResponse,
    CertificateUpdate,
)
from auth import get_current_admin
from crud import (
    create_certificate,
    get_certificate_by_code,
    get_certificate_by_id,
    get_certificates,
    get_certificates_by_email,
    update_certificate,
    delete_certificate,
    get_certificates_count,
)

router = APIRouter(prefix="/api/certificates", tags=["certificates"])


# ============ Public Routes ============

@router.get("/verify/{code}", response_model=CertificateVerifyResponse)
def verify_certificate(code: str, db: Session = Depends(get_db)):
    """
    Verify a certificate by code (public endpoint)
    Returns only public information
    """
    certificate = get_certificate_by_code(db, code.upper())
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    
    if not certificate.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate is not valid",
        )
    
    return certificate


@router.get("/search", response_model=list[CertificateVerifyResponse])
def search_certificates(
    email: str = Query(..., description="Email to search"),
    db: Session = Depends(get_db),
):
    """
    Search certificates by email (public endpoint)
    Returns only public information
    """
    certificates = get_certificates_by_email(db, email)
    return certificates


# ============ Admin Routes ============

@router.post("/", response_model=CertificateResponse)
def create_new_certificate(
    certificate_data: CertificateCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Create a new certificate (admin only)
    """
    certificate = create_certificate(db, certificate_data)
    return certificate


@router.get("/admin/all", response_model=list[CertificateResponse])
def get_all_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Get all certificates (admin only)
    """
    certificates = get_certificates(db, skip=skip, limit=limit)
    return certificates


@router.get("/admin/stats")
def get_certificate_stats(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Get certificate statistics (admin only)
    """
    total = get_certificates_count(db)
    return {
        "total_certificates": total,
    }


@router.get("/admin/{certificate_id}", response_model=CertificateResponse)
def get_certificate_detail(
    certificate_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Get a specific certificate (admin only)
    """
    certificate = get_certificate_by_id(db, certificate_id)
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    return certificate


@router.patch("/admin/{certificate_id}", response_model=CertificateResponse)
def update_certificate_details(
    certificate_id: str,
    certificate_update: CertificateUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Update a certificate (admin only)
    """
    certificate = update_certificate(
        db, certificate_id, certificate_update.model_dump(exclude_unset=True)
    )
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    return certificate


@router.delete("/admin/{certificate_id}")
def delete_certificate_by_id(
    certificate_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Delete a certificate (admin only)
    """
    success = delete_certificate(db, certificate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    return {"success": True, "message": "Certificate deleted successfully"}


@router.post("/admin/bulk-create")
def bulk_create_certificates(
    certificates_data: list[CertificateCreate],
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Create multiple certificates at once (admin only)
    """
    created_certificates = []
    for cert_data in certificates_data:
        certificate = create_certificate(db, cert_data)
        created_certificates.append(certificate)
    
    return {
        "success": True,
        "count": len(created_certificates),
        "certificates": created_certificates,
    }
