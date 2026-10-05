from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.services.auth_service import AuthService
from app.services.resume_service import ResumeService
from app.services.job_matching_service import JobMatchingService
from app.services.job_service import JobService

from app.ai.analyzers.job_matcher import JobMatcher

from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.repositories.job_repository import JobRepository


def get_auth_service(db: Session = Depends(get_db),) -> AuthService:
    return AuthService(db)


def get_resume_service(
    db: Session = Depends(get_db),) -> ResumeService:

    return ResumeService(db)


def get_job_service(db: Session = Depends(get_db),) -> JobService:

    repository = JobRepository(db)

    return JobService(repository)

def get_job_matching_service(
    db: Session = Depends(get_db),
) -> JobMatchingService:

    return JobMatchingService(
        job_repository=JobRepository(db),
        resume_repository=ResumeRepository(db),
        analysis_repository=ResumeAnalysisRepository(db),
        matcher=JobMatcher(),
    )