from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.specialties import crud
from app.specialties.schemas import SpecialtyCreate, SpecialtyUpdate

VALID_MEDIA_TYPES = {"icon", "image"}
DEFAULT_ICON_NAME = "hospital"


def _validate_media(media_type: str | None, icon_name: str | None, cover_image_url: str | None) -> None:
    if media_type is not None and media_type not in VALID_MEDIA_TYPES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Type de média invalide")
    if media_type == "image" and not cover_image_url:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, "Une image doit être téléversée pour ce type de média"
        )


def create_specialty(db: Session, data: SpecialtyCreate):
    _validate_media(data.media_type, data.icon_name, data.cover_image_url)
    if data.media_type == "icon" and not data.icon_name:
        data = data.model_copy(update={"icon_name": DEFAULT_ICON_NAME})
    return crud.create_specialty(db, data)


def update_specialty(db: Session, specialty, data: SpecialtyUpdate):
    # Validate against the resulting state (existing values overridden by any
    # provided ones), not just the partial payload in isolation.
    resulting_media_type = data.media_type if data.media_type is not None else specialty.media_type
    resulting_cover_image_url = (
        data.cover_image_url if "cover_image_url" in data.model_fields_set else specialty.cover_image_url
    )
    _validate_media(resulting_media_type, None, resulting_cover_image_url)
    return crud.update_specialty(db, specialty, data)


def get_specialty_or_404(db: Session, specialty_id: int):
    specialty = crud.get_specialty(db, specialty_id)
    if not specialty:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Spécialité introuvable")
    return specialty


def get_active_specialty_by_slug_or_404(db: Session, slug: str):
    specialty = crud.get_specialty_by_slug(db, slug)
    if not specialty or not specialty.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Spécialité introuvable")
    return specialty


def get_doctor_or_404(db: Session, doctor_id: int):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Médecin introuvable")
    return doctor


def get_faq_or_404(db: Session, faq_id: int):
    faq = crud.get_faq(db, faq_id)
    if not faq:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Question introuvable")
    return faq
