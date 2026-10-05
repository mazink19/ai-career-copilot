from app.db.models.resume_analysis import ResumeAnalysis as ResumeAnalysisModel
from app.schemas.ai.resume_analysis import ResumeAnalysis


def to_ai_schema(
    db_analysis: ResumeAnalysisModel,
) -> ResumeAnalysis:

    return ResumeAnalysis(
    summary=db_analysis.summary,
    skills=db_analysis.skills or [],
    experience=db_analysis.experience or [],
    education=db_analysis.education or [],
    projects=db_analysis.projects or [],
)