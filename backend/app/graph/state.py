from typing import TypedDict
from app.db.models.analysis_status import AnalysisStatus
from app.schemas.ai.resume_analysis import ResumeAnalysis
from app.db.models.resume_analysis import ResumeAnalysis as ResumeAnalysisModel

class ResumeAnalysisState(TypedDict, total = False):
    resume_id: int
    file_path: str
    resume_text: str
    analysis: ResumeAnalysis
    saved_analysis: ResumeAnalysisModel

    status: AnalysisStatus
    error: str