from app.ai.analyzers.resume_analyzer import ResumeAnalyzer
from app.ai.extraction.pdf_extractior import PDFExtractor

from app.db.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository
from app.db.models.analysis_status import AnalysisStatus

def make_extract_resume_node(extractor: PDFExtractor):

    def extract_resume(state):

        resume_text = extractor.extract(state["file_path"])

        return {
            "resume_text": resume_text
        }

    return extract_resume


def make_analyze_resume_node(analyzer: ResumeAnalyzer,):

    def analyze_resume(state):

        try:
            analysis = analyzer.analyze(
                state["resume_text"]
            )

            return {
                "analysis": analysis,
                "status": AnalysisStatus.COMPLETED,
            }

        except Exception as e:

            return {
                "status": AnalysisStatus.FAILED,
                "error": str(e),
            }

    return analyze_resume

def route_after_analysis(state):

    if state["status"] == AnalysisStatus.COMPLETED:
        return "success"

    return "failure"


def make_save_analysis_node(
    repository: ResumeAnalysisRepository,
):

    def save_analysis(state):

        analysis = state["analysis"]
        saved_analysis = repository.get_by_resume_id(
            state["resume_id"]
        )

        saved_analysis.summary = analysis.summary
        saved_analysis.skills = analysis.skills
        saved_analysis.experience = analysis.experience
        saved_analysis.education = analysis.education
        saved_analysis.projects = analysis.projects
        saved_analysis.status = AnalysisStatus.COMPLETED

        saved_analysis = repository.update(saved_analysis)
        return {
            "analysis": analysis,
            "saved_analysis": saved_analysis,
            "status": AnalysisStatus.COMPLETED
        }

    return save_analysis


def make_create_analysis_node(repository: ResumeAnalysisRepository):
    def create_analysis(state):

        resume_analysis = ResumeAnalysis(
            resume_id=state["resume_id"],
            status=AnalysisStatus.PENDING,
        )

        saved_analysis = repository.create(resume_analysis)

        return {
            "saved_analysis": saved_analysis,
            "status": AnalysisStatus.PENDING,
        }

    return create_analysis


def make_mark_analyzing_node(
    repository: ResumeAnalysisRepository,):
    def mark_analyzing(state):

        analysis = repository.get_by_resume_id(state["resume_id"])
        analysis.status = AnalysisStatus.ANALYZING
        repository.update(analysis)

        return {
            "saved_analysis": analysis,
            "status": AnalysisStatus.ANALYZING
            
        }
    return mark_analyzing


def make_handle_failure_node(
    repository: ResumeAnalysisRepository,
):
    
    def handle_failure(state):

        analysis = repository.get_by_resume_id(
            state["resume_id"]
        )

        if analysis is not None:
            analysis.status = AnalysisStatus.FAILED
            saved_analysis = repository.update(analysis)

            return {
                "saved_analysis": saved_analysis,
                "status": AnalysisStatus.FAILED,
            }

        return {
            "status": AnalysisStatus.FAILED,
            "error": "Resume analysis record not found",
        }

    return handle_failure
