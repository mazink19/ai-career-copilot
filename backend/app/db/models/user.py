from datetime import datetime
from app.db.base import Base

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.resume import Resume

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )