from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.promotion import Promotion
from app.promotions import crud

VALID_REACTION_TYPES = {"like", "interested", "hot", "not_interested"}


def get_promotion_or_404(db: Session, promotion_id: int) -> Promotion:
    promotion = crud.get_promotion(db, promotion_id)
    if not promotion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre introuvable")
    return promotion


def enrich(db: Session, promotions: list[Promotion], device_id: str | None) -> list[Promotion]:
    """Attaches the computed fields (is_expired, reaction_counts, my_reaction) that
    schemas.PromotionListOut expects but that aren't real columns."""
    today = date.today()
    for promotion in promotions:
        promotion.is_expired = promotion.valid_until < today
        promotion.reaction_counts = crud.get_reaction_counts(db, promotion.id)
        promotion.my_reaction = None
        if device_id:
            reaction = crud.get_device_reaction(db, promotion.id, device_id)
            promotion.my_reaction = reaction.reaction_type if reaction else None
    return promotions


def enrich_one(db: Session, promotion: Promotion, device_id: str | None) -> Promotion:
    return enrich(db, [promotion], device_id)[0]


def react(db: Session, promotion_id: int, device_id: str, reaction_type: str) -> Promotion:
    """The single place offer validity is enforced for reactions — reached no
    matter what the UI shows, so an expired/unpublished/nonexistent offer can
    never be reacted to via a direct request either."""
    if reaction_type not in VALID_REACTION_TYPES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Type de réaction invalide")
    if not device_id or not device_id.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Identifiant appareil requis")

    promotion = crud.get_promotion(db, promotion_id)
    if not promotion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Offre introuvable")
    if not promotion.is_published:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cette offre n'est plus disponible.")
    if promotion.valid_until < date.today():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cette offre a expiré, vous ne pouvez plus réagir.")

    device_id = device_id.strip()
    crud.upsert_reaction(db, promotion_id, device_id, reaction_type)
    return enrich_one(db, promotion, device_id)
