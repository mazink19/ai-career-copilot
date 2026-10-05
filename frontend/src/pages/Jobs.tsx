import { useEffect, useState } from "react";
import JobSearch from "../components/jobs/JobSearch";
import JobFilters from "../components/jobs/JobFilters";
import JobCard from "../components/jobs/JobCard";
import { getJobs } from "../services/api";
import type { Job, JobMatchAnalysis } from "../types/job";

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [page, setPage] = useState(1);

  const PAGE_SIZE = 20;
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("all");
  const [match, setMatch] = useState("all");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const totalPages = Math.ceil(total / PAGE_SIZE);
  const [matchResults, setMatchResults] = useState<
    Record<number, JobMatchAnalysis>
  >({});

  const handleMatch = (
    jobId: number,
    result: JobMatchAnalysis
  ) => {
    setMatchResults((prev) => ({
      ...prev,
      [jobId]: result,
    }));
  };
  // Reset page to 1 whenever search or location changes
  useEffect(() => {
  setPage(1);
}, [search, location]);

  // Load jobs from backend whenever search/location changes
  useEffect(() => {
    async function loadJobs() {
      try {
        setLoading(true);
        setError(null);

        const data = await getJobs({
          search: search.trim() || undefined,
          location:
            location !== "all" ? location : undefined,
          limit: PAGE_SIZE,
          offset: (page - 1) * PAGE_SIZE
        });

        setJobs(data.jobs);
        setTotal(data.total);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load jobs."
        );
      } finally {
        setLoading(false);
      }
    }

    loadJobs();
  }, [search, location, page]);

  // Match score filtering stays client-side
  const filteredJobs = jobs.filter((job) => {
    const jobMatch = matchResults[job.id];

    return (
      match === "all" ||
      (jobMatch !== undefined &&
        jobMatch.match_score >= Number(match))
    );
  });

  return (
    <div className="space-y-8 pb-10">

      {/* Header */}
      <section>
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-blue-500" />

          <span className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-400">
            Career intelligence
          </span>
        </div>

        <div className="mt-4 flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div>
            <h1 className="text-4xl font-semibold tracking-[-0.04em] md:text-5xl">
              Job matches
            </h1>

            <p className="mt-4 max-w-2xl text-sm leading-6 text-zinc-500 md:text-base dark:text-zinc-400">
              Discover opportunities ranked against your resume,
              skills, and career profile.
            </p>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white px-4 py-3 dark:border-zinc-800 dark:bg-zinc-900">
            <p className="text-2xl font-bold">
              {filteredJobs.length}
            </p>

            <p className="text-xs text-zinc-400">
              matching opportunities
            </p>
          </div>
        </div>
      </section>

      {/* Search / filters */}
      <section className="rounded-3xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
        <div className="grid gap-3 lg:grid-cols-[1fr_auto]">
          <JobSearch
            search={search}
            onSearchChange={setSearch}
          />

          <JobFilters
            location={location}
            match={match}
            onLocationChange={setLocation}
            onMatchChange={setMatch}
          />
        </div>
      </section>

      {/* Loading */}
      {loading && (
        <section className="space-y-4">
          {[1, 2, 3].map((item) => (
            <div
              key={item}
              className="h-48 animate-pulse rounded-3xl bg-zinc-100 dark:bg-zinc-900"
            />
          ))}
        </section>
      )}

      {/* Error */}
      {!loading && error && (
        <div className="rounded-3xl border border-red-200 bg-red-50 p-8 dark:border-red-900/50 dark:bg-red-950/20">
          <p className="text-sm font-semibold text-red-700 dark:text-red-400">
            Unable to load jobs
          </p>

          <p className="mt-2 text-sm text-red-600/80 dark:text-red-400/70">
            {error}
          </p>
        </div>
      )}

      {/* Jobs */}
      {!loading && !error && (
        <section className="space-y-4">
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                onMatch={handleMatch}
              />
            ))
          ) : (
            <div className="rounded-3xl border border-dashed border-zinc-300 bg-white p-12 text-center dark:border-zinc-700 dark:bg-zinc-900">
              <p className="text-sm font-semibold">
                No matching jobs
              </p>

              <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
                Try changing your search or filters.
              </p>
            </div>
          )}
        </section>
      )}
      {/* Pagination */}
{!loading && !error && jobs.length > 0 && (
  <div className="flex items-center justify-center gap-4 pt-6">
    <button
      onClick={() => setPage((prev) => prev - 1)}
      disabled={page === 1}
      className="rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-700"
    >
      Previous
    </button>

    <span className="text-sm text-zinc-500 dark:text-zinc-400">
      Page {page} of {totalPages}
      disabled={page >= totalPages} 
    </span>

    <button
      onClick={() => setPage((prev) => prev + 1)}
      disabled={jobs.length < PAGE_SIZE}
      className="rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-700"
    >
      Next
    </button>
  </div>
)}
    </div>
  );
}