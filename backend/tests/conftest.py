import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.ai.extraction.pdf_extractior import PDFExtractor
from app.main import app
from app.db.base import Base
from app.db.dependencies import get_db
from app.dependencies.resume import get_resume_service
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.services.resume_analysis_service import ResumeAnalysisService
from app.services.resume_service import ResumeService

from tests.fakes.fake_resume_analyzer import FakeResumeAnalyzer


TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()


    def override_get_resume_service():
        db = TestingSessionLocal()

        try:
            analysis_repository = ResumeAnalysisRepository(db)
            analysis_service = ResumeAnalysisService(
            analysis_repository=analysis_repository,
            extractor=PDFExtractor(),
            analyzer=FakeResumeAnalyzer(),
        )

            yield ResumeService(
            db,
            analysis_service=analysis_service,)

        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_resume_service] = override_get_resume_service

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)