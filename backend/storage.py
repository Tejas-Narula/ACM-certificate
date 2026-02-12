"""Supabase Storage helpers for certificate images."""
from supabase import create_client
from config import settings
import uuid

BUCKET_NAME = "certificate-images"

_client = None


def get_supabase():
    """Lazily initialise the Supabase client."""
    global _client
    if _client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env"
            )
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client


def _event_folder(event_id: str) -> str:
    """Return the storage folder path for an event."""
    return f"{event_id}"


def upload_image(event_id: str, file_bytes: bytes, filename: str, content_type: str) -> str:
    """Upload an image to Supabase Storage and return the public URL."""
    sb = get_supabase()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "png"
    unique_name = f"{uuid.uuid4().hex[:12]}.{ext}"
    path = f"{_event_folder(event_id)}/{unique_name}"

    sb.storage.from_(BUCKET_NAME).upload(
        path,
        file_bytes,
        file_options={"content-type": content_type},
    )

    public_url = sb.storage.from_(BUCKET_NAME).get_public_url(path)
    return public_url


def list_images(event_id: str) -> list[str]:
    """List all image URLs for an event."""
    sb = get_supabase()
    folder = _event_folder(event_id)

    try:
        files = sb.storage.from_(BUCKET_NAME).list(folder)
    except Exception:
        return []

    urls = []
    for f in files:
        name = f.get("name", "")
        if name and not name.startswith("."):
            url = sb.storage.from_(BUCKET_NAME).get_public_url(f"{folder}/{name}")
            urls.append(url)
    return urls


def delete_image(event_id: str, filename: str) -> bool:
    """Delete a specific image from storage."""
    sb = get_supabase()
    path = f"{_event_folder(event_id)}/{filename}"
    try:
        sb.storage.from_(BUCKET_NAME).remove([path])
        return True
    except Exception:
        return False
