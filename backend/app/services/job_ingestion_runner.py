from app.core.job_sources import (
    ASHBY_BOARDS,
    GREENHOUSE_BOARDS,
    LEVER_BOARDS,)

from app.schemas.job_ingestion import (
    IngestionReport,
    IngestionSourceResult,
)


from app.db.dependencies import get_db
from app.integrations.jobs.ashby import AshbySource
from app.integrations.jobs.greenhouse import GreenhouseSource
from app.integrations.jobs.lever import LeverSource
from app.repositories.job_repository import JobRepository
from app.services.job_ingestion_service import JobIngestionService


def run_job_ingestion() -> int:
    
    db = next(get_db())
    try:
        repository = JobRepository(db)
        service = JobIngestionService(repository)

        results = []

        for config in GREENHOUSE_BOARDS:
            try:
                source = GreenhouseSource(
                    board_token=config["board_token"],
                    company=config["company"],
                )

                processed = service.ingest(source)
                results.append(
                    IngestionSourceResult(
                        source="greenhouse",
                        company=config["company"],
                        processed=processed,
                        success=True,
                    )
                )

            except Exception as exc:
                results.append(
                    IngestionSourceResult(
                        source="greenhouse",
                        company=config["company"],
                        success=False,
                        error=str(exc),
                    )
                )

        for config in LEVER_BOARDS:
            try:
                source = LeverSource(
                    company=config["company"],
                )

                processed = service.ingest(source)

                results.append(
                    IngestionSourceResult(
                        source="lever",
                        company=config["company"],
                        processed=processed,
                        success=True,
                    )
                )

            except Exception as exc:
                results.append(
                    IngestionSourceResult(
                        source="lever",
                        company=config["company"],
                        success=False,
                        error=str(exc),
                    )
                )

        for config in ASHBY_BOARDS:
            try:
                source = AshbySource(
                    board_name=config["board_name"],
                    company=config["company"],
                )

                processed = service.ingest(source)
                results.append(
                    IngestionSourceResult(
                        source="ashby",
                        company=config["company"],
                        processed=processed,
                        success=True,
                    )
                )

            except Exception as exc:
                results.append(
                    IngestionSourceResult(
                        source="ashby",
                        company=config["company"],
                        success=False,
                        error=str(exc),
                    )
                )

        return IngestionReport(
            total_processed=sum(
                result.processed
                for result in results
            ),
            sources=results,
        )

    finally:
        db.close()