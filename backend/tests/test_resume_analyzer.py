import pytest

from app.ai.analyzers.resume_analyzer import ResumeAnalyzer
from app.ai.extraction.pdf_extractior import PDFExtractor
from app.db.models.analysis_status import AnalysisStatus
from app.db.models.resume import Resume
from app.db.models.user import User
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.schemas.ai.resume_analysis import ResumeAnalysis
from app.services.resume_analysis_service import ResumeAnalysisService
from tests.fakes.failing_resume_analyzer import FailingResumeAnalyzer


def test_resume_analyzer():

    analyzer = ResumeAnalyzer()

    resume_text = """
    John Doe

    Python Backend Developer

    Skills:
    Python, FastAPI, PostgreSQL, Docker, LangChain

    Education:
    BSc Computer Science

    Experience:
    Backend Developer Intern at ABC Company.
    Worked on REST APIs using FastAPI and PostgreSQL.

    Projects:
    Built an AI Career Copilot using FastAPI and LangChain.
    """

    result = analyzer.analyze(resume_text)

    print("\n", result)

    assert isinstance(result, ResumeAnalysis)
    assert result.summary
    assert len(result.skills) > 0

def test_resume_analysis_failure(db):

    user = User(
        first_name="Test",
        last_name="User",
        email="failure@example.com",
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

    repository = ResumeAnalysisRepository(db)

    service = ResumeAnalysisService(
        analysis_repository=repository,
        extractor=PDFExtractor(),
        analyzer=FailingResumeAnalyzer(),
    )

    service.analyze_resume(
    file_path="tests/files/test_resume.pdf",
    resume_id=resume.id,
)

    analysis = repository.get_by_resume_id(resume.id)

    assert analysis is not None
    assert analysis.status == AnalysisStatus.FAILED