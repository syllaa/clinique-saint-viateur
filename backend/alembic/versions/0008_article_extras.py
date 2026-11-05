"""article structured extras and article faqs

Revision ID: 0008
Revises: 0007
Create Date: 2026-08-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("articles", sa.Column("practical_info", sa.Text(), nullable=True))
    op.add_column("articles", sa.Column("included_items", sa.Text(), nullable=True))
    op.add_column("articles", sa.Column("benefits", sa.Text(), nullable=True))
    op.add_column("articles", sa.Column("secondary_image_url", sa.String(255), nullable=True))
    op.add_column("articles", sa.Column("secondary_image_alt", sa.String(200), nullable=True))

    op.create_table(
        "article_faqs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "article_id",
            sa.Integer(),
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question", sa.String(300), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_article_faqs_article_id", "article_faqs", ["article_id"])


def downgrade() -> None:
    op.drop_index("ix_article_faqs_article_id", table_name="article_faqs")
    op.drop_table("article_faqs")
    op.drop_column("articles", "secondary_image_alt")
    op.drop_column("articles", "secondary_image_url")
    op.drop_column("articles", "benefits")
    op.drop_column("articles", "included_items")
    op.drop_column("articles", "practical_info")
