import { useState } from "react";
import { matchJob } from "../../services/api";
import type {
  Job,
  JobMatchAnalysis,
} from "../../types/job";

interface JobCardProps {
  job: Job;
  onMatch: (jobId: number, result: JobMatchAnalysis) => void;
}


export default function JobCard({ job, onMatch }: JobCardProps) {
  const [analysis, setAnalysis] =
    useState<JobMatchAnalysis | null>(null);

  const [analyzing, setAnalyzing] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleMatch() {
    try {
      setAnalyzing(true);
      setError(null);

      const result = await matchJob(job.id);

      setAnalysis(result);
      onMatch(job.id, result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to analyze job match."
      );
    } finally {
      setAnalyzing(false);
    }
  }

  return (
    <article className="group overflow-hidden rounded-3xl border border-zinc-200 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-zinc-300 hover:shadow-xl hover:shadow-zinc-200/40 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700 dark:hover:shadow-black/20">
      <div className="p-6 md:p-7">

        {/* Top */}
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex min-w-0 gap-4">

            {/* Company avatar */}
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-zinc-950 text-sm font-bold text-white dark:bg-white dark:text-zinc-950">
              {job.company.charAt(0).toUpperCase()}
            </div>

            <div className="min-w-0">
              <h3 className="truncate text-xl font-semibold tracking-tight">
                {job.title}
              </h3>

              <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                {job.company}
              </p>
            </div>
          </div>

          {/* Job badge */}
          <span className="w-fit rounded-full bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700 dark:bg-blue-950/40 dark:text-blue-300">
            Open position
          </span>
        </div>

        {/* Description */}
        <div className="mt-6">
          <p className="line-clamp-4 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
                  {job.description.length > 500
            ? `${job.description.slice(0, 550)}...`
            : job.description}
                </p>
        </div>

        {/* AI Analysis */}
        {analysis && (
          <div className="mt-6 rounded-2xl border border-blue-200 bg-blue-50/50 p-5 dark:border-blue-900/50 dark:bg-blue-950/20">

            {/* Score */}
            {/* Score */}
              <div>
                <div className="flex items-center justify-between">
                  <div>
                   <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-600 dark:text-blue-400">
                      AI Match
                    </p>

                    <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                      Resume compatibility
                    </p>
                  </div>

                  <span className="text-2xl font-semibold tracking-tight text-blue-700 dark:text-blue-300">
                    {analysis.match_score}%
                  </span>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-blue-100 dark:bg-blue-950">
                  <div
                    className="h-full rounded-full bg-blue-600 transition-all duration-500"
                    style={{ width: `${analysis.match_score}%` }}
                  />
                </div>
              </div>

            {/* Matched skills */}
            {analysis.matched_skills.length > 0 && (
              <div className="mt-5">
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                  Matched skills
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                  {analysis.matched_skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missing skills */}
            {analysis.missing_skills.length > 0 && (
              <div className="mt-5">
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                  Skills to improve
                </p>

                <div className="mt-2 flex flex-wrap gap-2">
                  {analysis.missing_skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-700 dark:bg-amber-950/30 dark:text-amber-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Strengths */}
            {analysis.strengths.length > 0 && (
              <div className="mt-5">
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                  Strengths
                </p>

                <ul className="mt-2 space-y-2">
                  {analysis.strengths.map((strength) => (
                    <li
                      key={strength}
                      className="flex gap-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300"
                      >
                      <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-zinc-400" />
                      <span>{strength}</span>
                      </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendations */}
            {analysis.recommendations.length > 0 && (
              <div className="mt-5">
                <p className="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-400">
                  Recommendations
                </p>

                <ul className="mt-2 space-y-2">
                  {analysis.recommendations.map((recommendation) => (
                    <li
                      key={recommendation}
                      className="flex gap-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300"
                    >
                      <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-400" />
                      <span>{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {/* Empty analysis state */}
              {analysis.matched_skills.length === 0 &&
              analysis.missing_skills.length === 0 &&
              analysis.strengths.length === 0 &&
              analysis.recommendations.length === 0 && (
              <p className="mt-5 text-sm text-zinc-500 dark:text-zinc-400">
                 No additional match insights were available.
              </p>
              )}
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600 dark:bg-red-950/20 dark:text-red-400">
            {error}
          </div>
        )}

        {/* Footer */}
        <div className="mt-7 flex flex-col gap-3 border-t border-zinc-100 pt-5 sm:flex-row sm:items-center sm:justify-between dark:border-zinc-800">

          <p className="text-xs text-zinc-400">
            AI matching available
          </p>

          <div className="flex flex-wrap gap-2">

            {/* Analyze */}
            <button
              onClick={handleMatch}
              disabled={analyzing}
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-zinc-200 px-4 py-2.5 text-sm font-semibold transition hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-700 dark:hover:bg-zinc-800"
            >
              {analyzing ? (
                <>
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-900 dark:border-zinc-600 dark:border-t-white" />
                  Analyzing...
                </>
              ) : (
                <>
                  Analyze match
                  <span>✦</span>
                </>
              )}
            </button>

            {/* Application */}
            <a
              href={job.application_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-zinc-950 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-zinc-800 dark:bg-white dark:text-zinc-950 dark:hover:bg-zinc-200"
            >
              View opportunity
              <span className="transition-transform duration-200 group-hover:translate-x-0.5">
                →
              </span>
            </a>

          </div>
        </div>

      </div>
    </article>
  );
}