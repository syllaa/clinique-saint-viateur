from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.site import crud
from app.site.schemas import MessageCreate

# ── Messages ──────────────────────────────────────────────

VALID_URGENCY = {"urgence", "programme"}


def create_message(db: Session, data: MessageCreate):
    if data.website:  # honeypot filled in: automated submission
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Requête invalide")
    if not data.name.strip() or not data.content.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Nom et message sont requis")
    if data.urgency not in VALID_URGENCY:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Type de demande invalide")
    return crud.create_message(db, data)


def get_message_or_404(db: Session, message_id: int):
    message = crud.get_message(db, message_id)
    if not message:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Message introuvable")
    return message


def unread_count(db: Session) -> int:
    return sum(1 for m in crud.list_messages(db) if m.status == "new")
