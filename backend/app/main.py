import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.router import router as auth_router
from app.auth.service import ensure_seed_admin, uses_default_password
from app.backups.router import router as backups_router
from app.backups.service import create_backup, ensure_backup_dir, list_backups
from app.blog.router import router as blog_router
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.jobs.router import router as jobs_router
from app.promotions.router import router as promotions_router
from app.seed import ensure_seed_content
from app.site.router import router as site_router
from app.specialties.router import router as specialties_router
from app.support.router import router as support_router
from app.uploads.router import router as uploads_router
from app.uploads.service import ensure_upload_dirs, upload_root

settings = get_settings()
logger = logging.getLogger("backups")
scheduler = BackgroundScheduler()


def run_scheduled_backup() -> None:
    try:
        create_backup()
    except RuntimeError as e:
        logger.error("Scheduled database backup failed: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_upload_dirs()
    ensure_backup_dir()
    db = SessionLocal()
    try:
        ensure_seed_admin(db)
        ensure_seed_content(db)
        if uses_default_password(db):
            logging.getLogger("security").warning(
                "Le compte administrateur utilise encore le mot de passe par défaut. "
                "Changez-le depuis l'administration (Sécurité) avant toute mise en ligne."
            )
    finally:
        db.close()

    if not list_backups():
        run_scheduled_backup()
    scheduler.add_job(
        run_scheduled_backup,
        IntervalTrigger(hours=settings.backup_interval_hours),
        id="db_backup",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(backups_router)
app.include_router(site_router)
app.include_router(specialties_router)
app.include_router(blog_router)
app.include_router(jobs_router)
app.include_router(promotions_router)
app.include_router(support_router)
app.include_router(uploads_router)

# Images and videos are public (specialty/article/job covers, ambient videos). CVs are never mounted here —
# they're only reachable through the authenticated streaming route in app/jobs/router.py.
ensure_upload_dirs()
app.mount("/uploads/images", StaticFiles(directory=str(upload_root() / "images")), name="uploaded-images")
app.mount("/uploads/videos", StaticFiles(directory=str(upload_root() / "videos")), name="uploaded-videos")


@app.get("/")
def health():
    return {"status": "ok", "service": settings.app_name}
