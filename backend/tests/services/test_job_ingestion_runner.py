from unittest.mock import Mock, patch

from app.services.job_ingestion_runner import run_job_ingestion


@patch("app.services.job_ingestion_runner.JobIngestionService")
@patch("app.services.job_ingestion_runner.JobRepository")
@patch("app.services.job_ingestion_runner.get_db")
@patch("app.services.job_ingestion_runner.GreenhouseSource")
@patch("app.services.job_ingestion_runner.LeverSource")
@patch("app.services.job_ingestion_runner.AshbySource")
def test_runner_continues_when_one_source_fails(
    mock_ashby,
    mock_lever,
    mock_greenhouse,
    mock_get_db,
    mock_repository,
    mock_service,
):
    db = Mock()
    mock_get_db.return_value = iter([db])

    service = mock_service.return_value

    greenhouse = mock_greenhouse.return_value
    lever = mock_lever.return_value
    ashby = mock_ashby.return_value

    greenhouse.source_name = "greenhouse"
    lever.source_name = "lever"
    ashby.source_name = "ashby"

    service.ingest.side_effect = [
        RuntimeError("Greenhouse failed"),
        10,
        20,
    ]

    with patch(
        "app.services.job_ingestion_runner.GREENHOUSE_BOARDS",
        [
            {
                "board_token": "test",
                "company": "Greenhouse Test",
            }
        ],
    ), patch(
        "app.services.job_ingestion_runner.LEVER_BOARDS",
        [
            {
                "company": "Lever Test",
            }
        ],
    ), patch(
        "app.services.job_ingestion_runner.ASHBY_BOARDS",
        [
            {
                "board_name": "test",
                "company": "Ashby Test",
            }
        ],
    ):
        report = run_job_ingestion()

    assert report.total_processed == 30

    assert len(report.sources) == 3

    assert report.sources[0].success is False
    assert report.sources[0].source == "greenhouse"

    assert report.sources[1].success is True
    assert report.sources[1].processed == 10

    assert report.sources[2].success is True
    assert report.sources[2].processed == 20

    assert service.ingest.call_count == 3

    db.close.assert_called_once()