from datetime import date, datetime

from pydantic import BaseModel


class JobOfferCreate(BaseModel):
    title: str
    department: str | None = None
    contract_type: str
    location: str = "Cocody, Abidjan"
    short_description: str = ""
    description: str = ""
    missions: str | None = None
    profile_requirements: str | None = None
    skills: str | None = None
    experience_level: str | None = None
    status: str = "published"
    application_deadline: date | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class JobOfferUpdate(BaseModel):
    title: str | None = None
    department: str | None = None
    contract_type: str | None = None
    location: str | None = None
    short_description: str | None = None
    description: str | None = None
    missions: str | None = None
    profile_requirements: str | None = None
    skills: str | None = None
    experience_level: str | None = None
    status: str | None = None
    application_deadline: date | None = None
    seo_title: str | None = None
    seo_description: str | None = None


class JobOfferListOut(BaseModel):
    id: int
    title: str
    slug: str
    department: str | None
    contract_type: str
    location: str
    short_description: str
    status: str
    application_deadline: date | None
    created_at: datetime

    model_config = {"from_attributes": True}


class JobOfferOut(JobOfferListOut):
    description: str
    missions: str | None
    profile_requirements: str | None
    skills: str | None
    experience_level: str | None
    seo_title: str | None
    seo_description: str | None
    updated_at: datetime


class JobApplicationOut(BaseModel):
    id: int
    job_offer_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    cover_letter: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class JobApplicationStatusUpdate(BaseModel):
    status: str
