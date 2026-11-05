"""add urgency and hospitalization info fields to messages

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "messages",
        sa.Column("urgency", sa.String(20), nullable=False, server_default="urgence"),
    )
    op.add_column(
        "messages",
        sa.Column("wants_hospitalization_info", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("messages", "wants_hospitalization_info")
    op.drop_column("messages", "urgency")
