interface JobSearchProps {
  search: string;
  onSearchChange: (value: string) => void;
}

export default function JobSearch({
  search,
  onSearchChange,
}: JobSearchProps) {
  return (
    <div className="relative">
      <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400">
        ⌕
      </span>

      <input
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        placeholder="Search jobs, companies, or skills..."
        className="
          h-12 w-full rounded-2xl
          border border-zinc-200
          bg-white pl-11 pr-4
          text-sm outline-none
          transition
          placeholder:text-zinc-400
          focus:border-blue-400
          focus:ring-4 focus:ring-blue-500/10
          dark:border-zinc-800
          dark:bg-zinc-900
          dark:text-white
        "
      />
    </div>
  );
}