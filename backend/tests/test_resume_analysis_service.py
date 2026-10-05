from app.ai.extraction.pdf_extractior import PDFExtractor
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.services.resume_analysis_service import ResumeAnalysisService
from tests.fakes.fake_resume_analyzer import FakeResumeAnalyzer

from fastapi.testclient import TestClient


def test_resume_analysis_service(db):
    repository = ResumeAnalysisRepository(db)

    service = ResumeAnalysisService(
        analysis_repository=repository,
        extractor=PDFExtractor(),
        analyzer=FakeResumeAnalyzer(),
    )

    result = service.analyze_resume(
        file_path="tests/files/test_resume.pdf",
        resume_id=1,
    )

    assert result.resume_id == 1
    assert result.summary == "Test resume summary"
    assert result.skills == ["Python", "FastAPI"]
    assert result.experience == ["Backend Engineer"]
    assert result.education == ["Computer Science"]
    assert result.projects == ["AI Career Copilot"]