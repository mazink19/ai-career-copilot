from datetime import datetime

from pydantic import BaseModel

from app.db.models.analysis_status import AnalysisStatus


class ResumeResponse(BaseModel):
    id: int
    file_name: str
    uploaded_at: datetime
    analysis_status: AnalysisStatus | None = None