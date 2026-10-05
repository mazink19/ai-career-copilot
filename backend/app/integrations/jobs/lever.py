import requests

from app.schemas.job_ingestion import NormalizedJob


class LeverSource:
    source_name = "lever"
    BASE_URL = "https://api.lever.co/v0/postings"

    def __init__(self, company: str):
        self.company = company

    def fetch_jobs(self) -> list[dict]:
        url = f"{self.BASE_URL}/{self.company}"

        response = requests.get(
            url,
            params={
                "mode": "json",
                "limit": 100,
                "skip": 0,
            },
            headers={
                "Accept": "application/json",
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def normalize_job(self, job: dict) -> NormalizedJob:
        categories = job.get("categories") or {}

        return NormalizedJob(
            source="lever",
            external_id=str(job["id"]),
            title=job["text"],
            company=self.company,
            description=job.get("descriptionPlain") or "",
            location=categories.get("location"),
            workplace_type=self._normalize_workplace_type(
                job.get("workplaceType")
            ),
            employment_type=categories.get("commitment"),
            job_url=job.get("hostedUrl"),
            application_url=job["applyUrl"],
            published_at=None,
            source_updated_at=None,
        )

    @staticmethod
    def _normalize_workplace_type(
        value: str | None,
    ) -> str | None:
        if not value:
            return None

        return value.lower()

    def fetch_normalized_jobs(self) -> list[NormalizedJob]:
        jobs = self.fetch_jobs()

        return [
            self.normalize_job(job)
            for job in jobs
        ]