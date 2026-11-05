from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Promotion(Base):
    """A time-limited promotional offer shown on the homepage carousel and the
    dedicated offers page. Named "Promotion" (not "Offer") because that name is
    already taken by JobOffer (recruitment postings) elsewhere in this codebase."""

    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    short_description: Mapped[str] = mapped_column(Text, default="")
    value_label: Mapped[str] = mapped_column(String(120), default="")  # e.g. "-20%", "Consultation offerte"
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_alt: Mapped[str | None] = mapped_column(String(200), nullable=True)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # See app/models/job_offer.py for why cascade is enforced at the ORM level
    # (this project's MySQL tables use MyISAM, which ignores FK ON DELETE CASCADE).
    reactions: Mapped[list["PromotionReaction"]] = relationship(cascade="all, delete-orphan")
