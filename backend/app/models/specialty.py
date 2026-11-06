from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Specialty(Base):
    """Medical specialty shown on the public site, with its own detail page."""

    __tablename__ = "specialties"

    id: Mapped[int] = mapped_column(primary_key=True)
    icon: Mapped[str | None] = mapped_column(String(10), nullable=True)  # legacy emoji, superseded by icon_name
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(400), default="")
    position: Mapped[int] = mapped_column(Integer, default=0)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    # Media shown on the card / detail header — exactly one of the two is used,
    # selected by media_type ("icon" | "image"); see app/specialties/service.py.
    media_type: Mapped[str] = mapped_column(String(10), default="icon", nullable=False)
    icon_name: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g. "heart-pulse" (Lucide slug)
    cover_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_alt: Mapped[str | None] = mapped_column(String(200), nullable=True)
    # Optional ambient video for the detail page header (uploaded via
    # /api/uploads/videos; only our own /uploads/videos/<uuid> URLs are accepted).
    cover_video_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    services_offered: Mapped[str] = mapped_column(Text, default="", nullable=False)
    symptoms_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    consultation_hours: Mapped[str | None] = mapped_column(String(200), nullable=True)
    practical_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(320), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # cascade="all, delete-orphan" enforces the parent/child cleanup at the ORM level
    # since this project's MySQL tables use the MyISAM engine, which silently ignores
    # FK "ON DELETE CASCADE" clauses (MyISAM has no FK enforcement at all).
    doctors: Mapped[list["SpecialtyDoctor"]] = relationship(
        order_by="SpecialtyDoctor.position", cascade="all, delete-orphan"
    )
    faqs: Mapped[list["SpecialtyFAQ"]] = relationship(
        order_by="SpecialtyFAQ.position", cascade="all, delete-orphan"
    )
