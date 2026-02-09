from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Admin
from schemas import WorkshopCreate, WorkshopResponse, WorkshopUpdate
from auth import get_current_admin
from crud import (
    create_workshop,
    get_workshop_by_id,
    get_workshops,
    update_workshop,
    delete_workshop,
)

router = APIRouter(prefix="/api/workshops", tags=["workshops"])


# ============ Public Routes ============

@router.get("/", response_model=list[WorkshopResponse])
def list_workshops(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get all workshops (public)
    """
    workshops = get_workshops(db, skip=skip, limit=limit)
    return workshops


@router.get("/{workshop_id}", response_model=WorkshopResponse)
def get_workshop(
    workshop_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific workshop (public)
    """
    workshop = get_workshop_by_id(db, workshop_id)
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found",
        )
    return workshop


# ============ Admin Routes ============

@router.post("/", response_model=WorkshopResponse)
def create_new_workshop(
    workshop_data: WorkshopCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Create a new workshop (admin only)
    """
    workshop = create_workshop(db, workshop_data)
    return workshop


@router.patch("/{workshop_id}", response_model=WorkshopResponse)
def update_workshop_details(
    workshop_id: str,
    workshop_update: WorkshopUpdate,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Update a workshop (admin only)
    """
    workshop = update_workshop(
        db, workshop_id, workshop_update.model_dump(exclude_unset=True)
    )
    if not workshop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found",
        )
    return workshop


@router.delete("/{workshop_id}")
def delete_workshop_by_id(
    workshop_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Delete a workshop (admin only)
    """
    success = delete_workshop(db, workshop_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workshop not found",
        )
    return {"success": True, "message": "Workshop deleted successfully"}
