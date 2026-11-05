from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_admin
from app.database import get_db
from app.support import crud, service
from app.support.schemas import TicketCreate, TicketOut, TicketUpdate

router = APIRouter(prefix="/api/support", tags=["support"], dependencies=[Depends(require_admin)])


@router.get("/tickets", response_model=list[TicketOut])
def list_tickets(status: str | None = None, db: Session = Depends(get_db)):
    return crud.list_tickets(db, status)


@router.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    return service.create_ticket(db, payload)


@router.patch("/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    return service.update_ticket(db, ticket_id, payload)


@router.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    service.delete_ticket(db, ticket_id)
