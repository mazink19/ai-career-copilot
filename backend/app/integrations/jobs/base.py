from typing import Protocol

from app.schemas.job_ingestion import NormalizedJob


class JobSource(Protocol):
    source_name: str

    def fetch_normalized_jobs(self) -> list[NormalizedJob]:
        ...