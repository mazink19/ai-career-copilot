from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(String(255))

    file_path: Mapped[str] = mapped_column(String(500))

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship("User", back_populates="resumes")
    analysis = relationship(
    "ResumeAnalysis",
    back_populates="resume",
    uselist=False,
    cascade="all, delete-orphan")