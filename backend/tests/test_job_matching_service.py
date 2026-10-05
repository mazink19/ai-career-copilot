from app.ai.analyzers.job_matcher import JobMatcher
from app.db.models.jobs import Job
from app.db.models.resume import Resume
from app.db.models.resume_analysis import ResumeAnalysis
from app.db.models.user import User
from app.repositories.job_repository import JobRepository
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.repositories.resume_repository import ResumeRepository
from app.schemas.ai.resume_analysis import ResumeAnalysis as ResumeAnalysisSchema
from app.services.job_matching_service import JobMatchingService


def test_job_matching_service(db):

    user = User(
        first_name="Test",
        last_name="User",
        email="matching@example.com",
        hashed_password="test-hash",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    resume = Resume(
        user_id=user.id,
        file_name="test_resume.pdf",
        file_path="tests/files/test_resume.pdf",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    job = Job(
        source="manual",
        external_id="test-job-123",
        title="AI Engineer",
        company="Example Corp",
        description="""
        We are looking for an AI Engineer with:
        Python, FastAPI, PostgreSQL, Docker and LangChain.
        """,
        application_url="https://example.com/jobs/123",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    analysis = ResumeAnalysis(
        resume_id=resume.id,
        summary="Python backend developer with AI experience",
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "LangChain",
        ],
        experience=["Backend Developer"],
        education=["BSc Computer Science"],
        projects=["AI Career Copilot"],
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    service = JobMatchingService(
        job_repository=JobRepository(db),
        resume_repository=ResumeRepository(db),
        analysis_repository=ResumeAnalysisRepository(db),
        matcher=JobMatcher(),
    )

    result = service.match_job(
        user_id=user.id,
        job_id=job.id,
    )

    assert result is not None
    assert 0 <= result.score <= 100
    assert result.matched_skills is not None
    assert result.missing_skills is not None
    assert result.strengths is not None
    assert result.recommendations is not None