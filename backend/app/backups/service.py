import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, status

from app.config import get_settings

settings = get_settings()

_FILENAME_RE = re.compile(r"backup_\d{8}_\d{6}\.sql")


def backup_root() -> Path:
    return Path(settings.backup_dir)


def ensure_backup_dir() -> None:
    backup_root().mkdir(parents=True, exist_ok=True)


def _mysqldump_bin() -> str:
    return settings.mysqldump_path or "mysqldump"


def _describe(path: Path) -> dict:
    stat = path.stat()
    return {
        "filename": path.name,
        "size_bytes": stat.st_size,
        "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
    }


def list_backups() -> list[dict]:
    ensure_backup_dir()
    files = sorted(backup_root().glob("backup_*.sql"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [_describe(f) for f in files]


def _apply_retention() -> None:
    cutoff = datetime.now(timezone.utc).timestamp() - settings.backup_retention_days * 86400
    for f in backup_root().glob("backup_*.sql"):
        if f.stat().st_mtime < cutoff:
            f.unlink(missing_ok=True)


def create_backup() -> dict:
    """Runs mysqldump and writes a timestamped .sql file. Raises RuntimeError
    (caller decides how to surface it — HTTPException for the API, a log line
    for the scheduled job) with mysqldump's stderr on failure."""
    ensure_backup_dir()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    target = backup_root() / f"backup_{timestamp}.sql"

    cmd = [
        _mysqldump_bin(),
        f"--host={settings.db_host}",
        f"--port={settings.db_port}",
        f"--user={settings.db_user}",
        "--single-transaction",
        "--routines",
        "--triggers",
        settings.db_name,
    ]
    # Password passed via env var, never on the command line (which is visible
    # to other processes/users via the OS process list).
    env = {**os.environ}
    if settings.db_password:
        env["MYSQL_PWD"] = settings.db_password

    try:
        with open(target, "wb") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, env=env, timeout=300)
    except FileNotFoundError:
        target.unlink(missing_ok=True)
        raise RuntimeError(
            f"mysqldump introuvable ({_mysqldump_bin()}). Vérifiez MYSQLDUMP_PATH dans la configuration."
        )

    if result.returncode != 0 or target.stat().st_size == 0:
        target.unlink(missing_ok=True)
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace") or "Échec de mysqldump")

    _apply_retention()
    return _describe(target)


def backup_path(filename: str) -> Path:
    """Resolve a stored backup filename to its on-disk path. `filename` always
    comes from the API, but is validated against the server-generated naming
    pattern regardless, to rule out any path traversal."""
    if not _FILENAME_RE.fullmatch(filename):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sauvegarde introuvable")
    path = backup_root() / filename
    if not path.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sauvegarde introuvable")
    return path


def delete_backup(filename: str) -> None:
    backup_path(filename).unlink()
