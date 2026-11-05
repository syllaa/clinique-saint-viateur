"""MCP server exposing support-ticket administration tools.

Lets an MCP-compatible client (e.g. Claude Desktop) list, create and update
support tickets stored by the FastAPI backend, without going through HTTP.

Run as a plain script (not `python -m mcp.admin_ticket`, which would collide
with this very package's own name "mcp"):

    python backend/mcp/admin_ticket.py
"""

# Import the real "mcp" package BEFORE backend/ is added to sys.path below,
# otherwise this file's own parent directory (backend/mcp) would shadow it.
from mcp.server.fastmcp import FastMCP

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # backend/, for `app.*` imports

from app.database import SessionLocal  # noqa: E402
from app.support import crud  # noqa: E402
from app.support.schemas import TicketCreate, TicketUpdate  # noqa: E402
from app.support.service import VALID_PRIORITIES, VALID_STATUSES  # noqa: E402

mcp = FastMCP("clinique-saint-viateur-admin-ticket")


def _ticket_to_dict(ticket) -> dict:
    return {
        "id": ticket.id,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
    }


@mcp.tool()
def list_tickets(status: str | None = None) -> list[dict]:
    """List support tickets, optionally filtered by status (open, in_progress, closed)."""
    db = SessionLocal()
    try:
        return [_ticket_to_dict(t) for t in crud.list_tickets(db, status)]
    finally:
        db.close()


@mcp.tool()
def get_ticket(ticket_id: int) -> dict:
    """Get a single ticket by id."""
    db = SessionLocal()
    try:
        ticket = crud.get_ticket(db, ticket_id)
        if not ticket:
            return {"error": f"Ticket {ticket_id} introuvable"}
        return _ticket_to_dict(ticket)
    finally:
        db.close()


@mcp.tool()
def create_ticket(subject: str, description: str, priority: str = "normal") -> dict:
    """Create a new support ticket."""
    if priority not in VALID_PRIORITIES:
        return {"error": f"Priorité invalide, attendu l'une de {sorted(VALID_PRIORITIES)}"}
    db = SessionLocal()
    try:
        ticket = crud.create_ticket(db, TicketCreate(subject=subject, description=description, priority=priority))
        return _ticket_to_dict(ticket)
    finally:
        db.close()


@mcp.tool()
def update_ticket_status(ticket_id: int, status: str) -> dict:
    """Update a ticket's status (open, in_progress, closed)."""
    if status not in VALID_STATUSES:
        return {"error": f"Statut invalide, attendu l'un de {sorted(VALID_STATUSES)}"}
    db = SessionLocal()
    try:
        ticket = crud.get_ticket(db, ticket_id)
        if not ticket:
            return {"error": f"Ticket {ticket_id} introuvable"}
        ticket = crud.update_ticket(db, ticket, TicketUpdate(status=status))
        return _ticket_to_dict(ticket)
    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()
