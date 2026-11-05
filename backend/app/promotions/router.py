from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.rate_limit import rate_limit
from app.promotions import crud, service
from app.promotions.schemas import (
    PromotionCreate,
    PromotionListOut,
    PromotionOut,
    PromotionPageOut,
    PromotionUpdate,
    ReactionIn,
)

router = APIRouter(prefix="/api/promotions", tags=["promotions"])

# ── Public ────────────────────────────────────────────────


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.get("", response_model=list[PromotionListOut])
def list_active_promotions(device_id: str | None = None, db: Session = Depends(get_db)):
    promotions = crud.list_active_promotions(db)
    return service.enrich(db, promotions, device_id)


@router.get("/all", response_model=PromotionPageOut)
def list_all_promotions(
    search: str | None = None,
    category: str | None = None,
    sort: str = Query("date", pattern="^(date|popular)$"),
    device_id: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    items, total = crud.list_promotions_page(db, category, search, sort, page, page_size)
    service.enrich(db, items, device_id)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post(
    "/{promotion_id}/reactions",
    response_model=PromotionOut,
    dependencies=[Depends(rate_limit("reaction", 30, 60))],
)
def react_to_promotion(promotion_id: int, payload: ReactionIn, db: Session = Depends(get_db)):
    return service.react(db, promotion_id, payload.device_id, payload.reaction_type)


# ── Admin ─────────────────────────────────────────────────


@router.get("/admin/all", response_model=list[PromotionListOut], dependencies=[Depends(require_admin)])
def list_all_promotions_admin(db: Session = Depends(get_db)):
    promotions = crud.list_all_promotions(db)
    return service.enrich(db, promotions, None)


@router.get("/admin/{promotion_id}", response_model=PromotionOut, dependencies=[Depends(require_admin)])
def get_promotion_admin(promotion_id: int, db: Session = Depends(get_db)):
    promotion = service.get_promotion_or_404(db, promotion_id)
    return service.enrich_one(db, promotion, None)


@router.post("", response_model=PromotionOut, status_code=201, dependencies=[Depends(require_admin)])
def create_promotion(payload: PromotionCreate, db: Session = Depends(get_db)):
    promotion = crud.create_promotion(db, payload)
    return service.enrich_one(db, promotion, None)


@router.patch("/{promotion_id}", response_model=PromotionOut, dependencies=[Depends(require_admin)])
def update_promotion(promotion_id: int, payload: PromotionUpdate, db: Session = Depends(get_db)):
    promotion = service.get_promotion_or_404(db, promotion_id)
    promotion = crud.update_promotion(db, promotion, payload)
    return service.enrich_one(db, promotion, None)


@router.patch("/{promotion_id}/toggle-active", response_model=PromotionOut, dependencies=[Depends(require_admin)])
def toggle_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = service.get_promotion_or_404(db, promotion_id)
    promotion = crud.toggle_promotion_active(db, promotion)
    return service.enrich_one(db, promotion, None)


@router.delete("/{promotion_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = service.get_promotion_or_404(db, promotion_id)
    crud.delete_promotion(db, promotion)
