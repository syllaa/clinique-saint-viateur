"""specialty cover video

Adds an optional ambient video to each specialty (detail page header).
Nullable column, no default: existing rows are untouched.

Revision ID: 0009
Revises: 0008
Create Date: 2026-11-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("specialties", sa.Column("cover_video_url", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("specialties", "cover_video_url")
