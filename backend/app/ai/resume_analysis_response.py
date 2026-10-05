from datetime import datetime

from pydantic import BaseModel

from app.db.models.analysis_status import AnalysisStatus


class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    summary: str | None = None
    status: AnalysisStatus
    skills: list[str] | None = None
    experience: list[str] | None = None
    education: list[str] | None = None
    projects: list[str] | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }