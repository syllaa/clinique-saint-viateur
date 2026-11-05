import io
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config import get_settings

settings = get_settings()

_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
_CV_EXTENSIONS = {".pdf"}
_CHUNK_SIZE = 1024 * 1024
_MAX_IMAGE_DIMENSION = 1600


def upload_root() -> Path:
    return Path(settings.upload_dir)


def ensure_upload_dirs() -> None:
    (upload_root() / "images").mkdir(parents=True, exist_ok=True)
    (upload_root() / "cvs").mkdir(parents=True, exist_ok=True)


async def _read_upload(file: UploadFile, max_mb: int) -> bytes:
    max_bytes = max_mb * 1024 * 1024
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await file.read(_CHUNK_SIZE)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Fichier trop volumineux (max {max_mb} Mo)")
        chunks.append(chunk)
    if total == 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Fichier vide")
    return b"".join(chunks)


async def save_image(file: UploadFile) -> str:
    """Validate then re-encode every uploaded image as WEBP.

    Re-encoding via Pillow both optimizes/unifies storage and acts as a strong
    content check: a renamed non-image file fails to decode here regardless of
    what its extension or declared content-type claimed (defense in depth on
    top of the extension whitelist).
    """
    ext = Path(file.filename or "").suffix.lower()
    if ext not in _IMAGE_EXTENSIONS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Type de fichier non autorisé ({ext or 'inconnu'}). Autorisés : {', '.join(sorted(_IMAGE_EXTENSIONS))}",
        )
    raw = await _read_upload(file, settings.max_image_mb)

    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Fichier image invalide ou corrompu")

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
    image.thumbnail((_MAX_IMAGE_DIMENSION, _MAX_IMAGE_DIMENSION))

    ensure_upload_dirs()
    filename = f"{uuid.uuid4().hex}.webp"
    target = upload_root() / "images" / filename
    image.save(target, format="WEBP", quality=82, method=6)
    return filename


async def save_cv(file: UploadFile) -> str:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in _CV_EXTENSIONS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Type de fichier non autorisé ({ext or 'inconnu'}). Autorisés : {', '.join(sorted(_CV_EXTENSIONS))}",
        )
    raw = await _read_upload(file, settings.max_cv_mb)
    if not raw.startswith(b"%PDF-"):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Fichier PDF invalide")

    ensure_upload_dirs()
    filename = f"{uuid.uuid4().hex}.pdf"
    target = upload_root() / "cvs" / filename
    target.write_bytes(raw)
    return filename


def cv_disk_path(filename: str) -> Path:
    """Resolve a stored CV filename to its on-disk path. `filename` is always a
    server-generated UUID (never user input), so no path-traversal risk here."""
    return upload_root() / "cvs" / filename


def image_url(filename: str) -> str:
    return f"/uploads/images/{filename}"
