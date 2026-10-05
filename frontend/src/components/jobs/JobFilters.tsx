interface JobFiltersProps {
  location: string;
  match: string;
  onLocationChange: (value: string) => void;
  onMatchChange: (value: string) => void;
}

export default function JobFilters({
  location,
  match,
  onLocationChange,
  onMatchChange,
}: JobFiltersProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row">
      <select
        value={location}
        onChange={(e) => onLocationChange(e.target.value)}
        className="
          h-12 rounded-2xl
          border border-zinc-200
          bg-white px-4
          text-sm text-zinc-700
          outline-none
          focus:border-blue-400
          focus:ring-4 focus:ring-blue-500/10
          dark:border-zinc-800
          dark:bg-zinc-900
          dark:text-zinc-300
        "
      >
        <option value="all">All locations</option>
        <option value="remote">Remote</option>
        <option value="hybrid">Hybrid</option>
        <option value="onsite">On-site</option>
      </select>

      <select
        value={match}
        onChange={(e) => onMatchChange(e.target.value)}
        className="
          h-12 rounded-2xl
          border border-zinc-200
          bg-white px-4
          text-sm text-zinc-700
          outline-none
          focus:border-blue-400
          focus:ring-4 focus:ring-blue-500/10
          dark:border-zinc-800
          dark:bg-zinc-900
          dark:text-zinc-300
        "
      >
        <option value="all">Any match</option>
        <option value="90">90%+ match</option>
        <option value="80">80%+ match</option>
        <option value="70">70%+ match</option>
      </select>
    </div>
  );
}