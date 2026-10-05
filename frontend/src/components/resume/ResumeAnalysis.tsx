import AnalysisSection from "./AnalysisSection";
import type { ResumeAnalysis as ResumeAnalysisType } from "../../types/resume";

interface ResumeAnalysisProps {
  analysis: ResumeAnalysisType;
}

export default function ResumeAnalysis({
  analysis,
}: ResumeAnalysisProps) {
  // Backend may return "completed", "pending", etc.
  // Normalize it so the UI is not sensitive to casing.
  const status = String(analysis.status).toUpperCase();

  const skills = analysis.skills ?? [];
  const experience = analysis.experience ?? [];
  const education = analysis.education ?? [];
  const projects = analysis.projects ?? [];

const sections = [

  {
    title: "Skills",
    items: skills,
  },
  {
    title: "Experience",
    items: experience,
  },
  {
    title: "Education",
    items: education,
  },
  {
    title: "Projects",
    items: projects,
  },
  ];

  const totalItems =
    skills.length +
    experience.length +
    education.length +
    projects.length;

  const hasAnalysisData = totalItems > 0;

  return (
    <section>
      {/* Header */}
      <div className="mb-5">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
          Resume intelligence
        </p>

        <h2 className="mt-2 text-2xl font-semibold tracking-tight">
          Latest analysis
        </h2>
      </div>

      {/* Status */}
      <div className="mb-5 flex items-center gap-2">
        <span
          className={`
            h-2 w-2 rounded-full
            ${
              status === "COMPLETED"
                ? "bg-emerald-500"
                : status === "FAILED"
                  ? "bg-red-500"
                  :status == "ANALYZING"
                   ? "bg-blue-500 animate-pulse"
                  : "bg-amber-500"
            }
          `}
        />

        <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">
          {getStatusLabel(status)}
        </span>
      </div>

      {/* Status + Summary */}
      <div className="grid gap-5 lg:grid-cols-[0.35fr_0.65fr]">

        {/* Analysis status */}
        <div className="rounded-3xl bg-zinc-950 p-7 text-white dark:border dark:border-zinc-800">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
            Analysis status
          </p>

          <div className="mt-6">
            <span className="text-3xl font-semibold tracking-tight">
              {getStatusTitle(status)}
            </span>
          </div>

          {/* Progress */}
          <div className="mt-7 h-1.5 overflow-hidden rounded-full bg-white/10">
            <div
              className={`
                h-full rounded-full transition-all duration-500
                ${
                  status === "COMPLETED"
                    ? "w-full bg-emerald-400"
                    : status === "FAILED"
                      ? "w-full bg-red-400"
                      : status === "ANALYZING"
                         ? "w-2/3 bg-blue-400"
                       : "w-1/3 bg-amber-400"
                }
              `}
            />
          </div>

          <p className="mt-4 text-xs leading-5 text-zinc-500">
            {getStatusDescription(status)}
          </p>
        </div>

        {/* Professional summary */}
        <div className="rounded-3xl border border-zinc-200 bg-white p-7 dark:border-zinc-800 dark:bg-zinc-900">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
            Professional summary
          </p>

          {analysis.summary ? (
            <p className="mt-5 text-sm leading-7 text-zinc-600 dark:text-zinc-300">
              {analysis.summary}
            </p>
          ) : (
            <p className="mt-5 text-sm leading-7 text-zinc-400">
              No professional summary was generated yet.
            </p>
          )}
        </div>
      </div>

      {/* Analysis categories */}
      {hasAnalysisData ? (
        <div className="mt-5 grid gap-5 md:grid-cols-2">
          {sections.map((section) => (
            <AnalysisSection
              key={section.title}
              title={section.title}
              items={section.items}
            />
          ))}
        </div>
      ) : (
        <div className="mt-5 rounded-3xl border border-dashed border-zinc-300 bg-white p-8 text-center dark:border-zinc-700 dark:bg-zinc-900">
          <p className="text-sm font-semibold">
            No analysis details available
          </p>

          <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
            The analysis has not produced any structured
            information yet.
          </p>
        </div>
      )}
    </section>
  );
}

/* ---------------- Helpers ---------------- */

function getStatusLabel(status: string) {
  switch (status) {
    case "COMPLETED":
      return "Analysis completed";

    case "ANALYZING":
      return "Analysis in progress";

    case "PENDING":
      return "Waiting for analysis";

    case "FAILED":
      return "Analysis failed";

    default:
      return "Unknown status";
  }
}

function getStatusTitle(status: string) {
  switch (status) {
    case "COMPLETED":
      return "Completed";

    case "ANALYZING":
      return "Analyzing...";

    case "PENDING":
      return "Pending";

    case "FAILED":
      return "Failed";

    default:
      return "Unknown";
  }
}

function getStatusDescription(status: string) {
  switch (status) {
    case "COMPLETED":
      return "Your resume has been analyzed successfully.";

    case "ANALYZING":
      return "Your resume is currently being analyzed.";

    case "PENDING":
      return "Your resume is waiting to be analyzed.";

    case "FAILED":
      return "The resume analysis could not be completed.";

    default:
      return "Analysis status is unavailable.";
  }
}