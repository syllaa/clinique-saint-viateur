from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobApplication(Base):
    """A candidacy submitted against one job offer, with an uploaded CV."""

    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_offer_id: Mapped[int] = mapped_column(
        ForeignKey("job_offers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    cv_path: Mapped[str] = mapped_column(String(255), nullable=False)  # server-generated filename only
    consent_given_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="nouvelle", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
