from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    subject: str
    content: str
    urgency: str = "urgence"
    wants_hospitalization_info: bool = False
    # Honeypot: a field hidden from humans in the form. Bots fill it in.
    # Never stored (excluded from model_dump).
    website: str | None = Field(default=None, exclude=True)


class MessageOut(BaseModel):
    id: int
    name: str
    email: str | None
    phone: str | None
    subject: str
    content: str
    urgency: str
    wants_hospitalization_info: bool
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
