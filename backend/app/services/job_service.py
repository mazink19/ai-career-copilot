from app.core.exceptions import NotFoundException
from app.db.models.jobs import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobResponse
from uuid import uuid4

class JobService:

    def __init__(self, repository: JobRepository):
        self.repository = repository

    def create_job(self, data: JobCreate) -> JobResponse:

        job = Job(
            source="manual",
            external_id=f"manual-{uuid4()}",
            title=data.title,
            company=data.company,
            description=data.description,
            application_url=str(data.application_url),
        )

        saved_job = self.repository.create(job)

        return JobResponse.model_validate(saved_job)

    def get_job(self, job_id: int) -> JobResponse:

        job = self.repository.get_by_id(job_id)

        if job is None:
            raise NotFoundException("Job not found")

        return JobResponse.model_validate(job)

    def get_jobs(self) -> list[JobResponse]:

        jobs = self.repository.get_all()

        return [
            JobResponse.model_validate(job)
            for job in jobs
        ]
    
    def get_application_url(self, job_id: int) -> str:

        job = self.repository.get_by_id(job_id)

        if job is None:
            raise NotFoundException("Job not found")

        return str(job.application_url)
    
    def search_jobs(
    self,
    search: str | None = None,
    company: str | None = None,
    location: str | None = None,
    workplace_type: str | None = None,
    employment_type: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[JobResponse], int]:

        jobs = self.repository.search(
            search=search,
            company=company,
            location=location,
            workplace_type=workplace_type,
            employment_type=employment_type,
            limit=limit,
            offset=offset,
        )

        total = self.repository.count(
            search=search,
            company=company,
            location=location,
            workplace_type=workplace_type,
            employment_type=employment_type,
        )

        return (
            [
                JobResponse.model_validate(job)
                for job in jobs
            ],
            total,
        )