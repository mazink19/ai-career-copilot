from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.resume_analysis import ResumeAnalysis

class ResumeAnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, analysis: ResumeAnalysis) -> ResumeAnalysis:
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def update(self, analysis: ResumeAnalysis) -> ResumeAnalysis:
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_by_resume_id(self,resume_id: int,) -> ResumeAnalysis | None:

        statement = (
            select(ResumeAnalysis)
            .where(ResumeAnalysis.resume_id == resume_id)
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()