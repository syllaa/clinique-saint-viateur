"""specialty media (icon picker or custom image)

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Best-effort mapping from the known seeded specialty names to a curated Lucide icon
# slug, so existing rows get a sensible professional icon instead of a blank one.
# Anything not in this map (custom specialties an admin already added) falls back
# to "hospital" — always a valid, non-null default per requirement (§11.9).
_NAME_TO_ICON = {
    "Médecine Générale": "stethoscope",
    "Gynécologie & Maternité": "venus",
    "Chirurgie": "scissors",
    "Cardiologie": "heart-pulse",
    "Pédiatrie": "baby",
    "Laboratoire d'Analyses": "flask-conical",
    "Échographie & Imagerie": "scan",
    "Cabinet Dentaire": "smile",
    "Urgences & Réanimation": "ambulance",
}
_DEFAULT_ICON = "hospital"


def upgrade() -> None:
    op.alter_column("specialties", "icon", existing_type=sa.String(10), nullable=True)
    op.add_column(
        "specialties", sa.Column("media_type", sa.String(10), nullable=False, server_default="icon")
    )
    op.add_column("specialties", sa.Column("icon_name", sa.String(50), nullable=True))
    op.add_column("specialties", sa.Column("image_alt", sa.String(200), nullable=True))

    bind = op.get_bind()
    specialties = sa.table(
        "specialties",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("icon_name", sa.String),
        sa.column("media_type", sa.String),
        sa.column("cover_image_url", sa.String),
    )
    rows = bind.execute(sa.select(specialties.c.id, specialties.c.name, specialties.c.cover_image_url)).fetchall()
    for row in rows:
        # A specialty that already had a cover image (set via the Phase B admin
        # editor) keeps behaving as an image; everything else gets an icon.
        if row.cover_image_url:
            bind.execute(specialties.update().where(specialties.c.id == row.id).values(media_type="image"))
        else:
            icon_name = _NAME_TO_ICON.get(row.name, _DEFAULT_ICON)
            bind.execute(
                specialties.update().where(specialties.c.id == row.id).values(icon_name=icon_name, media_type="icon")
            )


def downgrade() -> None:
    op.drop_column("specialties", "image_alt")
    op.drop_column("specialties", "icon_name")
    op.drop_column("specialties", "media_type")
    op.execute("UPDATE specialties SET icon = '🏥' WHERE icon IS NULL")
    op.alter_column(
        "specialties", "icon", existing_type=sa.String(10), nullable=False, server_default="🏥"
    )
