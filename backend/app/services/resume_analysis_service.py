from app.ai.analyzers.resume_analyzer import ResumeAnalyzer
from app.ai.extraction.pdf_extractior import PDFExtractor
from app.ai.resume_analysis_response import ResumeAnalysisResponse
from app.core.exceptions import NotFoundException
from app.db.models.resume_analysis import ResumeAnalysis
from app.graph.workflow import build_resume_analysis_graph
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository


class ResumeAnalysisService:

    def __init__(
        self,
        analysis_repository: ResumeAnalysisRepository,
        extractor: PDFExtractor,
        analyzer: ResumeAnalyzer,
    ):
        self.repository = analysis_repository

        self.graph = build_resume_analysis_graph(
            extractor=extractor,
            analyzer=analyzer,
            analysis_repository=analysis_repository,
        )

    def analyze_resume(self,file_path: str,resume_id: int,) -> ResumeAnalysis:

        result = self.graph.invoke({
            "resume_id": resume_id,
            "file_path": file_path,
        })

        return result["saved_analysis"]

    def get_resume_analysis(self,resume_id: int,) -> ResumeAnalysisResponse:

        analysis = self.repository.get_by_resume_id(resume_id)

        if analysis is None:
            raise NotFoundException("Resume analysis not found")

        return ResumeAnalysisResponse.model_validate(analysis)