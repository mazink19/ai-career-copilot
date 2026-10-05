import { useEffect, useState } from "react";

import type { Page } from "../types/navigation";

import type {
  Resume,
  ResumeAnalysis,
} from "../types/resume";

import type {
  Job,
} from "../types/job";

import {
  getResumes,
  getJobs,
  getResumeAnalysis,
} from "../services/api";

/* ========================================================= */
/* Dashboard */
/* ========================================================= */

function Dashboard({onNavigate,
}: {
  onNavigate: (page: Page) => void;
}) {

  const [resumes, setResumes] = useState<Resume[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [latestAnalysis, setLatestAnalysis] =
    useState<ResumeAnalysis | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        const [resumeData, jobData] = await Promise.all([
          getResumes(),
          getJobs(),
        ]);

        setResumes(resumeData);
        setJobs(jobData.jobs);

        /*
         * Get analysis for the latest resume.
         *
         * We assume the backend returns resumes
         * newest-first.
         */
        if (resumeData.length > 0) {
          const latestResume = resumeData[0];

          try {
            const analysis = await getResumeAnalysis(
              latestResume.id
            );

            setLatestAnalysis(analysis);
          } catch {
            setLatestAnalysis(null);
          }
        } else {
          setLatestAnalysis(null);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load dashboard."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  /* ---------------- Loading ---------------- */

  if (loading) {
    return (
      <div className="flex min-h-100 items-center justify-center">
        <p className="text-sm text-zinc-500">
          Loading your career dashboard...
        </p>
      </div>
    );
  }

  /* ---------------- Error ---------------- */

  if (error) {
    return (
      <div className="rounded-3xl border border-red-200 bg-red-50 p-6 dark:border-red-900/40 dark:bg-red-950/20">
        <h2 className="font-semibold text-red-700 dark:text-red-400">
          Unable to load dashboard
        </h2>

        <p className="mt-2 text-sm text-red-600 dark:text-red-400">
          {error}
        </p>

        <button
          onClick={() => window.location.reload()}
          className="mt-4 rounded-xl bg-zinc-950 px-4 py-2 text-xs font-semibold text-white"
        >
          Try again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-10 pb-10">

      {/* -------------------------------------------------- */}
      {/* Welcome */}
      {/* -------------------------------------------------- */}

      <section className="relative overflow-hidden rounded-[28px] border border-zinc-200 bg-white px-6 py-8 shadow-sm md:px-10 md:py-10 dark:border-zinc-800 dark:bg-zinc-900">

        {/* Decorative background */}
        <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full bg-blue-500/10 blur-3xl" />

        <div className="pointer-events-none absolute -bottom-32 right-24 h-64 w-64 rounded-full bg-violet-500/10 blur-3xl" />

        <div className="relative">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">

            <div>
              <div className="mb-4 flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />

                <span className="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-400">
                  Career overview
                </span>
              </div>

              <h1 className="max-w-3xl text-3xl font-semibold tracking-[-0.03em] text-zinc-950 md:text-5xl dark:text-white">
                Build the career
                <br className="hidden md:block" />
                you want next.
              </h1>

              <p className="mt-4 max-w-xl text-sm leading-6 text-zinc-500 md:text-base dark:text-zinc-400">
                Your resume, skills, and opportunities in one place.
                See where you stand and what to improve next.
              </p>
            </div>

            <button
              onClick={() => onNavigate("settings")}
              className="group flex w-fit items-center gap-3 rounded-xl bg-zinc-950 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:shadow-xl hover:shadow-zinc-950/10 dark:bg-white dark:text-zinc-950 dark:hover:shadow-white/10"
            >
              <span>View career profile</span>

              <span className="transition-transform group-hover:translate-x-1">
                →
              </span>
            </button>

          </div>
        </div>
      </section>

      {/* -------------------------------------------------- */}
      {/* Main metrics */}
      {/* -------------------------------------------------- */}

      <section className="grid gap-5 lg:grid-cols-[1.4fr_1fr_1fr]">

        <CareerReadinessCard
          analysis={latestAnalysis}
        />

        <MetricCard
          label="Resumes"
          value={String(resumes.length)}
          description={
            resumes.length === 1
              ? "Resume uploaded"
              : "Resumes uploaded"
          }
          trend="Live"
        />

        <MetricCard
          label="Jobs"
          value={String(jobs.length)}
          description="Available opportunities"
          trend="Live"
        />

      </section>

      {/* -------------------------------------------------- */}
      {/* Resume + jobs */}
      {/* -------------------------------------------------- */}

      <section className="grid gap-5 xl:grid-cols-[1.05fr_0.95fr]">

        <ResumeOverview
          analysis={latestAnalysis}
         onViewResume={() => onNavigate("resume")}
        />

        <JobMatches
          jobs={jobs}
          onViewJobs={() => onNavigate("jobs")}
        />

      </section>

      {/* -------------------------------------------------- */}
      {/* Bottom section */}
      {/* -------------------------------------------------- */}

      <section className="grid gap-5 lg:grid-cols-2">

        <NextAction
          analysis={latestAnalysis}
          onViewResume={() => onNavigate("resume")}
        />

        <RecentActivity
          resumes={resumes}
          jobs={jobs}
        />

      </section>

    </div>
  );
}

/* ========================================================= */
/* Career readiness */
/* ========================================================= */

function CareerReadinessCard({
  analysis,
}: {
  analysis: ResumeAnalysis | null;
}) {
  const status = analysis?.status ?? "NO_ANALYSIS";

  const statusText = {
  pending: "Analysis pending",
  analyzing: "Analysis in progress",
  completed: "Analysis completed",
  failed: "Analysis failed",
  NO_ANALYSIS: "No resume analysis yet",
}[status];

  const progressWidth = {
  pending: "25%",
  analyzing: "60%",
  completed: "100%",
  failed: "100%",
  NO_ANALYSIS: "0%",
}[status];

const progressClass = {
  pending: "bg-yellow-400",
  analyzing: "bg-yellow-400",
  completed: "bg-emerald-400",
  failed: "bg-red-400",
  NO_ANALYSIS: "bg-zinc-700",
}[status];
  return (
    <div className="relative overflow-hidden rounded-3xl border border-zinc-200 bg-zinc-950 p-7 text-white shadow-sm dark:border-zinc-800">

      <div className="pointer-events-none absolute -right-16 -top-16 h-48 w-48 rounded-full bg-blue-500/20 blur-3xl" />

      <div className="relative">

        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
          Career readiness
        </p>

        <div className="mt-5">
          <span className="text-3xl font-semibold tracking-tight">
            {statusText}
          </span>
        </div>

        <p className="mt-4 max-w-md text-sm leading-6 text-zinc-400">
          {analysis?.summary ??
            "Upload a resume to receive your AI-powered career analysis."}
        </p>

        <div className="mt-7">

          <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
            <div
              className={`h-full rounded-full transition-all duration-700 ${progressClass}`}
              style={{
                width: progressWidth,
              }}
            />
          </div>

          <p className="mt-4 text-xs text-zinc-500">
            {getAnalysisDescription(status)}
          </p>

        </div>
      </div>
    </div>
  );
}

function getAnalysisDescription(
  status:
    | ResumeAnalysis["status"]
    | "NO_ANALYSIS"
) {
  switch (status) {
    case "completed":
      return "Your latest resume has been evaluated.";

    case "analyzing":
      return "Your resume is currently being analyzed.";

    case "pending":
      return "Your resume is waiting for analysis.";

    case "failed":
      return "Resume analysis could not be completed.";

    default:
      return "Upload a resume to get started.";
  }
}

/* ========================================================= */
/* Metric card */
/* ========================================================= */

function MetricCard({
  label,
  value,
  suffix,
  description,
  trend,
}: {
  label: string;
  value: string;
  suffix?: string;
  description: string;
  trend: string;
}) {
  return (
    <div className="group rounded-3xl border border-zinc-200 bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-zinc-200/40 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:shadow-black/20">

      <div className="flex items-start justify-between">

        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
          {label}
        </p>

        <span className="rounded-full bg-zinc-100 px-2.5 py-1 text-[10px] font-semibold text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400">
          {trend}
        </span>

      </div>

      <div className="mt-8 flex items-baseline gap-1">

        <span className="text-5xl font-semibold tracking-tighter">
          {value}
        </span>

        {suffix && (
          <span className="text-sm text-zinc-400">
            {suffix}
          </span>
        )}

      </div>

      <p className="mt-3 text-xs text-zinc-500">
        {description}
      </p>

    </div>
  );
}

/* ========================================================= */
/* Resume overview */
/* ========================================================= */

function ResumeOverview({
  analysis,
  onViewResume,
}: {
  analysis: ResumeAnalysis | null;
  onViewResume: () => void;
}) {
  return (
    <div className="rounded-3xl border border-zinc-200 bg-white p-6 md:p-7 dark:border-zinc-800 dark:bg-zinc-900">

      <div className="flex items-start justify-between">

        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
            Resume intelligence
          </p>

          <h2 className="mt-2 text-xl font-semibold tracking-tight">
            Latest analysis
          </h2>
        </div>

        <button
          onClick={onViewResume}
          className="text-xs font-semibold text-zinc-400 transition hover:text-zinc-950 dark:hover:text-white"
        >
          View resume →
        </button>

      </div>

      {!analysis ? (
        <div className="mt-7 rounded-2xl bg-zinc-50 p-5 dark:bg-zinc-800/50">

          <p className="text-sm font-semibold">
            No analysis available
          </p>

          <p className="mt-2 text-xs leading-5 text-zinc-400">
            Upload a resume to receive your AI-powered analysis.
          </p>

        </div>
      ) : (
        <>
          <div className="mt-7 grid gap-5 sm:grid-cols-2">

          <AnalysisCount
            label="Skills"
            count={analysis.skills?.length ?? 0}
          />

          <AnalysisCount
            label="Experience"
            count={analysis.experience?.length ?? 0}
          />

          <AnalysisCount
            label="Education"
            count={analysis.education?.length ?? 0}
          />

          <AnalysisCount
            label="Projects"
            count={analysis.projects?.length ?? 0}
          />

          </div>

          <div className="mt-7 rounded-2xl bg-zinc-50 px-4 py-4 dark:bg-zinc-800/50">

            <p className="text-xs font-semibold">
              Analysis status
            </p>

            <p className="mt-1 text-[11px] text-zinc-400">
              {analysis.status}
            </p>

          </div>
        </>
      )}

    </div>
  );
}

function AnalysisCount({
  label,
  count,
}: {
  label: string;
  count: number;
}) {
  return (
    <div className="rounded-2xl border border-zinc-100 p-4 dark:border-zinc-800">

      <p className="text-xs font-medium text-zinc-500">
        {label}
      </p>

      <p className="mt-3 text-3xl font-semibold tracking-tight">
        {count}
      </p>

      <p className="mt-1 text-[11px] text-zinc-400">
        extracted items
      </p>

    </div>
  );
}

/* ========================================================= */
/* Job matches */
/* ========================================================= */

function JobMatches({
  jobs,
  onViewJobs,
}: {
  jobs: Job[];
  onViewJobs: () => void;
}) {
  const visibleJobs = jobs.slice(0, 3);

  return (
    <div className="rounded-3xl border border-zinc-200 bg-white p-6 md:p-7 dark:border-zinc-800 dark:bg-zinc-900">

      <div className="flex items-start justify-between">

        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
            Opportunities
          </p>

          <h2 className="mt-2 text-xl font-semibold tracking-tight">
            Recent jobs
          </h2>
        </div>

        <button
          onClick={onViewJobs}
          className="text-xs font-semibold text-zinc-400 transition hover:text-zinc-950 dark:hover:text-white"
        >
          View all →
        </button>

      </div>

      {visibleJobs.length === 0 ? (
        <div className="mt-6 rounded-2xl bg-zinc-50 p-5 dark:bg-zinc-800/50">

          <p className="text-sm font-semibold">
            No jobs available
          </p>

          <p className="mt-2 text-xs text-zinc-400">
            Check the jobs page for available opportunities.
          </p>

        </div>
      ) : (
        <div className="mt-6 divide-y divide-zinc-100 dark:divide-zinc-800">

          {visibleJobs.map((job) => (
            <JobRow
              key={job.id}
              title={job.title}
              company={job.company}
              initial={job.title
                .slice(0, 2)
                .toUpperCase()}
            />
          ))}

        </div>
      )}

    </div>
  );
}

function JobRow({
  title,
  company,
  initial,
}: {
  title: string;
  company: string;
  initial: string;
}) {
  return (
    <div className="group flex items-center gap-4 py-4 first:pt-1 last:pb-1">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-zinc-200 bg-zinc-50 text-[10px] font-bold text-zinc-500 dark:border-zinc-800 dark:bg-zinc-800 dark:text-zinc-300">
        {initial}
      </div>

      <div className="min-w-0 flex-1">

        <p className="truncate text-sm font-semibold">
          {title}
        </p>

        <p className="mt-1 truncate text-[11px] text-zinc-400">
          {company}
        </p>

      </div>

    </div>
  );
}

/* ========================================================= */
/* Next action */
/* ========================================================= */

function NextAction({
  analysis,
  onViewResume,
}: {
  analysis: ResumeAnalysis | null;
  onViewResume: () => void;
}) {
  const projectCount = analysis?.projects?.length ?? 0;

  return (
    <div className="relative overflow-hidden rounded-3xl border border-blue-200/70 bg-blue-50/60 p-7 dark:border-blue-900/40 dark:bg-blue-950/20">

      <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-blue-400/10 blur-2xl" />

      <div className="relative">

        <div className="flex items-center gap-2">

          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600 text-xs text-white">
            →
          </span>

          <p className="text-xs font-bold uppercase tracking-[0.14em] text-blue-600 dark:text-blue-400">
            Recommended next step
          </p>

        </div>

        <h2 className="mt-5 max-w-md text-2xl font-semibold tracking-tight">
          {analysis
            ? "Review your resume analysis."
            : "Upload your resume first."}
        </h2>

        <p className="mt-3 max-w-md text-sm leading-6 text-zinc-500 dark:text-zinc-400">
          {analysis
            ? `Your latest analysis extracted ${projectCount} project${
                projectCount === 1 ? "" : "s"
              }. Review the full analysis to identify areas you can improve.`
            : "Upload your resume to let the AI analyze your skills, experience, education, and projects."}
        </p>

        <button
          onClick={onViewResume}
          className="mt-6 rounded-xl bg-zinc-950 px-4 py-2.5 text-xs font-semibold text-white transition hover:-translate-y-0.5 dark:bg-white dark:text-zinc-950"
        >
          {analysis
            ? "Review resume →"
            : "Upload resume →"}
        </button>

      </div>
    </div>
  );
}

/* ========================================================= */
/* Recent activity */
/* ========================================================= */

function RecentActivity({
  resumes,
  jobs,
}: {
  resumes: Resume[];
  jobs: Job[];
}) {
  return (
    <div className="rounded-3xl border border-zinc-200 bg-white p-7 dark:border-zinc-800 dark:bg-zinc-900">

      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
          Activity
        </p>

        <h2 className="mt-2 text-xl font-semibold tracking-tight">
          Recent activity
        </h2>
      </div>

      <div className="mt-6 space-y-5">

        {resumes.length > 0 && (
          <ActivityItem
            title={`Resume uploaded: ${resumes[0].file_name}`}
            time={formatDate(resumes[0].uploaded_at)}
            icon="✓"
          />
        )}

        <ActivityItem
          title={`${jobs.length} jobs currently available`}
          time="Current"
          icon="↗"
        />

        {resumes.length === 0 && (
          <ActivityItem
            title="No resume uploaded yet"
            time="Get started by uploading one"
            icon="!"
          />
        )}

      </div>

    </div>
  );
}

function ActivityItem({
  title,
  time,
  icon,
}: {
  title: string;
  time: string;
  icon: string;
}) {
  return (
    <div className="flex items-center gap-4">

      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-zinc-100 text-xs text-zinc-500 dark:bg-zinc-800 dark:text-zinc-300">
        {icon}
      </div>

      <div className="flex-1">

        <p className="text-xs font-semibold">
          {title}
        </p>

        <p className="mt-1 text-[11px] text-zinc-400">
          {time}
        </p>

      </div>

    </div>
  );
}

/* ========================================================= */
/* Helpers */
/* ========================================================= */

function formatDate(date: string) {
  return new Date(date).toLocaleDateString();
}

/* ========================================================= */
/* Export */
/* ========================================================= */

export default Dashboard;