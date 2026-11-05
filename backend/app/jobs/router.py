from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.rate_limit import rate_limit
from app.jobs import crud, service
from app.jobs.schemas import (
    JobApplicationOut,
    JobApplicationStatusUpdate,
    JobOfferCreate,
    JobOfferListOut,
    JobOfferOut,
    JobOfferUpdate,
)
from app.uploads.service import cv_disk_path

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

# ── Offers ────────────────────────────────────────────────


@router.get("/offers", response_model=list[JobOfferListOut])
def list_offers(department: str | None = None, contract_type: str | None = None, db: Session = Depends(get_db)):
    return crud.list_offers(db, True, department, contract_type)


@router.get("/offers/admin/all", response_model=list[JobOfferListOut], dependencies=[Depends(require_admin)])
def list_all_offers(db: Session = Depends(get_db)):
    return crud.list_offers(db, False, None, None)


@router.get("/offers/admin/{offer_id}", response_model=JobOfferOut, dependencies=[Depends(require_admin)])
def get_offer_admin(offer_id: int, db: Session = Depends(get_db)):
    return service.get_offer_or_404(db, offer_id)


@router.post("/offers", response_model=JobOfferOut, status_code=201, dependencies=[Depends(require_admin)])
def create_offer(payload: JobOfferCreate, db: Session = Depends(get_db)):
    return service.create_offer(db, payload)


@router.patch("/offers/{offer_id}", response_model=JobOfferOut, dependencies=[Depends(require_admin)])
def update_offer(offer_id: int, payload: JobOfferUpdate, db: Session = Depends(get_db)):
    offer = service.get_offer_or_404(db, offer_id)
    return service.update_offer(db, offer, payload)


@router.delete("/offers/{offer_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = service.get_offer_or_404(db, offer_id)
    crud.delete_offer(db, offer)


# ── Applications ──────────────────────────────────────────


@router.post(
    "/offers/{slug}/applications",
    response_model=JobApplicationOut,
    status_code=201,
    dependencies=[Depends(rate_limit("application", 5, 3600))],
)
async def submit_application(
    slug: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    cover_letter: str | None = Form(None),
    consent: bool = Form(...),
    cv: UploadFile = File(...),
    website: str | None = Form(None),  # honeypot, see app/site/schemas.py
    db: Session = Depends(get_db),
):
    if website:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Requête invalide")
    return await service.submit_application(db, slug, first_name, last_name, email, phone, cover_letter, consent, cv)


@router.get("/applications", response_model=list[JobApplicationOut], dependencies=[Depends(require_admin)])
def list_applications(offer_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_applications(db, offer_id, status)


@router.patch(
    "/applications/{application_id}/status",
    response_model=JobApplicationOut,
    dependencies=[Depends(require_admin)],
)
def update_application_status(
    application_id: int, payload: JobApplicationStatusUpdate, db: Session = Depends(get_db)
):
    application = service.get_application_or_404(db, application_id)
    return service.update_application_status(db, application, payload.status)


@router.get("/applications/{application_id}/cv", dependencies=[Depends(require_admin)])
def download_cv(application_id: int, db: Session = Depends(get_db)):
    application = service.get_application_or_404(db, application_id)
    path = cv_disk_path(application.cv_path)
    filename = f"CV_{application.last_name}_{application.first_name}.pdf"
    return FileResponse(path, filename=filename, media_type="application/pdf")


# ── Public detail (registered last: the most generic GET pattern) ──


@router.get("/offers/{slug}", response_model=JobOfferOut)
def get_offer_by_slug(slug: str, db: Session = Depends(get_db)):
    return service.get_open_offer_by_slug_or_404(db, slug)
