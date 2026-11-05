from sqlalchemy.orm import Session

from app.models.specialty import Specialty
from app.models.specialty_doctor import SpecialtyDoctor
from app.models.specialty_faq import SpecialtyFAQ
from app.specialties.schemas import (
    SpecialtyCreate,
    SpecialtyDoctorCreate,
    SpecialtyDoctorUpdate,
    SpecialtyFaqCreate,
    SpecialtyFaqUpdate,
    SpecialtyUpdate,
)
from app.utils import unique_slug

# ── Specialties ───────────────────────────────────────────


def list_specialties(db: Session, active_only: bool = True) -> list[Specialty]:
    query = db.query(Specialty)
    if active_only:
        query = query.filter(Specialty.is_active.is_(True))
    return query.order_by(Specialty.position, Specialty.id).all()


def get_specialty(db: Session, specialty_id: int) -> Specialty | None:
    return db.get(Specialty, specialty_id)


def get_specialty_by_slug(db: Session, slug: str) -> Specialty | None:
    return db.query(Specialty).filter(Specialty.slug == slug).first()


def create_specialty(db: Session, data: SpecialtyCreate) -> Specialty:
    slug = unique_slug(
        data.name, exists=lambda s: db.query(Specialty).filter(Specialty.slug == s).first() is not None
    )
    specialty = Specialty(**data.model_dump(), slug=slug)
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty


def update_specialty(db: Session, specialty: Specialty, data: SpecialtyUpdate) -> Specialty:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(specialty, field, value)
    db.commit()
    db.refresh(specialty)
    return specialty


def toggle_active(db: Session, specialty: Specialty) -> Specialty:
    specialty.is_active = not specialty.is_active
    db.commit()
    db.refresh(specialty)
    return specialty


def delete_specialty(db: Session, specialty: Specialty) -> None:
    db.delete(specialty)
    db.commit()


# ── Doctors ───────────────────────────────────────────────


def get_doctor(db: Session, doctor_id: int) -> SpecialtyDoctor | None:
    return db.get(SpecialtyDoctor, doctor_id)


def create_doctor(db: Session, specialty_id: int, data: SpecialtyDoctorCreate) -> SpecialtyDoctor:
    doctor = SpecialtyDoctor(specialty_id=specialty_id, **data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor(db: Session, doctor: SpecialtyDoctor, data: SpecialtyDoctorUpdate) -> SpecialtyDoctor:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor: SpecialtyDoctor) -> None:
    db.delete(doctor)
    db.commit()


# ── FAQs ──────────────────────────────────────────────────


def get_faq(db: Session, faq_id: int) -> SpecialtyFAQ | None:
    return db.get(SpecialtyFAQ, faq_id)


def create_faq(db: Session, specialty_id: int, data: SpecialtyFaqCreate) -> SpecialtyFAQ:
    faq = SpecialtyFAQ(specialty_id=specialty_id, **data.model_dump())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


def update_faq(db: Session, faq: SpecialtyFAQ, data: SpecialtyFaqUpdate) -> SpecialtyFAQ:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(faq, field, value)
    db.commit()
    db.refresh(faq)
    return faq


def delete_faq(db: Session, faq: SpecialtyFAQ) -> None:
    db.delete(faq)
    db.commit()
