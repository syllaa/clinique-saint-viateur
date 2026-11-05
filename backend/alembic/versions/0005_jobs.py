"""job offers and job applications

Revision ID: 0005
Revises: 0004
Create Date: 2026-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_offers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(220), nullable=False),
        sa.Column("department", sa.String(120), nullable=True),
        sa.Column("contract_type", sa.String(30), nullable=False),
        sa.Column("location", sa.String(160), nullable=False, server_default="Cocody, Abidjan"),
        sa.Column("short_description", sa.String(400), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("missions", sa.Text(), nullable=True),
        sa.Column("profile_requirements", sa.Text(), nullable=True),
        sa.Column("skills", sa.Text(), nullable=True),
        sa.Column("experience_level", sa.String(60), nullable=True),
        sa.Column("status", sa.String(10), nullable=False, server_default="published"),
        sa.Column("application_deadline", sa.Date(), nullable=True),
        sa.Column("seo_title", sa.String(200), nullable=True),
        sa.Column("seo_description", sa.String(320), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint("uq_job_offers_slug", "job_offers", ["slug"])
    op.create_index("ix_job_offers_slug", "job_offers", ["slug"])

    op.create_table(
        "job_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "job_offer_id",
            sa.Integer(),
            sa.ForeignKey("job_offers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("first_name", sa.String(80), nullable=False),
        sa.Column("last_name", sa.String(80), nullable=False),
        sa.Column("email", sa.String(160), nullable=False),
        sa.Column("phone", sa.String(40), nullable=False),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column("cv_path", sa.String(255), nullable=False),
        sa.Column("consent_given_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="nouvelle"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_job_applications_job_offer_id", "job_applications", ["job_offer_id"])


def downgrade() -> None:
    op.drop_index("ix_job_applications_job_offer_id", table_name="job_applications")
    op.drop_table("job_applications")
    op.drop_index("ix_job_offers_slug", table_name="job_offers")
    op.drop_constraint("uq_job_offers_slug", "job_offers", type_="unique")
    op.drop_table("job_offers")
