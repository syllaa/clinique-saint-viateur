from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SpecialtyDoctor(Base):
    """A doctor listed under one medical specialty's detail page."""

    __tablename__ = "specialty_doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    specialty_id: Mapped[int] = mapped_column(
        ForeignKey("specialties.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    title: Mapped[str | None] = mapped_column(String(150), nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(400), nullable=True)
    position: Mapped[int] = mapped_column(Integer, default=0)
