"""Search-engine endpoints: /sitemap.xml and /robots.txt.

Served by the API but meant to be exposed at the site root (the reverse
proxy routes them; the Vite dev/preview servers proxy them too). Absolute
URLs use settings.site_url, the public address of the website.
"""
from datetime import date, datetime
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.jobs import crud as jobs_crud
from app.models.article import Article
from app.models.specialty import Specialty

router = APIRouter(tags=["seo"])

# Public, indexable pages that always exist (path, change frequency, priority).
STATIC_PAGES = [
    ("/", "weekly", "1.0"),
    ("/specialites", "monthly", "0.9"),
    ("/blog", "weekly", "0.8"),
    ("/promotions", "weekly", "0.6"),
    ("/nous-rejoindre", "monthly", "0.6"),
]


def _base_url() -> str:
    return get_settings().site_url.rstrip("/")


def _url(loc: str, lastmod: datetime | date | None = None, changefreq: str | None = None, priority: str | None = None) -> str:
    parts = [f"<loc>{escape(_base_url() + loc)}</loc>"]
    if lastmod:
        parts.append(f"<lastmod>{lastmod.date().isoformat() if isinstance(lastmod, datetime) else lastmod.isoformat()}</lastmod>")
    if changefreq:
        parts.append(f"<changefreq>{changefreq}</changefreq>")
    if priority:
        parts.append(f"<priority>{priority}</priority>")
    return "<url>" + "".join(parts) + "</url>"


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap(db: Session = Depends(get_db)) -> Response:
    urls = [_url(path, changefreq=freq, priority=prio) for path, freq, prio in STATIC_PAGES]

    for s in db.query(Specialty).filter(Specialty.is_active.is_(True)).order_by(Specialty.position).all():
        urls.append(_url(f"/specialites/{s.slug}", s.updated_at, "monthly", "0.8"))

    for a in db.query(Article).filter(Article.status == "published").order_by(Article.created_at.desc()).all():
        urls.append(_url(f"/blog/{a.slug}", a.published_at or a.created_at, "monthly", "0.6"))

    for o in jobs_crud.list_offers(db, published_only=True, department=None, contract_type=None):
        urls.append(_url(f"/nous-rejoindre/offres/{o.slug}", o.updated_at, "weekly", "0.5"))

    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    return Response(content=body, media_type="application/xml")


@router.get("/robots.txt", include_in_schema=False, response_class=PlainTextResponse)
def robots() -> str:
    # The admin is not listed here on purpose: naming it would advertise it.
    # It is unreachable without login anyway (and returns a 404 page when locked).
    return f"User-agent: *\nAllow: /\n\nSitemap: {_base_url()}/sitemap.xml\n"
