from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class JobOffer(Base):
    """A job posting shown under "Nous rejoindre"."""

    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    department: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contract_type: Mapped[str] = mapped_column(String(30), nullable=False)  # CDI|CDD|Stage|Freelance
    location: Mapped[str] = mapped_column(String(160), default="Cocody, Abidjan")
    short_description: Mapped[str] = mapped_column(String(400), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    missions: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(60), nullable=True)
    status: Mapped[str] = mapped_column(String(10), default="published", nullable=False)  # published|draft
    application_deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
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

    # See app/models/specialty.py for why cascade is enforced at the ORM level
    # (this project's MySQL tables use MyISAM, which ignores FK ON DELETE CASCADE).
    applications: Mapped[list["JobApplication"]] = relationship(cascade="all, delete-orphan")
