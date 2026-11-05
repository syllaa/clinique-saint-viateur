from datetime import datetime, timezone

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.blog.schemas import (
    ArticleCreate,
    ArticleFaqCreate,
    ArticleFaqUpdate,
    ArticleUpdate,
    BlogCategoryCreate,
    BlogCategoryUpdate,
)
from app.models.article import Article
from app.models.article_faq import ArticleFAQ
from app.models.blog_category import BlogCategory
from app.utils import unique_slug

# ── Categories ────────────────────────────────────────────


def list_categories(db: Session, active_only: bool = True) -> list[BlogCategory]:
    query = db.query(BlogCategory)
    if active_only:
        query = query.filter(BlogCategory.is_active.is_(True))
    return query.order_by(BlogCategory.position, BlogCategory.id).all()


def get_category(db: Session, category_id: int) -> BlogCategory | None:
    return db.get(BlogCategory, category_id)


def create_category(db: Session, data: BlogCategoryCreate) -> BlogCategory:
    slug = unique_slug(
        data.name, exists=lambda s: db.query(BlogCategory).filter(BlogCategory.slug == s).first() is not None
    )
    category = BlogCategory(name=data.name, slug=slug, position=data.position)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category: BlogCategory, data: BlogCategoryUpdate) -> BlogCategory:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


def toggle_category_active(db: Session, category: BlogCategory) -> BlogCategory:
    category.is_active = not category.is_active
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: BlogCategory) -> None:
    db.delete(category)
    db.commit()


# ── Articles ──────────────────────────────────────────────


def list_articles_page(
    db: Session,
    published_only: bool,
    category_slug: str | None,
    search: str | None,
    page: int,
    page_size: int,
) -> tuple[list[Article], int]:
    query = db.query(Article)
    if published_only:
        query = query.filter(Article.status == "published")
    if category_slug:
        query = query.join(BlogCategory).filter(BlogCategory.slug == category_slug)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Article.title.ilike(like), Article.excerpt.ilike(like)))
    total = query.count()
    items = (
        query.order_by(Article.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total


def get_article(db: Session, article_id: int) -> Article | None:
    return db.get(Article, article_id)


def get_article_by_slug(db: Session, slug: str) -> Article | None:
    return db.query(Article).filter(Article.slug == slug).first()


def list_related_articles(db: Session, article: Article, limit: int = 3) -> list[Article]:
    return (
        db.query(Article)
        .filter(
            Article.category_id == article.category_id,
            Article.id != article.id,
            Article.status == "published",
        )
        .order_by(Article.created_at.desc())
        .limit(limit)
        .all()
    )


def create_article(db: Session, data: ArticleCreate) -> Article:
    slug = unique_slug(
        data.title, exists=lambda s: db.query(Article).filter(Article.slug == s).first() is not None
    )
    article = Article(
        **data.model_dump(),
        slug=slug,
        published_at=datetime.now(timezone.utc) if data.status == "published" else None,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(db: Session, article: Article, data: ArticleUpdate) -> Article:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(article, field, value)
    if updates.get("status") == "published" and article.published_at is None:
        article.published_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: Article) -> None:
    db.delete(article)
    db.commit()


# ── FAQs ──────────────────────────────────────────────────


def get_faq(db: Session, faq_id: int) -> ArticleFAQ | None:
    return db.get(ArticleFAQ, faq_id)


def create_faq(db: Session, article_id: int, data: ArticleFaqCreate) -> ArticleFAQ:
    faq = ArticleFAQ(article_id=article_id, **data.model_dump())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


def update_faq(db: Session, faq: ArticleFAQ, data: ArticleFaqUpdate) -> ArticleFAQ:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(faq, field, value)
    db.commit()
    db.refresh(faq)
    return faq


def delete_faq(db: Session, faq: ArticleFAQ) -> None:
    db.delete(faq)
    db.commit()
