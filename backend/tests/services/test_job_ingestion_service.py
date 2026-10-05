from unittest.mock import Mock
import pytest

from app.services.job_ingestion_service import JobIngestionService


def test_ingest_processes_jobs():
    repository = Mock()
    source = Mock()

    source.source_name = "greenhouse"

    jobs = [
        Mock(source="greenhouse", external_id="1"),
        Mock(source="greenhouse", external_id="2"),
    ]

    source.fetch_normalized_jobs.return_value = jobs
    repository.upsert_many.return_value = 2

    service = JobIngestionService(repository)

    result = service.ingest(source)

    assert result == 2

    repository.upsert_many.assert_called_once_with(jobs)

    repository.deactivate_missing_jobs.assert_called_once_with(
        source="greenhouse",
        external_ids={"1", "2"},
    )


def test_ingest_does_not_deactivate_jobs_when_feed_is_empty():
    repository = Mock()
    source = Mock()

    source.source_name = "greenhouse"
    source.fetch_normalized_jobs.return_value = []

    service = JobIngestionService(repository)

    result = service.ingest(source)

    assert result == 0

    repository.upsert_many.assert_not_called()
    repository.deactivate_missing_jobs.assert_not_called()    


def test_ingest_propagates_source_error():
    repository = Mock()
    source = Mock()

    source.source_name = "greenhouse"

    source.fetch_normalized_jobs.side_effect = RuntimeError(
        "Greenhouse API failed"
    )

    service = JobIngestionService(repository)

    with pytest.raises(RuntimeError, match="Greenhouse API failed"):
        service.ingest(source)

    repository.upsert_many.assert_not_called()
    repository.deactivate_missing_jobs.assert_not_called()
