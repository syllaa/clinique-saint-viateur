from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.auth.dependencies import require_admin
from app.backups import service
from app.backups.schemas import BackupOut

router = APIRouter(prefix="/api/backups", tags=["backups"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[BackupOut])
def list_backups():
    return service.list_backups()


@router.post("", response_model=BackupOut, status_code=201)
def create_backup():
    try:
        return service.create_backup()
    except RuntimeError as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(e))


@router.get("/{filename}/download")
def download_backup(filename: str):
    path = service.backup_path(filename)
    return FileResponse(path, filename=filename, media_type="application/sql")


@router.delete("/{filename}", status_code=204)
def delete_backup(filename: str):
    service.delete_backup(filename)
