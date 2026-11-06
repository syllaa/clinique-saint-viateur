import io
import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config import get_settings

settings = get_settings()

_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
_CV_EXTENSIONS = {".pdf"}
_VIDEO_EXTENSIONS = {".mp4", ".webm"}
# Public URL of a video this service stored (server-generated UUID name only).
_VIDEO_URL_RE = re.compile(r"/uploads/videos/[0-9a-f]{32}\.(mp4|webm)")
_CHUNK_SIZE = 1024 * 1024
_MAX_IMAGE_DIMENSION = 1600


def upload_root() -> Path:
    return Path(settings.upload_dir)


def ensure_upload_dirs() -> None:
    (upload_root() / "images").mkdir(parents=True, exist_ok=True)
    (upload_root() / "cvs").mkdir(parents=True, exist_ok=True)
    (upload_root() / "videos").mkdir(parents=True, exist_ok=True)


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


def _looks_like(ext: str, raw: bytes) -> bool:
    """Checks the file signature, not just the name: MP4 files carry an
    'ftyp' box at offset 4, WebM files start with the EBML magic number."""
    if ext == ".mp4":
        return raw[4:8] == b"ftyp"
    if ext == ".webm":
        return raw[:4] == bytes([0x1A, 0x45, 0xDF, 0xA3])
    return False


async def save_video(file: UploadFile) -> str:
    """Stores an ambient video (MP4 or WebM) as-is under a random name.
    Videos are not re-encoded server-side: they must be prepared beforehand
    (see docs/medias-a-generer.md)."""
    ext = Path(file.filename or "").suffix.lower()
    if ext not in _VIDEO_EXTENSIONS:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Type de fichier non autorisé ({ext or 'inconnu'}). Autorisés : .mp4, .webm",
        )
    raw = await _read_upload(file, settings.max_video_mb)
    if not _looks_like(ext, raw):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Fichier vidéo invalide ou corrompu")

    ensure_upload_dirs()
    filename = f"{uuid.uuid4().hex}{ext}"
    (upload_root() / "videos" / filename).write_bytes(raw)
    return filename


def video_url(filename: str) -> str:
    return f"/uploads/videos/{filename}"


def is_uploaded_video_url(url: str | None) -> bool:
    return bool(url and _VIDEO_URL_RE.fullmatch(url))


def delete_uploaded_video(url: str | None) -> None:
    """Removes a video file previously stored by save_video. Anything that is
    not one of our own UUID-named files is ignored (no path traversal)."""
    if not is_uploaded_video_url(url):
        return
    (upload_root() / "videos" / url.rsplit("/", 1)[1]).unlink(missing_ok=True)
