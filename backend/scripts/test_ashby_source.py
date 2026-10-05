from app.integrations.jobs.ashby import AshbySource


def main():
    source = AshbySource(
        board_name="ashby",
        company="Ashby",
    )

    jobs = source.fetch_normalized_jobs()

    print(f"Fetched {len(jobs)} jobs")

    for job in jobs[:3]:
        print()
        print("Source:", job.source)
        print("External ID:", job.external_id)
        print("Title:", job.title)
        print("Company:", job.company)
        print("Location:", job.location)
        print("Workplace:", job.workplace_type)
        print("Employment:", job.employment_type)
        print("Published:", job.published_at)
        print("Job URL:", job.job_url)
        print("Application URL:", job.application_url)
        print("Description:", job.description[:300])


if __name__ == "__main__":
    main()