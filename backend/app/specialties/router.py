from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.specialties import crud, service
from app.specialties.schemas import (
    SpecialtyCreate,
    SpecialtyDoctorCreate,
    SpecialtyDoctorOut,
    SpecialtyDoctorUpdate,
    SpecialtyFaqCreate,
    SpecialtyFaqOut,
    SpecialtyFaqUpdate,
    SpecialtyListOut,
    SpecialtyOut,
    SpecialtyUpdate,
)

router = APIRouter(prefix="/api/specialties", tags=["specialties"])

# ── Public ────────────────────────────────────────────────


@router.get("", response_model=list[SpecialtyListOut])
def list_specialties(db: Session = Depends(get_db)):
    return crud.list_specialties(db, active_only=True)


# ── Admin ─────────────────────────────────────────────────


@router.get("/admin/all", response_model=list[SpecialtyListOut], dependencies=[Depends(require_admin)])
def list_all_specialties(db: Session = Depends(get_db)):
    return crud.list_specialties(db, active_only=False)


@router.get("/admin/{specialty_id}", response_model=SpecialtyOut, dependencies=[Depends(require_admin)])
def get_specialty_admin(specialty_id: int, db: Session = Depends(get_db)):
    return service.get_specialty_or_404(db, specialty_id)


@router.post("", response_model=SpecialtyOut, status_code=201, dependencies=[Depends(require_admin)])
def create_specialty(payload: SpecialtyCreate, db: Session = Depends(get_db)):
    return service.create_specialty(db, payload)


@router.patch("/{specialty_id}", response_model=SpecialtyOut, dependencies=[Depends(require_admin)])
def update_specialty(specialty_id: int, payload: SpecialtyUpdate, db: Session = Depends(get_db)):
    specialty = service.get_specialty_or_404(db, specialty_id)
    return service.update_specialty(db, specialty, payload)


@router.patch(
    "/{specialty_id}/toggle-active", response_model=SpecialtyOut, dependencies=[Depends(require_admin)]
)
def toggle_specialty_active(specialty_id: int, db: Session = Depends(get_db)):
    specialty = service.get_specialty_or_404(db, specialty_id)
    return crud.toggle_active(db, specialty)


@router.delete("/{specialty_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_specialty(specialty_id: int, db: Session = Depends(get_db)):
    specialty = service.get_specialty_or_404(db, specialty_id)
    crud.delete_specialty(db, specialty)


# ── Doctors (admin) ───────────────────────────────────────


@router.post(
    "/{specialty_id}/doctors", response_model=SpecialtyDoctorOut, status_code=201, dependencies=[Depends(require_admin)]
)
def create_doctor(specialty_id: int, payload: SpecialtyDoctorCreate, db: Session = Depends(get_db)):
    service.get_specialty_or_404(db, specialty_id)
    return crud.create_doctor(db, specialty_id, payload)


@router.patch("/doctors/{doctor_id}", response_model=SpecialtyDoctorOut, dependencies=[Depends(require_admin)])
def update_doctor(doctor_id: int, payload: SpecialtyDoctorUpdate, db: Session = Depends(get_db)):
    doctor = service.get_doctor_or_404(db, doctor_id)
    return crud.update_doctor(db, doctor, payload)


@router.delete("/doctors/{doctor_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = service.get_doctor_or_404(db, doctor_id)
    crud.delete_doctor(db, doctor)


# ── FAQs (admin) ──────────────────────────────────────────


@router.post(
    "/{specialty_id}/faqs", response_model=SpecialtyFaqOut, status_code=201, dependencies=[Depends(require_admin)]
)
def create_faq(specialty_id: int, payload: SpecialtyFaqCreate, db: Session = Depends(get_db)):
    service.get_specialty_or_404(db, specialty_id)
    return crud.create_faq(db, specialty_id, payload)


@router.patch("/faqs/{faq_id}", response_model=SpecialtyFaqOut, dependencies=[Depends(require_admin)])
def update_faq(faq_id: int, payload: SpecialtyFaqUpdate, db: Session = Depends(get_db)):
    faq = service.get_faq_or_404(db, faq_id)
    return crud.update_faq(db, faq, payload)


@router.delete("/faqs/{faq_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = service.get_faq_or_404(db, faq_id)
    crud.delete_faq(db, faq)


# ── Public detail (registered last: the most generic GET pattern) ──


@router.get("/{slug}", response_model=SpecialtyOut)
def get_specialty_by_slug(slug: str, db: Session = Depends(get_db)):
    return service.get_active_specialty_by_slug_or_404(db, slug)
