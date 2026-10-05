from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_jobs_source_external_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # External source identity
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Job information
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Location / work arrangement
    location: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    workplace_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    employment_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # External URLs
    job_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    application_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    # Dates from external source
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    source_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Ingestion state
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    nullable=False,
)

    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
    nullable=False,
)