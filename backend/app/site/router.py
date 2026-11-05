from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.rate_limit import rate_limit
from app.site import crud, service
from app.site.schemas import MessageCreate, MessageOut

router = APIRouter(prefix="/api", tags=["site"])

# ── Messages ──────────────────────────────────────────────
# Public: send a message. Admin-only: list / read / delete.


@router.post(
    "/messages",
    response_model=MessageOut,
    status_code=201,
    dependencies=[Depends(rate_limit("contact", 5, 600))],
)
def send_message(payload: MessageCreate, db: Session = Depends(get_db)):
    return service.create_message(db, payload)


@router.get("/messages", response_model=list[MessageOut], dependencies=[Depends(require_admin)])
def list_messages(db: Session = Depends(get_db)):
    return crud.list_messages(db)


@router.patch("/messages/{message_id}/read", response_model=MessageOut, dependencies=[Depends(require_admin)])
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    message = service.get_message_or_404(db, message_id)
    return crud.mark_message_read(db, message)


@router.post("/messages/mark-all-read", status_code=204, dependencies=[Depends(require_admin)])
def mark_all_messages_read(db: Session = Depends(get_db)):
    crud.mark_all_messages_read(db)


@router.delete("/messages/{message_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = service.get_message_or_404(db, message_id)
    crud.delete_message(db, message)
