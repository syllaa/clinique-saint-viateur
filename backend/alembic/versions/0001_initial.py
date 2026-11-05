"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(80), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="admin"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(120), nullable=True),
        sa.Column("phone", sa.String(40), nullable=True),
        sa.Column("subject", sa.String(160), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(10), nullable=False, server_default="new"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("excerpt", sa.String(400), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("category", sa.String(60), nullable=False, server_default="Actualité"),
        sa.Column("icon", sa.String(10), nullable=False, server_default="📋"),
        sa.Column("status", sa.String(10), nullable=False, server_default="published"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("icon", sa.String(10), nullable=False, server_default="🏥"),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("description", sa.String(400), nullable=False, server_default=""),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("services")
    op.drop_table("articles")
    op.drop_table("messages")
    op.drop_table("tickets")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
