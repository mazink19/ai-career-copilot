from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.models.jobs import Job
from app.schemas.job_ingestion import NormalizedJob


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job: Job) -> Job:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_by_id(self, job_id: int) -> Job | None:
        statement = select(Job).where(Job.id == job_id)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def get_all(self) -> list[Job]:
        statement = select(Job)
        result = self.db.execute(statement)
        return result.scalars().all()

    def get_by_source_and_external_id(
        self,
        source: str,
        external_id: str,
    ) -> Job | None:
        statement = select(Job).where(
            Job.source == source,
            Job.external_id == external_id,
        )
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def upsert(self, data: NormalizedJob) -> Job:
        job = self.get_by_source_and_external_id(
            source=data.source,
            external_id=data.external_id,
        )

        if job is None:
            job = Job(
                source=data.source,
                external_id=data.external_id,
                title=data.title,
                company=data.company,
                description=data.description,
                location=data.location,
                workplace_type=data.workplace_type,
                employment_type=data.employment_type,
                job_url=str(data.job_url) if data.job_url else None,
                application_url=str(data.application_url),
                published_at=data.published_at,
                source_updated_at=data.source_updated_at,
                is_active=True,
            )
            self.db.add(job)
        else:
            job.title = data.title
            job.company = data.company
            job.description = data.description
            job.location = data.location
            job.workplace_type = data.workplace_type
            job.employment_type = data.employment_type
            job.job_url = str(data.job_url) if data.job_url else None
            job.application_url = str(data.application_url)
            job.published_at = data.published_at
            job.source_updated_at = data.source_updated_at
            job.is_active = True

        self.db.commit()
        self.db.refresh(job)

        return job

    def upsert_many(self, jobs: list[NormalizedJob]) -> int:
        if not jobs:
            return 0

        # Prevent duplicate (source, external_id) values
        # inside the same batch.
        unique_jobs: dict[tuple[str, str], NormalizedJob] = {}

        for job in jobs:
            unique_jobs[(job.source, job.external_id)] = job

        jobs = list(unique_jobs.values())

        rows = [
            {
                "source": job.source,
                "external_id": job.external_id,
                "title": job.title,
                "company": job.company,
                "description": job.description,
                "location": job.location,
                "workplace_type": job.workplace_type,
                "employment_type": job.employment_type,
                "job_url": str(job.job_url) if job.job_url else None,
                "application_url": str(job.application_url),
                "published_at": job.published_at,
                "source_updated_at": job.source_updated_at,
                "is_active": True,
            }
            for job in jobs
        ]

        statement = insert(Job).values(rows)

        statement = statement.on_conflict_do_update(
            index_elements=["source", "external_id"],
            set_={
                "title": statement.excluded.title,
                "company": statement.excluded.company,
                "description": statement.excluded.description,
                "location": statement.excluded.location,
                "workplace_type": statement.excluded.workplace_type,
                "employment_type": statement.excluded.employment_type,
                "job_url": statement.excluded.job_url,
                "application_url": statement.excluded.application_url,
                "published_at": statement.excluded.published_at,
                "source_updated_at": statement.excluded.source_updated_at,
                "is_active": True,
                "updated_at": func.now(),
            },
        )

        self.db.execute(statement)
        self.db.commit()

        return len(jobs)



    def search(
        self,
        search: str | None = None,
        company: str | None = None,
        location: str | None = None,
        workplace_type: str | None = None,
        employment_type: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Job]:
        statement = select(Job).where(Job.is_active.is_(True))

        if search:
            search_pattern = f"%{search}%"

            statement = statement.where(
                Job.title.ilike(search_pattern)
                | Job.description.ilike(search_pattern)
                | Job.company.ilike(search_pattern)
            )

        if company:
            statement = statement.where(
                Job.company.ilike(f"%{company}%")
            )

        if location:
            statement = statement.where(
                Job.location.ilike(f"%{location}%")
            )

        if workplace_type:
            statement = statement.where(
                Job.workplace_type == workplace_type
            )

        if employment_type:
            statement = statement.where(
                Job.employment_type == employment_type
            )

        statement = (
            statement
            .order_by(Job.published_at.desc().nullslast(), Job.id.desc())
            .limit(limit)
            .offset(offset)
        )

        result = self.db.execute(statement)

        return result.scalars().all()
    
    def count(
    self,
    search: str | None = None,
    company: str | None = None,
    location: str | None = None,
    workplace_type: str | None = None,
    employment_type: str | None = None,
) -> int:
        statement = select(func.count()).select_from(Job).where(
            Job.is_active.is_(True)
        )

        if search:
            search_pattern = f"%{search}%"

            statement = statement.where(
                Job.title.ilike(search_pattern)
                | Job.description.ilike(search_pattern)
                | Job.company.ilike(search_pattern)
            )

        if company:
            statement = statement.where(
                Job.company.ilike(f"%{company}%")
            )

        if location:
            statement = statement.where(
                Job.location.ilike(f"%{location}%")
            )

        if workplace_type:
            statement = statement.where(
                Job.workplace_type == workplace_type
            )

        if employment_type:
            statement = statement.where(
                Job.employment_type == employment_type
            )

        result = self.db.execute(statement)

        return result.scalar_one()
    def deactivate_missing_jobs(self, source: str,external_ids: set[str],) -> int:
        if not external_ids:
            return 0

        statement = (
            Job.__table__.update()
            .where(
                Job.source == source,
                Job.is_active.is_(True),
                ~Job.external_id.in_(external_ids),
            )
            .values(
                is_active=False,
                updated_at=func.now(),
            )
        )

        result = self.db.execute(statement)
        self.db.commit()

        return result.rowcount