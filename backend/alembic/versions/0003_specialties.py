"""rename services to specialties, add detail-page fields, doctors, faqs

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-24

"""
import re
import unicodedata
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "item"


def upgrade() -> None:
    op.rename_table("services", "specialties")

    # Nullable / no server_default on TEXT columns for the ADD COLUMN step (MySQL
    # versions vary in support for TEXT/BLOB defaults on ALTER TABLE) — backfilled
    # via UPDATE below, then tightened to NOT NULL.
    op.add_column("specialties", sa.Column("slug", sa.String(160), nullable=True))
    op.add_column("specialties", sa.Column("cover_image_url", sa.String(255), nullable=True))
    op.add_column("specialties", sa.Column("full_description", sa.Text(), nullable=True))
    op.add_column("specialties", sa.Column("services_offered", sa.Text(), nullable=True))
    op.add_column("specialties", sa.Column("symptoms_text", sa.Text(), nullable=True))
    op.add_column("specialties", sa.Column("consultation_hours", sa.String(200), nullable=True))
    op.add_column("specialties", sa.Column("practical_info", sa.Text(), nullable=True))
    op.add_column("specialties", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("specialties", sa.Column("seo_title", sa.String(200), nullable=True))
    op.add_column("specialties", sa.Column("seo_description", sa.String(320), nullable=True))
    op.add_column("specialties", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("specialties", sa.Column("updated_at", sa.DateTime(), nullable=True))

    bind = op.get_bind()
    specialties = sa.table(
        "specialties",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
        sa.column("full_description", sa.Text),
        sa.column("services_offered", sa.Text),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )
    now = sa.func.now()
    rows = bind.execute(sa.select(specialties.c.id, specialties.c.name)).fetchall()
    used_slugs: set[str] = set()
    for row in rows:
        base = _slugify(row.name)
        slug = base
        n = 2
        while slug in used_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_slugs.add(slug)
        bind.execute(
            specialties.update()
            .where(specialties.c.id == row.id)
            .values(slug=slug, full_description="", services_offered="", created_at=now, updated_at=now)
        )

    op.alter_column("specialties", "slug", existing_type=sa.String(160), nullable=False)
    op.alter_column("specialties", "full_description", existing_type=sa.Text(), nullable=False)
    op.alter_column("specialties", "services_offered", existing_type=sa.Text(), nullable=False)
    op.alter_column("specialties", "created_at", existing_type=sa.DateTime(), nullable=False)
    op.alter_column("specialties", "updated_at", existing_type=sa.DateTime(), nullable=False)
    op.create_unique_constraint("uq_specialties_slug", "specialties", ["slug"])
    op.create_index("ix_specialties_slug", "specialties", ["slug"])

    op.create_table(
        "specialty_doctors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "specialty_id",
            sa.Integer(),
            sa.ForeignKey("specialties.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("title", sa.String(150), nullable=True),
        sa.Column("photo_url", sa.String(255), nullable=True),
        sa.Column("bio", sa.String(400), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_specialty_doctors_specialty_id", "specialty_doctors", ["specialty_id"])

    op.create_table(
        "specialty_faqs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "specialty_id",
            sa.Integer(),
            sa.ForeignKey("specialties.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("question", sa.String(300), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_specialty_faqs_specialty_id", "specialty_faqs", ["specialty_id"])


def downgrade() -> None:
    op.drop_index("ix_specialty_faqs_specialty_id", table_name="specialty_faqs")
    op.drop_table("specialty_faqs")
    op.drop_index("ix_specialty_doctors_specialty_id", table_name="specialty_doctors")
    op.drop_table("specialty_doctors")

    op.drop_index("ix_specialties_slug", table_name="specialties")
    op.drop_constraint("uq_specialties_slug", "specialties", type_="unique")
    for col in [
        "updated_at",
        "created_at",
        "seo_description",
        "seo_title",
        "practical_info",
        "consultation_hours",
        "symptoms_text",
        "services_offered",
        "full_description",
        "cover_image_url",
        "slug",
    ]:
        op.drop_column("specialties", col)

    op.rename_table("specialties", "services")
