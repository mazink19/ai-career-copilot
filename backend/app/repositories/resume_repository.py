from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.resume import Resume


class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_id(self, resume_id: int) -> Resume | None:
        statement = (
            select(Resume)
            .where(Resume.id == resume_id)
        )

        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def get_by_user_id(self, user_id: int) -> Resume | None:
        statement = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
        )

        result = self.db.execute(statement)
        return result.scalars().first()

    def get_by_user(self, user_id: int) -> list[Resume]:
        statement = (
            select(Resume)
            .where(Resume.user_id == user_id)
        )

        result = self.db.execute(statement)
        return result.scalars().all()

    def delete(self, resume: Resume) -> None:
        self.db.delete(resume)
        self.db.commit()