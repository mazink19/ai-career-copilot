from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.resume_service import ResumeService
from app.services.resume_analysis_service import ResumeAnalysisService

from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.ai.extraction.pdf_extractior import PDFExtractor
from app.ai.analyzers.resume_analyzer import ResumeAnalyzer


def get_resume_analysis_service(
    db: Session = Depends(get_db),
) -> ResumeAnalysisService:

    repository = ResumeAnalysisRepository(db)

    return ResumeAnalysisService(
        analysis_repository=repository,
        extractor=PDFExtractor(),
        analyzer=ResumeAnalyzer(),
    )


def get_resume_service(
    db: Session = Depends(get_db),
    analysis_service: ResumeAnalysisService = Depends(
        get_resume_analysis_service
    ),
) -> ResumeService:

    return ResumeService(
        db=db,
        analysis_service=analysis_service,
    )