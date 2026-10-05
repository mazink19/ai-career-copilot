import { useRef, useState } from "react";
import { uploadResume } from "../../services/api";

interface ResumeUploadProps {
  onUploaded?: () => void;
}

export default function ResumeUpload({
  onUploaded,
}: ResumeUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  function openFilePicker() {
  if (uploading) {
    return;
  }

  setError(null);
  setSuccess(null);
  fileInputRef.current?.click();
}

  async function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError(null);
    setSuccess(null);

    // Frontend validation
    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");
      event.target.value = "";
      return;
    }

    const maxSize = 5 * 1024 * 1024;

    if (file.size > maxSize) {
      setError("The file must be smaller than 5 MB.");
      event.target.value = "";
      return;
    }

    try {
      setUploading(true);
      const resume = await uploadResume(file);

      setSuccess(`${resume.file_name} uploaded successfully.`);

      onUploaded?.();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to upload resume."
      );
    } finally {
      setUploading(false);

      // Allows selecting the same file again.
      event.target.value = "";
    }
  }

  return (
   <div
  className={`group relative overflow-hidden rounded-3xl border border-dashed bg-white p-8 transition dark:bg-zinc-900 ${
    uploading
      ? "cursor-not-allowed border-zinc-300 opacity-80 dark:border-zinc-700"
      : "border-zinc-300 hover:border-blue-400 hover:bg-blue-50/30 dark:border-zinc-700 dark:hover:border-blue-500 dark:hover:bg-blue-950/10"
  }`}
>
  <input
    ref={fileInputRef}
    type="file"
    accept="application/pdf"
    onChange={handleFileChange}
    className="hidden"
  />

      <div className="flex flex-col items-center justify-center text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-zinc-100 text-xl transition group-hover:scale-105 dark:bg-zinc-800">
          {uploading ? (
            <span className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-900 dark:border-zinc-600 dark:border-t-white" />
          ) : ("↑")}
        </div>

        <h3 className="mt-5 text-lg font-semibold">
          {uploading
            ? "Uploading your resume..."
            : "Upload your resume"}
        </h3>

        <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-500 dark:text-zinc-400">
          Upload a PDF and let Career Copilot analyze your
          experience, skills, education, and projects.
        </p>

        <button
          type="button"
          onClick={openFilePicker}
          disabled={uploading}
          className="mt-6 rounded-xl bg-zinc-950 px-5 py-3 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-50 dark:bg-white dark:text-zinc-950"
        >
          {uploading ? "Uploading..." : "Choose PDF"}
        </button>

        <p className="mt-3 text-[11px] text-zinc-400">
          PDF files · Maximum 5 MB
        </p>

        {success && (
          <div className="mt-5 rounded-xl bg-emerald-50 px-4 py-3 text-xs font-medium text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400">
            {success}
          </div>
        )}

        {error && (
          <div className="mt-5 rounded-xl bg-red-50 px-4 py-3 text-xs font-medium text-red-700 dark:bg-red-950/30 dark:text-red-400">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}