from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class JobBase(BaseModel):
    title: str
    company: str
    description: str

    location: str | None = None
    workplace_type: str | None = None
    employment_type: str | None = None

    application_url: HttpUrl
    job_url: HttpUrl | None = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    source: str
    published_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class JobMatchResponse(BaseModel):
    job: JobResponse

    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    match_reason: str

    model_config = ConfigDict(from_attributes=True)