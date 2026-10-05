import type { Resume } from "../../types/resume";

interface ResumeCardProps {
  resume: Resume;
  selected?: boolean;
  onDelete?: (resume: Resume) => void;
}

export default function ResumeCard({
  resume,
  selected = false,
  onDelete,
}: ResumeCardProps) {
  const uploadedDate = new Date(
    resume.uploaded_at
  ).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  return (
    <div
      className={`
        rounded-3xl border bg-white p-6 transition-all
        dark:bg-zinc-900
        ${
          selected
            ? "border-blue-500/50 shadow-lg shadow-blue-500/5"
            : "border-zinc-200 hover:border-zinc-300 hover:shadow-md dark:border-zinc-800 dark:hover:border-zinc-700"
        }
      `}
    >
      <div className="flex items-center gap-4">
        {/* PDF icon */}
        <div
          className="
            flex h-12 w-12 shrink-0 items-center
            justify-center rounded-xl
            bg-red-50 text-xs font-bold text-red-500
            dark:bg-red-950/30 dark:text-red-400
          "
        >
          PDF
        </div>

        {/* File information */}
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold">
            {resume.file_name}
          </p>

          <p className="mt-1 text-xs text-zinc-400">
            Uploaded {uploadedDate}
          </p>
        </div>

        {/* Selected indicator */}
        {selected && (
          <div className="flex items-center gap-2 text-xs font-medium text-blue-600 dark:text-blue-400">
            <span className="h-2 w-2 rounded-full bg-blue-500" />
            Selected
          </div>
        )}
      </div>

      {/* Bottom actions */}
      <div className="mt-5 flex items-center justify-between border-t border-zinc-100 pt-5 dark:border-zinc-800">
        <div className="flex items-center gap-2">
           <span
           className={`
            h-2 w-2 rounded-full
            ${getStatusColor(resume.analysis_status)}
            ${resume.analysis_status === "analyzing" ? "animate-pulse" : ""}
            `}
            />

          <span className="text-xs font-medium text-zinc-500">
            {getStatusLabel(resume.analysis_status)}
  </span>
        </div>

        <div className="flex items-center gap-4">
          {selected && (
            <span className="text-xs font-semibold text-blue-600 dark:text-blue-400">
              Viewing analysis
            </span>
          )}

          {onDelete && (
            <button
              type="button"
              onClick={(event) => {
                event.stopPropagation();
                onDelete(resume);
              }}
              className="
                text-xs font-medium text-red-500
                transition hover:text-red-600
                dark:text-red-400 dark:hover:text-red-300
              "
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function getStatusLabel(
  status: Resume["analysis_status"]
) {
  switch (status) {
    case "completed":
      return "Analysis completed";

    case "analyzing":
      return "Analysis in progress";

    case "pending":
      return "Analysis pending";

    case "failed":
      return "Analysis failed";

    default:
      return "No analysis yet";
  }
}

function getStatusColor(
  status: Resume["analysis_status"]
) {
  switch (status) {
  case "completed":
    return "bg-emerald-500";

  case "analyzing":
    return "bg-blue-500";

  case "pending":
    return "bg-amber-500";

  case "failed":
    return "bg-red-500";

  default:
    return "bg-zinc-400";
  }
}