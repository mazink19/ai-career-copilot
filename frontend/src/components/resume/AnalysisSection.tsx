interface AnalysisSectionProps {
  title: string;
  items: string[];
}

export default function AnalysisSection({
  title,
  items,
}: AnalysisSectionProps) {
  return (
    <div className="rounded-[20px] border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900">
      <h3 className="text-sm font-semibold">
        {title}
      </h3>

      {items.length > 0 ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {items.map((item) => (
            <span
              key={item}
              className="rounded-lg bg-zinc-100 px-3 py-2 text-xs font-medium text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300"
            >
              {item}
            </span>
          ))}
        </div>
      ) : (
        <p className="mt-4 text-sm text-zinc-500 dark:text-zinc-400">
          No information available.
        </p>
      )}
    </div>
  );
}