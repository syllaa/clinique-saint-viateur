from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PromotionReaction(Base):
    """One anonymous device's reaction to one promotion. The site has no public
    user accounts, so reactions are keyed by a client-generated device id
    (stored in the visitor's browser) rather than a user id. One row per
    (promotion, device) — changing a reaction updates this row in place."""

    __tablename__ = "promotion_reactions"
    __table_args__ = (UniqueConstraint("promotion_id", "device_id", name="uq_promotion_reaction_device"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    promotion_id: Mapped[int] = mapped_column(
        ForeignKey("promotions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    device_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reaction_type: Mapped[str] = mapped_column(String(20), nullable=False)  # like|interested|hot|not_interested
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
