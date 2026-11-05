"""promotions and promotion reactions

Revision ID: 0007
Revises: 0006
Create Date: 2026-08-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "promotions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(220), nullable=False),
        sa.Column("short_description", sa.Text(), nullable=False, server_default=""),
        sa.Column("value_label", sa.String(120), nullable=False, server_default=""),
        sa.Column("category", sa.String(80), nullable=True),
        sa.Column("cover_image_url", sa.String(255), nullable=True),
        sa.Column("image_alt", sa.String(200), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint("uq_promotions_slug", "promotions", ["slug"])
    op.create_index("ix_promotions_slug", "promotions", ["slug"])

    op.create_table(
        "promotion_reactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "promotion_id",
            sa.Integer(),
            sa.ForeignKey("promotions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("reaction_type", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_promotion_reactions_promotion_id", "promotion_reactions", ["promotion_id"])
    op.create_index("ix_promotion_reactions_device_id", "promotion_reactions", ["device_id"])
    op.create_unique_constraint(
        "uq_promotion_reaction_device", "promotion_reactions", ["promotion_id", "device_id"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_promotion_reaction_device", "promotion_reactions", type_="unique")
    op.drop_index("ix_promotion_reactions_device_id", table_name="promotion_reactions")
    op.drop_index("ix_promotion_reactions_promotion_id", table_name="promotion_reactions")
    op.drop_table("promotion_reactions")
    op.drop_index("ix_promotions_slug", table_name="promotions")
    op.drop_constraint("uq_promotions_slug", "promotions", type_="unique")
    op.drop_table("promotions")
