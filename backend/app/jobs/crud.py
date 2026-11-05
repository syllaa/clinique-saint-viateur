from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.jobs.schemas import JobOfferCreate, JobOfferUpdate
from app.models.job_application import JobApplication
from app.models.job_offer import JobOffer
from app.utils import unique_slug

# ── Offers ────────────────────────────────────────────────


def list_offers(
    db: Session, published_only: bool, department: str | None, contract_type: str | None
) -> list[JobOffer]:
    query = db.query(JobOffer)
    if published_only:
        query = query.filter(JobOffer.status == "published")
        today = date.today()
        query = query.filter((JobOffer.application_deadline.is_(None)) | (JobOffer.application_deadline >= today))
    if department:
        query = query.filter(JobOffer.department == department)
    if contract_type:
        query = query.filter(JobOffer.contract_type == contract_type)
    return query.order_by(JobOffer.created_at.desc()).all()


def get_offer(db: Session, offer_id: int) -> JobOffer | None:
    return db.get(JobOffer, offer_id)


def get_offer_by_slug(db: Session, slug: str) -> JobOffer | None:
    return db.query(JobOffer).filter(JobOffer.slug == slug).first()


def create_offer(db: Session, data: JobOfferCreate) -> JobOffer:
    slug = unique_slug(
        data.title, exists=lambda s: db.query(JobOffer).filter(JobOffer.slug == s).first() is not None
    )
    offer = JobOffer(**data.model_dump(), slug=slug)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer


def update_offer(db: Session, offer: JobOffer, data: JobOfferUpdate) -> JobOffer:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(offer, field, value)
    db.commit()
    db.refresh(offer)
    return offer


def delete_offer(db: Session, offer: JobOffer) -> None:
    db.delete(offer)
    db.commit()


# ── Applications ──────────────────────────────────────────


def list_applications(db: Session, offer_id: int | None, status: str | None) -> list[JobApplication]:
    query = db.query(JobApplication)
    if offer_id:
        query = query.filter(JobApplication.job_offer_id == offer_id)
    if status:
        query = query.filter(JobApplication.status == status)
    return query.order_by(JobApplication.created_at.desc()).all()


def get_application(db: Session, application_id: int) -> JobApplication | None:
    return db.get(JobApplication, application_id)


def create_application(
    db: Session,
    job_offer_id: int,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    cover_letter: str | None,
    cv_path: str,
) -> JobApplication:
    application = JobApplication(
        job_offer_id=job_offer_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        cover_letter=cover_letter,
        cv_path=cv_path,
        consent_given_at=datetime.now(timezone.utc),
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application_status(db: Session, application: JobApplication, new_status: str) -> JobApplication:
    application.status = new_status
    db.commit()
    db.refresh(application)
    return application
