import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.dependencies.services import get_job_matching_service
from mcp.server import MCPServer
from app.db.dependencies import get_db
from app.repositories.job_repository import JobRepository
mcp = MCPServer("AI Career Copilot")



@mcp.tool()
def search_jobs(
    search: str | None = None,
    company: str | None = None,
    location: str | None = None,
    workplace_type: str | None = None,
    employment_type: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """
    Search available jobs using keywords and filters.
    """

    db = next(get_db())

    try:
        repository = JobRepository(db)

        jobs = repository.search(
            search=search,
            company=company,
            location=location,
            workplace_type=workplace_type,
            employment_type=employment_type,
            limit=min(limit, 50),
            offset=0,
        )

        return [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "workplace_type": job.workplace_type,
                "employment_type": job.employment_type,
                "application_url": job.application_url,
                "source": job.source,
            }
            for job in jobs
        ]

    finally:
        db.close()

@mcp.tool()
def get_job(job_id: int) -> dict:
    """
    Get complete details for a specific job.
    """

    db = next(get_db())

    try:
        repository = JobRepository(db)

        job = repository.get_by_id(job_id)

        if job is None:
            return {
                "error": f"Job {job_id} not found"
            }

        return {
            "id": job.id,
            "source": job.source,
            "external_id": job.external_id,
            "title": job.title,
            "company": job.company,
            "description": job.description,
            "location": job.location,
            "workplace_type": job.workplace_type,
            "employment_type": job.employment_type,
            "job_url": job.job_url,
            "application_url": job.application_url,
            "published_at": (
                job.published_at.isoformat()
                if job.published_at
                else None
            ),
        }

    finally:
        db.close()     

@mcp.tool()
def match_job_to_resume(
    job_id: int,
    user_id: int,
) -> dict:
    """
    Analyze how well a user's resume matches a specific job.
    """

    db = next(get_db())

    try:
        service = get_job_matching_service(db)

        analysis = service.match_job(
            user_id=user_id,
            job_id=job_id,
        )

        return analysis.model_dump()

    finally:
        db.close()
        db.close()



if __name__ == "__main__":
    mcp.run()