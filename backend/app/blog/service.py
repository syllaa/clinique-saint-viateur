from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.blog import crud
from app.blog.schemas import ArticleCreate, ArticleUpdate
from app.models.article import Article
from app.utils import sanitize_html


def get_category_or_404(db: Session, category_id: int):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Catégorie introuvable")
    return category


def get_article_or_404(db: Session, article_id: int) -> Article:
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Article introuvable")
    return article


def get_published_article_by_slug_or_404(db: Session, slug: str) -> Article:
    article = crud.get_article_by_slug(db, slug)
    if not article or article.status != "published":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Article introuvable")
    return article


def create_article(db: Session, data: ArticleCreate) -> Article:
    if not data.title.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Titre requis")
    get_category_or_404(db, data.category_id)
    data = data.model_copy(update={"content": sanitize_html(data.content)})
    return crud.create_article(db, data)


def update_article(db: Session, article: Article, data: ArticleUpdate) -> Article:
    if data.category_id is not None:
        get_category_or_404(db, data.category_id)
    if data.content is not None:
        data = data.model_copy(update={"content": sanitize_html(data.content)})
    return crud.update_article(db, article, data)


def get_faq_or_404(db: Session, faq_id: int):
    faq = crud.get_faq(db, faq_id)
    if not faq:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Question introuvable")
    return faq
