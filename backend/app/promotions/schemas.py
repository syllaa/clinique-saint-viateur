from datetime import date, datetime

from pydantic import BaseModel


class ReactionCounts(BaseModel):
    like: int = 0
    interested: int = 0
    hot: int = 0
    not_interested: int = 0


class PromotionCreate(BaseModel):
    title: str
    short_description: str = ""
    value_label: str = ""
    category: str | None = None
    cover_image_url: str | None = None
    image_alt: str | None = None
    valid_until: date
    is_published: bool = True
    position: int = 0


class PromotionUpdate(BaseModel):
    title: str | None = None
    short_description: str | None = None
    value_label: str | None = None
    category: str | None = None
    cover_image_url: str | None = None
    image_alt: str | None = None
    valid_until: date | None = None
    is_published: bool | None = None
    position: int | None = None


class PromotionListOut(BaseModel):
    id: int
    title: str
    slug: str
    short_description: str
    value_label: str
    category: str | None
    cover_image_url: str | None
    image_alt: str | None
    valid_until: date
    is_published: bool
    position: int
    created_at: datetime
    is_expired: bool
    reaction_counts: ReactionCounts
    my_reaction: str | None = None

    model_config = {"from_attributes": True}


class PromotionOut(PromotionListOut):
    updated_at: datetime


class PromotionPageOut(BaseModel):
    items: list[PromotionListOut]
    total: int
    page: int
    page_size: int


class ReactionIn(BaseModel):
    device_id: str
    reaction_type: str
