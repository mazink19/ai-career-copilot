import { useCallback, useEffect, useState } from "react";

import ResumeUpload from "../components/resume/ResumeUpload";
import ResumeCard from "../components/resume/ResumeCard";
import ResumeAnalysis from "../components/resume/ResumeAnalysis";


import {
  deleteResume, 
  getResumeAnalysis,
  getResumes,
} from "../services/api";

import type {
  Resume as ResumeType,
  ResumeAnalysis as ResumeAnalysisType,
} from "../types/resume";

export default function Resume() {
  const [resumes, setResumes] = useState<ResumeType[]>([]);
  const [selectedResume, setSelectedResume] =
    useState<ResumeType | null>(null);

  const [analysis, setAnalysis] =
    useState<ResumeAnalysisType | null>(null);

  const [loading, setLoading] = useState(true);
  const [analysisLoading, setAnalysisLoading] =
    useState(false);

  const [error, setError] = useState<string | null>(null);

  // ---------------- Load resumes ----------------

  const loadResumes = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await getResumes();

      setResumes(data);

      if (data.length === 0) {
       setSelectedResume(null);
       setAnalysis(null);
       return;
      }

      setSelectedResume((current) => {
        if (current) {
          const stillExists = data.find(
          (resume) => resume.id === current.id
          );

        if (stillExists) {
        return stillExists;
        }
      }

        return data[0];
});
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load resumes."
      );
    } finally {
      setLoading(false);
    }
  }, []);

  // ---------------- Initial load ----------------

  useEffect(() => {
    loadResumes();
  }, [loadResumes]);

  // ---------------- Analysis polling ----------------

  useEffect(() => {
    if (!selectedResume) {
      setAnalysis(null);
      return;
    }

    let cancelled = false;
    let timeoutId: number | undefined;

    async function pollAnalysis() {
      try {
        setAnalysisLoading(true);
        setError(null);

        const data = await getResumeAnalysis(
          selectedResume!.id
        );

        if (cancelled) {
          return;
        }

        setAnalysis(data);

        // Keep polling while the backend is processing
        if (
          data.status === "pending" ||
          data.status === "analyzing"
        ) {
          timeoutId = window.setTimeout(
            pollAnalysis,
            3000
          );
        }
      } catch (err) {
        if (cancelled) {
          return;
        }

        setAnalysis(null);

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load resume analysis."
        );
      } finally {
        if (!cancelled) {
          setAnalysisLoading(false);
        }
      }
    }

    pollAnalysis();

    return () => {
      cancelled = true;

      if (timeoutId !== undefined) {
        window.clearTimeout(timeoutId);
      }
    };
  }, [selectedResume]);
  // ---------------- Delete resume ----------------
  async function handleDelete(resume: ResumeType) {
  const confirmed = window.confirm(
    `Delete "${resume.file_name}"? This action cannot be undone.`
  );

  if (!confirmed) {
    return;
  }

  try {
    setError(null);

    await deleteResume(resume.id);

    // If the deleted resume was selected,
    // clear its analysis immediately.
    if (selectedResume?.id === resume.id) {
      setSelectedResume(null);
      setAnalysis(null);
    }

    await loadResumes();
  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "Failed to delete resume."
    );
  }
}

  // ---------------- Upload ----------------

  async function handleUploaded() {
    await loadResumes();
  }

  return (
    <div className="space-y-10 pb-10">

      {/* Header */}
      <section>
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
          Career Copilot
        </p>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight">
          Your Resumes
        </h1>

        <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-500 dark:text-zinc-400">
          Upload and analyze your resumes to understand
          your skills, experience, education, and projects.
        </p>
      </section>

      {/* Upload */}
      <ResumeUpload onUploaded={handleUploaded} />

      {/* Error */}
      {error && (
        <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/20 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Resumes */}
      <section>
        <div className="mb-5">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-400">
            Your documents
          </p>

          <h2 className="mt-2 text-2xl font-semibold tracking-tight">
            Resumes
          </h2>
        </div>

        {loading ? (
          <div className="rounded-3xl border border-zinc-200 bg-white p-8 text-center dark:border-zinc-800 dark:bg-zinc-900">
            <p className="text-sm text-zinc-500">
              Loading resumes...
            </p>
          </div>
        ) : resumes.length === 0 ? (
          <div className="rounded-3xl border border-dashed border-zinc-300 bg-white p-8 text-center dark:border-zinc-700 dark:bg-zinc-900">
            <p className="text-sm font-semibold">
              No resumes yet
            </p>

            <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
              Upload your first resume to get started.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {resumes.map((resume) => (
              <div
                key={resume.id}
                onClick={() => {setSelectedResume(resume);setAnalysis(null);}}
                className={`
                  cursor-pointer rounded-3xl transition
                  ${
                    selectedResume?.id === resume.id
                      ? "ring-2 ring-blue-500/30"
                      : ""
                  }
                `}
              >
                <ResumeCard
                  resume={resume}
                  selected={
                    selectedResume?.id === resume.id
                  }
                  onDelete={handleDelete}
                />
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Analysis */}
      {selectedResume && (
        <section>
          {analysisLoading && !analysis ? (
            <div className="rounded-3xl border border-zinc-200 bg-white p-8 text-center dark:border-zinc-800 dark:bg-zinc-900">
              <p className="text-sm text-zinc-500">
                Loading resume analysis...
              </p>
            </div>
          ) : analysis ? (
            <ResumeAnalysis analysis={analysis} />
          ) : (
            <div className="rounded-3xl border border-dashed border-zinc-300 bg-white p-8 text-center dark:border-zinc-700 dark:bg-zinc-900">
              <p className="text-sm font-semibold">
                Analysis unavailable
              </p>

              <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
                We could not load the analysis for this
                resume.
              </p>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

