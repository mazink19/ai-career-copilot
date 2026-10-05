from app.integrations.jobs.greenhouse import GreenhouseSource


def main():
    source = GreenhouseSource(
    board_token="anthropic",
    company="Anthropic",
)

    jobs = source.fetch_normalized_jobs()

    print(f"Found {len(jobs)} jobs")

    for job in jobs[:3]:
        print()
        print("Source:", job.source)
        print("External ID:", job.external_id)
        print("Title:", job.title)
        print("Company:", job.company)
        print("Location:", job.location)
        print("Job URL:", job.job_url)
        print("Application URL:", job.application_url)
        print("Updated:", job.source_updated_at)


if __name__ == "__main__":
    main()