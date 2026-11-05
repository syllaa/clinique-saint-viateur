"""blog categories + article extension (slug, category_id, author, seo, cover image)

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-24

"""
import re
import unicodedata
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The categories the article editor UI has always offered. Anything else found on
# existing rows (drifted data) is appended below so no article ever loses its category.
_DEFAULT_CATEGORIES = ["Actualité", "Santé", "Événement", "Prévention", "Services", "Communiqué"]


def _slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "item"


def upgrade() -> None:
    op.create_table(
        "blog_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_unique_constraint("uq_blog_categories_name", "blog_categories", ["name"])
    op.create_unique_constraint("uq_blog_categories_slug", "blog_categories", ["slug"])
    op.create_index("ix_blog_categories_slug", "blog_categories", ["slug"])

    bind = op.get_bind()
    blog_categories = sa.table(
        "blog_categories",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
        sa.column("position", sa.Integer),
    )

    existing_values = {
        row[0]
        for row in bind.execute(sa.text("SELECT DISTINCT category FROM articles")).fetchall()
        if row[0]
    }
    all_names = list(dict.fromkeys(_DEFAULT_CATEGORIES + sorted(existing_values)))

    used_slugs: set[str] = set()
    name_to_id: dict[str, int] = {}
    for position, name in enumerate(all_names):
        base = _slugify(name)
        slug = base
        n = 2
        while slug in used_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_slugs.add(slug)
        result = bind.execute(blog_categories.insert().values(name=name, slug=slug, position=position))
        name_to_id[name] = result.lastrowid

    op.add_column("articles", sa.Column("category_id", sa.Integer(), nullable=True))
    op.add_column("articles", sa.Column("slug", sa.String(220), nullable=True))
    op.add_column(
        "articles",
        sa.Column("author", sa.String(120), nullable=False, server_default="Clinique Saint Viateur"),
    )
    op.add_column("articles", sa.Column("cover_image_url", sa.String(255), nullable=True))
    op.add_column("articles", sa.Column("seo_title", sa.String(200), nullable=True))
    op.add_column("articles", sa.Column("seo_description", sa.String(320), nullable=True))
    op.add_column("articles", sa.Column("published_at", sa.DateTime(), nullable=True))

    articles = sa.table(
        "articles",
        sa.column("id", sa.Integer),
        sa.column("title", sa.String),
        sa.column("slug", sa.String),
        sa.column("category", sa.String),
        sa.column("category_id", sa.Integer),
        sa.column("status", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("published_at", sa.DateTime),
    )
    rows = bind.execute(
        sa.select(articles.c.id, articles.c.title, articles.c.category, articles.c.status, articles.c.created_at)
    ).fetchall()
    used_article_slugs: set[str] = set()
    default_category_id = name_to_id[_DEFAULT_CATEGORIES[0]]
    for row in rows:
        base = _slugify(row.title)
        slug = base
        n = 2
        while slug in used_article_slugs:
            slug = f"{base}-{n}"
            n += 1
        used_article_slugs.add(slug)
        category_id = name_to_id.get(row.category, default_category_id)
        values = {"slug": slug, "category_id": category_id}
        if row.status == "published":
            values["published_at"] = row.created_at
        bind.execute(articles.update().where(articles.c.id == row.id).values(**values))

    op.alter_column("articles", "category_id", existing_type=sa.Integer(), nullable=False)
    op.alter_column("articles", "slug", existing_type=sa.String(220), nullable=False)
    op.create_foreign_key("fk_articles_category_id", "articles", "blog_categories", ["category_id"], ["id"])
    op.create_unique_constraint("uq_articles_slug", "articles", ["slug"])
    op.create_index("ix_articles_slug", "articles", ["slug"])
    op.drop_column("articles", "category")


def downgrade() -> None:
    op.add_column("articles", sa.Column("category", sa.String(60), nullable=True))
    bind = op.get_bind()
    bind.execute(sa.text("UPDATE articles a JOIN blog_categories c ON a.category_id = c.id SET a.category = c.name"))
    op.alter_column(
        "articles", "category", existing_type=sa.String(60), nullable=False, server_default="Actualité"
    )

    op.drop_index("ix_articles_slug", table_name="articles")
    op.drop_constraint("uq_articles_slug", "articles", type_="unique")
    op.drop_constraint("fk_articles_category_id", "articles", type_="foreignkey")
    op.drop_column("articles", "published_at")
    op.drop_column("articles", "seo_description")
    op.drop_column("articles", "seo_title")
    op.drop_column("articles", "cover_image_url")
    op.drop_column("articles", "author")
    op.drop_column("articles", "category_id")
    op.drop_column("articles", "slug")

    op.drop_index("ix_blog_categories_slug", table_name="blog_categories")
    op.drop_constraint("uq_blog_categories_slug", "blog_categories", type_="unique")
    op.drop_constraint("uq_blog_categories_name", "blog_categories", type_="unique")
    op.drop_table("blog_categories")
