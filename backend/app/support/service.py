from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.support import crud
from app.support.schemas import TicketCreate, TicketUpdate

VALID_STATUSES = {"open", "in_progress", "closed"}
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}


def create_ticket(db: Session, data: TicketCreate):
    if data.priority not in VALID_PRIORITIES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Priorité invalide")
    return crud.create_ticket(db, data)


def update_ticket(db: Session, ticket_id: int, data: TicketUpdate):
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket introuvable")
    if data.status and data.status not in VALID_STATUSES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Statut invalide")
    if data.priority and data.priority not in VALID_PRIORITIES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Priorité invalide")
    return crud.update_ticket(db, ticket, data)


def delete_ticket(db: Session, ticket_id: int) -> None:
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Ticket introuvable")
    crud.delete_ticket(db, ticket)
