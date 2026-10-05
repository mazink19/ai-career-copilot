from app.integrations.jobs.base import JobSource
from app.repositories.job_repository import JobRepository


class JobIngestionService:
    # This service is responsible for ingesting jobs from a given source and updating the job repository accordingly.
    def __init__(self, repository: JobRepository):
        self.repository = repository
    # The ingest method takes a JobSource as input, fetches normalized jobs from the source, and updates the job repository. It returns the number of processed jobs. If the source returns an empty feed, it does not deactivate existing jobs and simply returns 0.
    def ingest(self, source: JobSource) -> int:
        jobs = source.fetch_normalized_jobs()

        # Never deactivate existing jobs if the source
        # unexpectedly returns an empty feed.
        if not jobs:
            return 0
        # Upsert the fetched jobs into the repository and get the count of processed jobs.
        processed = self.repository.upsert_many(jobs)

        external_ids = {
            job.external_id
            for job in jobs
        }
        # Deactivate any jobs that are no longer present in the source feed.
        self.repository.deactivate_missing_jobs(
            source=source.source_name,
            external_ids=external_ids,
        )

        return processed