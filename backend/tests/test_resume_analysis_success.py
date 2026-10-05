from app.ai.extraction.pdf_extractior import PDFExtractor
from app.db.models.analysis_status import AnalysisStatus
from app.db.models.resume import Resume
from app.db.models.user import User
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.services.resume_analysis_service import ResumeAnalysisService
from tests.fakes.fake_resume_analyzer import FakeResumeAnalyzer


def test_resume_analysis_success(db):
    user = User(
        first_name="Test",
        last_name="User",
        email="success@example.com",
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
        analyzer=FakeResumeAnalyzer(),
    )

    service.analyze_resume(
        file_path="tests/files/test_resume.pdf",
        resume_id=resume.id,
    )

    analysis = repository.get_by_resume_id(resume.id)

    assert analysis is not None
    assert analysis.status == AnalysisStatus.COMPLETED
    assert analysis.summary == "Test resume summary"
    assert analysis.skills == ["Python", "FastAPI"]