from app.core.exceptions import NotFoundException
from app.db.models.jobs import Job
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate
from app.services.job_service import JobService


def test_create_job(db):

    repository = JobRepository(db)
    service = JobService(repository)

    job = Job(
    source="manual",
    external_id="test-job-123",
    title="AI Engineer",
    company="Example Corp",
    description="Build AI applications",
    application_url="https://example.com/jobs/123",
)

    result = service.create_job(job)

    assert result.id is not None
    assert result.title == "AI Engineer"
    assert result.company == "Example Corp"
    assert str(result.application_url) == "https://example.com/jobs/123"


def test_get_job(db):

    repository = JobRepository(db)
    service = JobService(repository)

    data = JobCreate(
        title="Backend Engineer",
        company="Example Corp",
        description="Build APIs",
        application_url="https://example.com/jobs/456",
    )

    created = service.create_job(data)

    result = service.get_job(created.id)

    assert result.id == created.id
    assert result.title == "Backend Engineer"


def test_get_job_not_found(db):

    repository = JobRepository(db)
    service = JobService(repository)

    try:
        service.get_job(999999)
        assert False
    except NotFoundException:
        assert True


def test_get_jobs(db):

    repository = JobRepository(db)
    service = JobService(repository)

    service.create_job(
        JobCreate(
            title="AI Engineer",
            company="Company A",
            description="AI work",
            application_url="https://example.com/ai",
        )
    )

    service.create_job(
        JobCreate(
            title="Backend Engineer",
            company="Company B",
            description="Backend work",
            application_url="https://example.com/backend",
        )
    )

    results = service.get_jobs()

    assert len(results) == 2
    assert results[0].title == "AI Engineer"
    assert results[1].title == "Backend Engineer"