from app.graph.workflow import build_resume_analysis_graph

from app.db.models.resume import Resume
from app.db.models.user import User
from app.db.models.analysis_status import AnalysisStatus
from tests.fakes.fake_resume_analyzer import FakeResumeAnalyzer
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository

from app.ai.extraction.pdf_extractior import PDFExtractor

class FailingResumeAnalyzer:

    def analyze(self, resume_text: str):
        raise RuntimeError("AI analysis failed")


def test_resume_analysis_graph(db):

    user = User(
        first_name="Test",
        last_name="User",
        email="graph@example.com",
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
    extractor = PDFExtractor()
    analyzer = FakeResumeAnalyzer()
    graph = build_resume_analysis_graph(extractor=extractor,
    analyzer=analyzer,
    analysis_repository=repository,)

    result = graph.invoke({
        "resume_id": resume.id,
        "file_path": "tests/files/test_resume.pdf",
    })
    assert result["resume_id"] == resume.id
    assert result["resume_text"]
    assert result["analysis"]
    assert result["saved_analysis"]

    saved_analysis = repository.get_by_resume_id(resume.id)

    assert saved_analysis is not None
    assert saved_analysis.summary

def test_resume_analysis_graph_failure(db):

    user = User(
        first_name="Test",
        last_name="User",
        email="graph-failure@example.com",
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

    extractor = PDFExtractor()

    analyzer = FailingResumeAnalyzer()

    graph = build_resume_analysis_graph(
        extractor=extractor,
        analyzer=analyzer,
        analysis_repository=repository,
    )

    result = graph.invoke({
        "resume_id": resume.id,
        "file_path": "tests/files/test_resume.pdf",
    })

    assert result["status"] == AnalysisStatus.FAILED

    saved_analysis = repository.get_by_resume_id(resume.id)

    assert saved_analysis is not None
    assert saved_analysis.status == AnalysisStatus.FAILED