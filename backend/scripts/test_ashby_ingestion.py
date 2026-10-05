from app.db.dependencies import get_db
from app.integrations.jobs.ashby import AshbySource
from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_service import JobIngestionService


def main():
    db = next(get_db())

    try:
        repository = JobRepository(db)
        service = JobIngestionService(repository)

        source = AshbySource(
            board_name="ashby",
            company="Ashby",
        )

        count = service.ingest(source)

        print(f"Ingested {count} Ashby jobs")

        jobs = repository.get_all()

        print(f"Total jobs in database: {len(jobs)}")

        ashby_jobs = [
            job
            for job in jobs
            if job.source == "ashby"
        ]

        print(f"Ashby jobs in database: {len(ashby_jobs)}")

        for job in ashby_jobs[:3]:
            print()
            print("DB ID:", job.id)
            print("Source:", job.source)
            print("External ID:", job.external_id)
            print("Title:", job.title)
            print("Company:", job.company)
            print("Location:", job.location)
            print("Workplace:", job.workplace_type)
            print("Employment:", job.employment_type)
            print("Published:", job.published_at)

    finally:
        db.close()


if __name__ == "__main__":
    main()