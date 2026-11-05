from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "Clinique Saint Viateur API"
    debug: bool = False

    # Database (MySQL)
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "clinique_saint_viateur"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # Auth
    secret_key: str = "change-me-in-.env"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # Seed admin (used once at startup if no user exists)
    admin_username: str = "admin"
    admin_password: str = "admin123"

    # Uploads (images are served publicly from upload_dir/images; CVs never are)
    upload_dir: str = "uploads"
    max_image_mb: int = 5
    max_cv_mb: int = 5

    # Automatic database backups (mysqldump). mysqldump_path lets a local dev
    # setup (e.g. XAMPP on Windows) point at a binary that isn't on PATH; on a
    # real server "mysqldump" alone is normally enough.
    backup_dir: str = "backups"
    backup_retention_days: int = 14
    backup_interval_hours: int = 24
    mysqldump_path: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
