import re
from datetime import date

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.jobs import crud
from app.jobs.schemas import JobOfferCreate, JobOfferUpdate
from app.uploads.service import save_cv
from app.utils import sanitize_html

VALID_CONTRACT_TYPES = {"CDI", "CDD", "Stage", "Freelance"}
VALID_APPLICATION_STATUSES = {"nouvelle", "en_cours", "retenue", "rejetee"}
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_offer_or_404(db: Session, offer_id: int):
    offer = crud.get_offer(db, offer_id)
    if not offer:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre introuvable")
    return offer


def get_open_offer_by_slug_or_404(db: Session, slug: str):
    offer = crud.get_offer_by_slug(db, slug)
    if not offer or offer.status != "published":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre introuvable")
    if offer.application_deadline and offer.application_deadline < date.today():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre introuvable")
    return offer


def get_application_or_404(db: Session, application_id: int):
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Candidature introuvable")
    return application


def create_offer(db: Session, data: JobOfferCreate):
    if data.contract_type not in VALID_CONTRACT_TYPES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Type de contrat invalide")
    data = data.model_copy(update={"description": sanitize_html(data.description)})
    return crud.create_offer(db, data)


def update_offer(db: Session, offer, data: JobOfferUpdate):
    if data.contract_type is not None and data.contract_type not in VALID_CONTRACT_TYPES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Type de contrat invalide")
    if data.description is not None:
        data = data.model_copy(update={"description": sanitize_html(data.description)})
    return crud.update_offer(db, offer, data)


async def submit_application(
    db: Session,
    slug: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    cover_letter: str | None,
    consent: bool,
    cv: UploadFile,
):
    offer = get_open_offer_by_slug_or_404(db, slug)
    if not first_name.strip() or not last_name.strip() or not phone.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Nom, prénom et téléphone sont requis")
    if not _EMAIL_RE.match(email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Email invalide")
    if not consent:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, "Le consentement au traitement des données est requis"
        )
    cv_filename = await save_cv(cv)
    return crud.create_application(
        db,
        job_offer_id=offer.id,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        cover_letter=cover_letter.strip() if cover_letter else None,
        cv_path=cv_filename,
    )


def update_application_status(db: Session, application, new_status: str):
    if new_status not in VALID_APPLICATION_STATUSES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Statut invalide")
    return crud.update_application_status(db, application, new_status)
