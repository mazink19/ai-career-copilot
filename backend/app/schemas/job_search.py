from pydantic import BaseModel

from app.schemas.job import JobResponse


class JobSearchResponse(BaseModel):
    jobs: list[JobResponse]
    total: int
    limit: int
    offset: int