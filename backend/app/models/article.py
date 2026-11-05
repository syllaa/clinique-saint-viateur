from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.blog_category import BlogCategory


class Article(Base):
    """Blog / news article shown on the public site."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True, nullable=False)
    excerpt: Mapped[str] = mapped_column(String(400), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    category_id: Mapped[int] = mapped_column(ForeignKey("blog_categories.id"), nullable=False)
    category: Mapped["BlogCategory"] = relationship(lazy="joined")
    author: Mapped[str] = mapped_column(String(120), default="Clinique Saint Viateur", nullable=False)
    cover_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    icon: Mapped[str] = mapped_column(String(10), default="📋", nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="published", nullable=False)  # published|draft
    # Optional structured sections for richer "event/campaign" style posts — plain
    # newline-delimited text, one item per line, each starting with an emoji
    # (e.g. "📅 29 septembre 2026"), parsed client-side into icon cards. Same
    # pattern as Specialty.services_offered/practical_info; empty for most posts.
    practical_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    included_items: Mapped[str | None] = mapped_column(Text, nullable=True)
    benefits: Mapped[str | None] = mapped_column(Text, nullable=True)
    secondary_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    secondary_image_alt: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(320), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # cascade="all, delete-orphan" enforces parent/child cleanup at the ORM level —
    # see app/models/specialty.py for why (MyISAM ignores FK ON DELETE CASCADE).
    faqs: Mapped[list["ArticleFAQ"]] = relationship(order_by="ArticleFAQ.position", cascade="all, delete-orphan")
