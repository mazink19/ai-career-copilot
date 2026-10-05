from typing import TypedDict

from app.schemas.ai.job_match_analysis import JobMatchAnalysis
from app.schemas.ai.resume_analysis import ResumeAnalysis


class JobMatchingState(TypedDict, total=False):

    resume: ResumeAnalysis
    job_description: str
    analysis: JobMatchAnalysis
    score: int
    recommendation: str