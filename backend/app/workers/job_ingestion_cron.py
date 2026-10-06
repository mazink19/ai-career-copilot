from app.services.job_ingestion_runner import run_job_ingestion


def main():
    report = run_job_ingestion()

    print(f"Job ingestion completed: {report.total_processed} jobs processed")

    for result in report.sources:
        if result.success:
            print(
                f"[SUCCESS] {result.source}/{result.company}: "
                f"{result.processed} jobs"
            )
        else:
            print(
                f"[FAILED] {result.source}/{result.company}: "
                f"{result.error}"
            )


if __name__ == "__main__":
    main()