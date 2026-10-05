from datetime import datetime

from pydantic import BaseModel, HttpUrl


class NormalizedJob(BaseModel):
    source: str
    external_id: str

    title: str
    company: str
    description: str

    location: str | None = None
    workplace_type: str | None = None
    employment_type: str | None = None

    job_url: HttpUrl | None = None
    application_url: HttpUrl

    published_at: datetime | None = None
    source_updated_at: datetime | None = None



class IngestionSourceResult(BaseModel):
    source: str
    company: str
    processed: int = 0
    success: bool
    error: str | None = None


class IngestionReport(BaseModel):
    total_processed: int = 0
    sources: list[IngestionSourceResult]    