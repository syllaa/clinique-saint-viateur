from datetime import datetime

from pydantic import BaseModel


class TicketCreate(BaseModel):
    subject: str
    description: str
    priority: str = "normal"


class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None


class TicketOut(BaseModel):
    id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
