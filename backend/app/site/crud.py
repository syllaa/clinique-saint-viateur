from sqlalchemy.orm import Session

from app.models.message import Message
from app.site.schemas import MessageCreate

# ── Messages ──────────────────────────────────────────────


def list_messages(db: Session) -> list[Message]:
    return db.query(Message).order_by(Message.created_at.desc()).all()


def get_message(db: Session, message_id: int) -> Message | None:
    return db.get(Message, message_id)


def create_message(db: Session, data: MessageCreate) -> Message:
    message = Message(**data.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def mark_message_read(db: Session, message: Message) -> Message:
    message.status = "read"
    db.commit()
    db.refresh(message)
    return message


def mark_all_messages_read(db: Session) -> None:
    db.query(Message).filter(Message.status == "new").update({"status": "read"})
    db.commit()


def delete_message(db: Session, message: Message) -> None:
    db.delete(message)
    db.commit()
