from app.db.dependencies import get_db
from app.integrations.jobs.lever import LeverSource
from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_service import JobIngestionService


def main():
    db = next(get_db())

    try:
        repository = JobRepository(db)
        service = JobIngestionService(repository)

        source = LeverSource(
            company="leverdemo",
        )

        count = service.ingest(source)

        print(f"Ingested {count} Lever jobs")

    finally:
        db.close()


if __name__ == "__main__":
    main()