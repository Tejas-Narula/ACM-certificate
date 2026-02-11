"""Image upload / list / delete endpoints for certificate templates per event."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from models import Admin
from auth import get_current_admin
from storage import upload_image, list_images, delete_image

router = APIRouter(prefix="/api/events", tags=["images"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp", "image/jpg"}


@router.post("/{event_id}/images")
async def upload_event_image(
    event_id: str,
    file: UploadFile = File(...),
    current_admin: Admin = Depends(get_current_admin),
):
    """Upload a certificate template image for an event (admin only)."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Use PNG, JPEG, or WebP.",
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 10 MB.",
        )

    try:
        url = upload_image(event_id, contents, file.filename or "image.png", file.content_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}",
        )

    return {"url": url}


@router.get("/{event_id}/images")
async def get_event_images(event_id: str):
    """List all uploaded certificate images for an event (public)."""
    urls = list_images(event_id)
    return {"images": urls}


@router.delete("/{event_id}/images/{filename}")
async def delete_event_image(
    event_id: str,
    filename: str,
    current_admin: Admin = Depends(get_current_admin),
):
    """Delete a certificate image (admin only)."""
    success = delete_image(event_id, filename)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return {"success": True, "message": "Image deleted"}
