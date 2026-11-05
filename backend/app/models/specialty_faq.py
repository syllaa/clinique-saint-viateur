from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SpecialtyFAQ(Base):
    """A single FAQ entry (question/answer) on one medical specialty's detail page."""

    __tablename__ = "specialty_faqs"

    id: Mapped[int] = mapped_column(primary_key=True)
    specialty_id: Mapped[int] = mapped_column(
        ForeignKey("specialties.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question: Mapped[str] = mapped_column(String(300), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)
