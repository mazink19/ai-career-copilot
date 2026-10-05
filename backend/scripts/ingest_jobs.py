import argparse

from app.db.dependencies import get_db

from app.integrations.jobs.ashby import AshbySource
from app.integrations.jobs.greenhouse import GreenhouseSource
from app.integrations.jobs.lever import LeverSource

from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_runner import run_job_ingestion

from app.services.job_ingestion_service import JobIngestionService

from app.core.job_sources import (
    ASHBY_BOARDS,
    GREENHOUSE_BOARDS,
    LEVER_BOARDS,
)

def ingest_greenhouse(service: JobIngestionService) -> int:
    total = 0

    for config in GREENHOUSE_BOARDS:
        source = GreenhouseSource(
            board_token=config["board_token"],
            company=config["company"],
        )

        count = service.ingest(source)

        print(
            f"Greenhouse - {config['company']}: "
            f"{count} jobs"
        )

        total += count

    return total


def ingest_lever(service: JobIngestionService) -> int:
    total = 0

    for config in LEVER_BOARDS:
        source = LeverSource(
            company=config["company"],
        )

        count = service.ingest(source)

        print(
            f"Lever - {config['company']}: "
            f"{count} jobs"
        )

        total += count

    return total


def ingest_ashby(service: JobIngestionService) -> int:
    total = 0

    for config in ASHBY_BOARDS:
        source = AshbySource(
            board_name=config["board_name"],
            company=config["company"],
        )

        count = service.ingest(source)

        print(
            f"Ashby - {config['company']}: "
            f"{count} jobs"
        )

        total += count

    return total


def main():
    parser = argparse.ArgumentParser(
        description="Ingest jobs from external ATS sources."
    )

    parser.add_argument(
        "--source",
        choices=["greenhouse", "lever", "ashby", "all"],
        default="all",
    )

    args = parser.parse_args()

    db = next(get_db())

    try:
        repository = JobRepository(db)
        service = JobIngestionService(repository)

        total = 0

        print("Starting job ingestion...\n")

        if args.source in ("greenhouse", "all"):
            count = ingest_greenhouse(service)
            print(f"Greenhouse: {count} jobs")
            total += count

        if args.source in ("lever", "all"):
            count = ingest_lever(service)
            print(f"Lever: {count} jobs")
            total += count

        if args.source in ("ashby", "all"):
            count = ingest_ashby(service)
            print(f"Ashby: {count} jobs")
            total += count

        print("\n--------------------------------")
        print(f"Total processed: {total}")
        print("--------------------------------")

    finally:
        db.close()


if __name__ == "__main__":
    total = run_job_ingestion()

    print(f"Ingestion completed: {total} jobs processed")