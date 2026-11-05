from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.blog import crud, service
from app.blog.schemas import (
    ArticleCreate,
    ArticleFaqCreate,
    ArticleFaqOut,
    ArticleFaqUpdate,
    ArticleListOut,
    ArticleOut,
    ArticlePageOut,
    ArticleUpdate,
    BlogCategoryCreate,
    BlogCategoryOut,
    BlogCategoryUpdate,
)
from app.database import get_db

router = APIRouter(prefix="/api/blog", tags=["blog"])

# ── Categories ────────────────────────────────────────────


@router.get("/categories", response_model=list[BlogCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db, active_only=True)


@router.get("/categories/admin/all", response_model=list[BlogCategoryOut], dependencies=[Depends(require_admin)])
def list_all_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db, active_only=False)


@router.post("/categories", response_model=BlogCategoryOut, status_code=201, dependencies=[Depends(require_admin)])
def create_category(payload: BlogCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, payload)


@router.patch("/categories/{category_id}", response_model=BlogCategoryOut, dependencies=[Depends(require_admin)])
def update_category(category_id: int, payload: BlogCategoryUpdate, db: Session = Depends(get_db)):
    category = service.get_category_or_404(db, category_id)
    return crud.update_category(db, category, payload)


@router.patch(
    "/categories/{category_id}/toggle-active",
    response_model=BlogCategoryOut,
    dependencies=[Depends(require_admin)],
)
def toggle_category(category_id: int, db: Session = Depends(get_db)):
    category = service.get_category_or_404(db, category_id)
    return crud.toggle_category_active(db, category)


@router.delete("/categories/{category_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = service.get_category_or_404(db, category_id)
    crud.delete_category(db, category)


# ── Articles ──────────────────────────────────────────────


@router.get("/articles", response_model=ArticlePageOut)
def list_articles(
    search: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(9, ge=1, le=50),
    db: Session = Depends(get_db),
):
    items, total = crud.list_articles_page(db, True, category, search, page, page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/articles/admin/all", response_model=ArticlePageOut, dependencies=[Depends(require_admin)])
def list_all_articles(
    search: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = crud.list_articles_page(db, False, category, search, page, page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/articles/admin/{article_id}", response_model=ArticleOut, dependencies=[Depends(require_admin)])
def get_article_admin(article_id: int, db: Session = Depends(get_db)):
    return service.get_article_or_404(db, article_id)


@router.post("/articles", response_model=ArticleOut, status_code=201, dependencies=[Depends(require_admin)])
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    return service.create_article(db, payload)


@router.patch("/articles/{article_id}", response_model=ArticleOut, dependencies=[Depends(require_admin)])
def update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)):
    article = service.get_article_or_404(db, article_id)
    return service.update_article(db, article, payload)


@router.delete("/articles/{article_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = service.get_article_or_404(db, article_id)
    crud.delete_article(db, article)


@router.get("/articles/{slug}/related", response_model=list[ArticleListOut])
def get_related_articles(slug: str, db: Session = Depends(get_db)):
    article = service.get_published_article_by_slug_or_404(db, slug)
    return crud.list_related_articles(db, article)


# ── FAQs (admin) ──────────────────────────────────────────


@router.post(
    "/articles/{article_id}/faqs", response_model=ArticleFaqOut, status_code=201, dependencies=[Depends(require_admin)]
)
def create_article_faq(article_id: int, payload: ArticleFaqCreate, db: Session = Depends(get_db)):
    service.get_article_or_404(db, article_id)
    return crud.create_faq(db, article_id, payload)


@router.patch("/articles/faqs/{faq_id}", response_model=ArticleFaqOut, dependencies=[Depends(require_admin)])
def update_article_faq(faq_id: int, payload: ArticleFaqUpdate, db: Session = Depends(get_db)):
    faq = service.get_faq_or_404(db, faq_id)
    return crud.update_faq(db, faq, payload)


@router.delete("/articles/faqs/{faq_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_article_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = service.get_faq_or_404(db, faq_id)
    crud.delete_faq(db, faq)


# ── Public detail (registered last: the most generic GET pattern) ──


@router.get("/articles/{slug}", response_model=ArticleOut)
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    return service.get_published_article_by_slug_or_404(db, slug)
