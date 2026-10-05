from app.db.dependencies import get_db
from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_service import JobIngestionService
from app.integrations.jobs.greenhouse import GreenhouseSource

def main():
    db = next(get_db())

    try:
        repository = JobRepository(db)
        service = JobIngestionService(repository)
        source = GreenhouseSource(
            board_token="anthropic",
            company="Anthropic",
        )
        count = service.ingest(source)

        print(f"Ingested {count} jobs")

        jobs = repository.get_all()

        print(f"Total jobs in database: {len(jobs)}")

        for job in jobs[-3:]:
            print()
            print("DB ID:", job.id)
            print("Source:", job.source)
            print("External ID:", job.external_id)
            print("Title:", job.title)
            print("Company:", job.company)
            print("Location:", job.location)

    finally:
        db.close()


if __name__ == "__main__":
    main()