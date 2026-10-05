from app.db.models.jobs import Job
from app.repositories.job_repository import JobRepository


def test_job_repository(db):

    repository = JobRepository(db)

    job = Job(
        source="manual",
        external_id="test-job-123",
        title="AI Engineer",
        company="Example Corp",
        description="Build AI applications",
        application_url="https://example.com/jobs/123",
    )

    saved_job = repository.create(job)

    assert saved_job.id is not None

    found_job = repository.get_by_id(saved_job.id)

    assert found_job is not None
    assert found_job.title == "AI Engineer"
    assert found_job.company == "Example Corp"
    assert found_job.application_url == "https://example.com/jobs/123"