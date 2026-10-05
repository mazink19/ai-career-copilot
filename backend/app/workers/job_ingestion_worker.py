from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.job_ingestion_runner import run_job_ingestion


def run():
    print("Starting job ingestion...")

    try:
        report = run_job_ingestion()

        print(
            f"Job ingestion completed: "
            f"{report.total_processed} jobs processed"
        )

        for result in report.sources:
            if result.success:
                print(
                    f"[SUCCESS] "
                    f"{result.source}/{result.company}: "
                    f"{result.processed} jobs"
                )
            else:
                print(
                    f"[FAILED] "
                    f"{result.source}/{result.company}: "
                    f"{result.error}"
                )

    except Exception as exc:
        print(f"Job ingestion failed: {exc}")


def main():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run,
        trigger="interval",
        hours=6,
        id="job_ingestion",
        replace_existing=True,
    )

    print("Job ingestion worker started.")
    print("Running every 6 hours.")

    run()

    scheduler.start()


if __name__ == "__main__":
    main()