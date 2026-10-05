from datetime import datetime
from html import unescape
import requests
from bs4 import BeautifulSoup
from app.schemas.job_ingestion import NormalizedJob


class GreenhouseSource:
    source_name = "greenhouse"
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    def __init__(self, board_token: str, company: str):
        self.board_token = board_token
        self.company = company

    def fetch_jobs(self) -> list[dict]:
        url = f"{self.BASE_URL}/{self.board_token}/jobs"

        response = requests.get(
            url,
            params={"content": "true"},
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    def normalize_job(self, job: dict) -> NormalizedJob:
        return NormalizedJob(
            source="greenhouse",
            external_id=str(job["id"]),
            title=job["title"],
            company=self.company,
            description=self._clean_description(
                job.get("content")
                ),
            location=(
                job.get("location", {}).get("name")
                if job.get("location")
                else None
            ),
            job_url=job.get("absolute_url"),
            application_url=job["absolute_url"],
            source_updated_at=self._parse_datetime(
                job.get("updated_at")
            ),
        )

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
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
        ]
    
    @staticmethod
    def _clean_description(html: str | None) -> str:
        if not html:
            return ""

        decoded_html = html

        for _ in range(2):
            decoded_html = unescape(decoded_html)

        soup = BeautifulSoup(decoded_html, "html.parser")

        return soup.get_text(
            separator="\n",
            strip=True,
        )