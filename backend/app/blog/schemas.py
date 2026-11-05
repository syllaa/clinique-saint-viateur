from datetime import datetime

from pydantic import BaseModel


class BlogCategoryCreate(BaseModel):
    name: str
    position: int = 0


class BlogCategoryUpdate(BaseModel):
    name: str | None = None
    position: int | None = None
    is_active: bool | None = None


class BlogCategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    position: int

    model_config = {"from_attributes": True}


class ArticleFaqCreate(BaseModel):
    question: str
    answer: str
    position: int = 0


class ArticleFaqUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    position: int | None = None


class ArticleFaqOut(BaseModel):
    id: int
    question: str
    answer: str
    position: int

    model_config = {"from_attributes": True}


class ArticleCreate(BaseModel):
    title: str
    excerpt: str
    content: str = ""
    category_id: int
    author: str = "Clinique Saint Viateur"
    cover_image_url: str | None = None
    icon: str = "📋"
    status: str = "published"
    practical_info: str | None = None
    included_items: str | None = None
    benefits: str | None = None
    secondary_image_url: str | None = None
    secondary_image_alt: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class ArticleUpdate(BaseModel):
    title: str | None = None
    excerpt: str | None = None
    content: str | None = None
    category_id: int | None = None
    author: str | None = None
    cover_image_url: str | None = None
    icon: str | None = None
    status: str | None = None
    practical_info: str | None = None
    included_items: str | None = None
    benefits: str | None = None
    secondary_image_url: str | None = None
    secondary_image_alt: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class ArticleListOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    category: BlogCategoryOut
    author: str
    cover_image_url: str | None
    icon: str
    status: str
    published_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ArticleOut(ArticleListOut):
    content: str
    practical_info: str | None
    included_items: str | None
    benefits: str | None
    secondary_image_url: str | None
    secondary_image_alt: str | None
    seo_title: str | None
    seo_description: str | None
    faqs: list[ArticleFaqOut] = []


class ArticlePageOut(BaseModel):
    items: list[ArticleListOut]
    total: int
    page: int
    page_size: int
