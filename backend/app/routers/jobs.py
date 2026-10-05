from fastapi import APIRouter, Depends, status, Query

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.dependencies.services import (
    get_job_matching_service,
    get_job_service,
)
from app.schemas.job import JobCreate, JobResponse
from app.schemas.ai.job_match_analysis import JobMatchAnalysis
from app.schemas.job_search import JobSearchResponse

from app.services.job_service import JobService
from app.services.job_matching_service import JobMatchingService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,)

def create_job(
    data: JobCreate,
    service: JobService = Depends(get_job_service),):

    return service.create_job(data)


@router.get("", response_model=JobSearchResponse)
def get_jobs(
    search: str | None = Query(default=None),
    company: str | None = Query(default=None),
    location: str | None = Query(default=None),
    workplace_type: str | None = Query(default=None),
    employment_type: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: JobService = Depends(get_job_service),
):
    jobs, total = service.search_jobs(
    search=search,
    company=company,
    location=location,
    workplace_type=workplace_type,
    employment_type=employment_type,
    limit=limit,
    offset=offset,
)

    return JobSearchResponse(
        jobs=jobs,
        total=total,
        limit=limit,
        offset=offset,
    )

@router.get("/{job_id}",response_model=JobResponse,)

def get_job(
    job_id: int,
    service: JobService = Depends(get_job_service),):
    return service.get_job(job_id)


@router.get( "/{job_id}/apply",)

def apply_to_job(job_id: int,
    service: JobService = Depends(get_job_service),):

    return {
        "application_url": service.get_application_url(job_id)
    }


@router.post(
    "/{job_id}/match",
    response_model=JobMatchAnalysis,)

def match_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobMatchingService = Depends(get_job_matching_service),):

    return service.match_job(
        user_id=current_user.id,
        job_id=job_id,
    )


