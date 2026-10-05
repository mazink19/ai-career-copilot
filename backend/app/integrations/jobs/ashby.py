from datetime import datetime

import requests

from app.schemas.job_ingestion import NormalizedJob


class AshbySource:
    source_name = "ashby"
    BASE_URL = "https://api.ashbyhq.com/posting-api/job-board"

    def __init__(self, board_name: str, company: str):
        self.board_name = board_name
        self.company = company

    def fetch_jobs(self) -> list[dict]:
        url = f"{self.BASE_URL}/{self.board_name}"

        response = requests.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    def normalize_job(self, job: dict) -> NormalizedJob:
        return NormalizedJob(
            source="ashby",
            external_id=job["jobUrl"],
            title=job["title"],
            company=self.company,
            description=job.get("descriptionPlain") or "",
            location=job.get("location"),
            workplace_type=job.get("workplaceType"),
            employment_type=self._normalize_employment_type(
                job.get("employmentType")
            ),
            job_url=job.get("jobUrl"),
            application_url=job["applyUrl"],
            published_at=self._parse_datetime(
                job.get("publishedAt")
            ),
            source_updated_at=None,
        )

    @staticmethod
    def _normalize_employment_type(
        value: str | None,
    ) -> str | None:
        if not value:
            return None

        mapping = {
            "FullTime": "Full-time",
            "PartTime": "Part-time",
            "Intern": "Intern",
            "Contract": "Contract",
            "Temporary": "Temporary",
        }

        return mapping.get(value, value)

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        if not value:
            return None

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    def fetch_normalized_jobs(self) -> list[NormalizedJob]:
        jobs = self.fetch_jobs()

        return [
            self.normalize_job(job)
            for job in jobs
            if job.get("isListed", True)
        ]