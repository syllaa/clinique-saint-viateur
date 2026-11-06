from datetime import datetime

from pydantic import BaseModel


class SpecialtyDoctorCreate(BaseModel):
    name: str
    title: str | None = None
    photo_url: str | None = None
    bio: str | None = None
    position: int = 0


class SpecialtyDoctorUpdate(BaseModel):
    name: str | None = None
    title: str | None = None
    photo_url: str | None = None
    bio: str | None = None
    position: int | None = None


class SpecialtyDoctorOut(BaseModel):
    id: int
    name: str
    title: str | None
    photo_url: str | None
    bio: str | None
    position: int

    model_config = {"from_attributes": True}


class SpecialtyFaqCreate(BaseModel):
    question: str
    answer: str
    position: int = 0


class SpecialtyFaqUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    position: int | None = None


class SpecialtyFaqOut(BaseModel):
    id: int
    question: str
    answer: str
    position: int

    model_config = {"from_attributes": True}


class SpecialtyCreate(BaseModel):
    name: str
    description: str = ""
    position: int = 0
    media_type: str = "icon"  # "icon" | "image"
    icon_name: str | None = None
    cover_image_url: str | None = None
    image_alt: str | None = None
    cover_video_url: str | None = None
    full_description: str = ""
    services_offered: str = ""
    symptoms_text: str | None = None
    consultation_hours: str | None = None
    practical_info: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class SpecialtyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    position: int | None = None
    media_type: str | None = None
    icon_name: str | None = None
    cover_image_url: str | None = None
    image_alt: str | None = None
    cover_video_url: str | None = None
    full_description: str | None = None
    services_offered: str | None = None
    symptoms_text: str | None = None
    consultation_hours: str | None = None
    practical_info: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class SpecialtyListOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str
    position: int
    is_active: bool
    media_type: str
    icon_name: str | None
    cover_image_url: str | None
    image_alt: str | None
    cover_video_url: str | None = None

    model_config = {"from_attributes": True}


class SpecialtyOut(SpecialtyListOut):
    full_description: str
    services_offered: str
    symptoms_text: str | None
    consultation_hours: str | None
    practical_info: str | None
    seo_title: str | None
    seo_description: str | None
    created_at: datetime
    updated_at: datetime
    doctors: list[SpecialtyDoctorOut] = []
    faqs: list[SpecialtyFaqOut] = []
