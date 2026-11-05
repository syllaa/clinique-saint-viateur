from datetime import date

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.promotion import Promotion
from app.models.promotion_reaction import PromotionReaction
from app.promotions.schemas import PromotionCreate, PromotionUpdate
from app.utils import unique_slug

# ── Promotions ────────────────────────────────────────────


def list_active_promotions(db: Session) -> list[Promotion]:
    today = date.today()
    return (
        db.query(Promotion)
        .filter(Promotion.is_published.is_(True), Promotion.valid_until >= today)
        .order_by(Promotion.position, Promotion.created_at.desc())
        .all()
    )


def list_promotions_page(
    db: Session,
    category: str | None,
    search: str | None,
    sort: str,
    page: int,
    page_size: int,
) -> tuple[list[Promotion], int]:
    query = db.query(Promotion)
    if category:
        query = query.filter(Promotion.category == category)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Promotion.title.ilike(like), Promotion.short_description.ilike(like)))
    total = query.count()
    if sort == "popular":
        counts = (
            db.query(PromotionReaction.promotion_id, func.count(PromotionReaction.id).label("cnt"))
            .group_by(PromotionReaction.promotion_id)
            .subquery()
        )
        query = query.outerjoin(counts, Promotion.id == counts.c.promotion_id).order_by(
            counts.c.cnt.desc().nullslast(), Promotion.created_at.desc()
        )
    else:
        query = query.order_by(Promotion.created_at.desc())
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def list_all_promotions(db: Session) -> list[Promotion]:
    return db.query(Promotion).order_by(Promotion.position, Promotion.created_at.desc()).all()


def list_categories(db: Session) -> list[str]:
    rows = (
        db.query(Promotion.category)
        .filter(Promotion.category.isnot(None), Promotion.category != "")
        .distinct()
        .order_by(Promotion.category)
        .all()
    )
    return [row[0] for row in rows]


def get_promotion(db: Session, promotion_id: int) -> Promotion | None:
    return db.get(Promotion, promotion_id)


def create_promotion(db: Session, data: PromotionCreate) -> Promotion:
    slug = unique_slug(
        data.title, exists=lambda s: db.query(Promotion).filter(Promotion.slug == s).first() is not None
    )
    promotion = Promotion(**data.model_dump(), slug=slug)
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


def update_promotion(db: Session, promotion: Promotion, data: PromotionUpdate) -> Promotion:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(promotion, field, value)
    db.commit()
    db.refresh(promotion)
    return promotion


def toggle_promotion_active(db: Session, promotion: Promotion) -> Promotion:
    promotion.is_published = not promotion.is_published
    db.commit()
    db.refresh(promotion)
    return promotion


def delete_promotion(db: Session, promotion: Promotion) -> None:
    db.delete(promotion)
    db.commit()


# ── Reactions ─────────────────────────────────────────────


def get_reaction_counts(db: Session, promotion_id: int) -> dict[str, int]:
    rows = (
        db.query(PromotionReaction.reaction_type, func.count(PromotionReaction.id))
        .filter(PromotionReaction.promotion_id == promotion_id)
        .group_by(PromotionReaction.reaction_type)
        .all()
    )
    counts = {"like": 0, "interested": 0, "hot": 0, "not_interested": 0}
    for reaction_type, count in rows:
        counts[reaction_type] = count
    return counts


def get_device_reaction(db: Session, promotion_id: int, device_id: str) -> PromotionReaction | None:
    return (
        db.query(PromotionReaction)
        .filter(PromotionReaction.promotion_id == promotion_id, PromotionReaction.device_id == device_id)
        .first()
    )


def upsert_reaction(db: Session, promotion_id: int, device_id: str, reaction_type: str) -> PromotionReaction:
    reaction = get_device_reaction(db, promotion_id, device_id)
    if reaction:
        reaction.reaction_type = reaction_type
    else:
        reaction = PromotionReaction(promotion_id=promotion_id, device_id=device_id, reaction_type=reaction_type)
        db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction
