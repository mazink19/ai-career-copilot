from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.analysis_status import AnalysisStatus


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,unique=True,)
    
    status: Mapped[AnalysisStatus] = mapped_column(
        default=AnalysisStatus.PENDING,nullable=False,)

    summary: Mapped[str | None] = mapped_column(String,nullable=True,)

    skills: Mapped[list | None] = mapped_column(JSON,nullable=True,)

    experience: Mapped[list | None] = mapped_column(JSON,nullable=True,)

    education: Mapped[list | None] = mapped_column(JSON,nullable=True,)

    projects: Mapped[list | None] = mapped_column(JSON,nullable=True,)

    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,)

    resume = relationship("Resume",back_populates="analysis",)