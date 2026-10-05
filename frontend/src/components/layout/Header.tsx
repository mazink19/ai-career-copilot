interface HeaderProps {
  title: string;
  darkMode: boolean;
  onToggleTheme: () => void;
  onOpenSidebar: () => void;
  firstName: string;
  lastName: string;
}

export default function Header({
  title,
  darkMode,
  onToggleTheme,
  onOpenSidebar,
  firstName,
  lastName
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-20 border-b border-zinc-200/70 bg-zinc-50/80 backdrop-blur-xl dark:border-zinc-800/70 dark:bg-zinc-950/80">
      <div className="flex h-18 items-center justify-between px-4 md:px-8">

        {/* Left */}
        <div className="flex items-center gap-4">
          <button
            onClick={onOpenSidebar}
            className="flex h-9 w-9 items-center justify-center rounded-xl border border-zinc-200 bg-white text-zinc-600 transition hover:border-zinc-300 hover:text-zinc-950 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:border-zinc-700 dark:hover:text-white"
            aria-label="Open navigation"
          >
            <span className="text-lg leading-none">
              ☰
            </span>
          </button>

          <div className="hidden h-5 w-px bg-zinc-200 sm:block dark:bg-zinc-800" />

          <div>
            <p className="text-sm font-semibold">
              {title}
            </p>

            <p className="hidden text-[11px] text-zinc-400 sm:block">
              AI Career Copilot
            </p>
          </div>
        </div>

        {/* Right */}
        <div className="flex items-center gap-2">

          {/* AI indicator */}
          <div className="hidden items-center gap-2 rounded-full border border-blue-200/70 bg-blue-50/70 px-3 py-1.5 text-[11px] font-medium text-blue-600 sm:flex dark:border-blue-900/50 dark:bg-blue-950/30 dark:text-blue-400">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-blue-500" />
            </span>

            AI ready
          </div>

          {/* Theme */}
          <button
            onClick={onToggleTheme}
            className="flex h-9 w-9 items-center justify-center rounded-xl border border-zinc-200 bg-white text-sm transition hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900"
            aria-label="Toggle theme"
          >
            {darkMode ? "☀" : "☾"}
          </button>

          {/* Divider */}
          <div className="mx-1 hidden h-6 w-px bg-zinc-200 md:block dark:bg-zinc-800" />

          {/* Avatar */}
          <button className="flex items-center gap-2 rounded-xl p-1 transition hover:bg-zinc-100 dark:hover:bg-zinc-900">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-linear-to-br from-blue-500 to-violet-500 text-[10px] font-bold text-white">
              {firstName.charAt(0).toUpperCase()}
             {lastName.charAt(0).toUpperCase()}
            </div>

            <span className="hidden text-xs font-medium md:block">
              {firstName}
            </span>
          </button>
        </div>
      </div>
    </header>
  );
}