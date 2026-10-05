import type { Page } from "../../types/navigation";

interface SidebarProps {
  currentPage: Page;
  onNavigate: (page: Page) => void;
  onLogout: () => void;
  onClose: () => void;
}

const navigation: {
  id: Page;
  label: string;
  icon: string;
}[] = [
  {
    id: "dashboard",
    label: "Overview",
    icon: "◉",
  },
  {
    id: "resume",
    label: "Resume",
    icon: "◍",
  },
  {
    id: "jobs",
    label: "Job Matches",
    icon: "◌",
  },
];

const careerNavigation: {
  id: Page;
  label: string;
  icon: string;
}[] = [
  {
    id: "settings",
    label: "Settings",
    icon: "⚙",
  },
];
export default function Sidebar({
  currentPage,
  onNavigate,
  onLogout,
  onClose,
}: SidebarProps) {
  return (
    <aside className="h-full w-64 border-r border-zinc-200/80 bg-white dark:border-zinc-800/80 dark:bg-zinc-950">

      <div className="flex h-full flex-col px-4 py-5">

        {/* Brand */}
        <div className="mb-8 flex items-center gap-3 px-2">

          <div className="relative flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-zinc-950 text-white shadow-sm dark:bg-white dark:text-zinc-950">
            <div className="absolute inset-0 bg-linear-to-br from-blue-500 via-violet-500 to-transparent opacity-80" />

            <span className="relative text-sm font-bold">
              ✦
            </span>
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-bold tracking-tight">
              Career Copilot
            </p>

            <p className="text-[11px] text-zinc-400">
              AI career OS
            </p>
          </div>

          {/* CLOSE */}
          <button
            type="button"
            onClick={onClose}
            aria-label="Close sidebar"
            className="
              flex h-8 w-8 shrink-0 items-center justify-center
              rounded-lg
              text-lg text-zinc-400
              transition
              hover:bg-zinc-100
              hover:text-zinc-900
              dark:hover:bg-zinc-800
              dark:hover:text-white
            "
          >
            ×
          </button>
        </div>

        {/* Workspace */}
        <div>
          <p className="mb-2 px-3 text-[10px] font-bold uppercase tracking-[0.16em] text-zinc-400">
            Workspace
          </p>

          <nav className="space-y-1">
            {navigation.map((item) => (
              <NavItem
                key={item.id}
                item={item}
                active={currentPage === item.id}
                onClick={() => onNavigate(item.id)}
              />
            ))}
          </nav>
        </div>

        {/* Career */}
        <div className="mt-7">
          <p className="mb-2 px-3 text-[10px] font-bold uppercase tracking-[0.16em] text-zinc-400">
            Career
          </p>

          <nav className="space-y-1">
            {careerNavigation.map((item) => (
              <NavItem
                key={item.id}
                item={item}
                active={currentPage === item.id}
                onClick={() => onNavigate(item.id)}
              />
            ))}
          </nav>
        </div>

        {/* Bottom */}
        <div className="relative z-50 mt-auto">

          {/* AI Copilot */}
          <button
            type="button"
            className="
              group relative w-full overflow-hidden
              rounded-2xl
              border border-blue-200/70
              bg-linear-to-br from-blue-50 via-white to-violet-50
              p-4 text-left
              transition
              hover:-translate-y-0.5
              hover:shadow-lg
              hover:shadow-blue-500/10
              dark:border-blue-900/50
              dark:from-blue-950/40
              dark:via-zinc-900
              dark:to-violet-950/30
            "
          >
            <div className="absolute -right-5 -top-5 h-20 w-20 rounded-full bg-blue-500/10 blur-2xl transition group-hover:bg-blue-500/20" />

            <div className="relative">
              <div className="flex items-center gap-2">
                <span className="text-blue-600 dark:text-blue-400">
                  ✦
                </span>

                <span className="text-xs font-bold">
                  AI Copilot
                </span>
              </div>

              <p className="mt-2 text-[11px] leading-4 text-zinc-500 dark:text-zinc-400">
                Ask about your resume, skills, or career direction.
              </p>

              <div className="mt-3 flex items-center text-[11px] font-semibold text-blue-600 dark:text-blue-400">
                Start conversation

                <span className="ml-auto transition group-hover:translate-x-1">
                  →
                </span>
              </div>
            </div>
          </button>

          {/* Profile */}
<div className="relative z-50 mt-4 flex items-center gap-3 border-t border-zinc-200 pt-4 dark:border-zinc-800">
  <button
    type="button"
    onClick={() => {
      console.log("MY PROFILE CLICKED");
      onNavigate("settings");
    }}
    className="relative z-50 flex min-w-0 flex-1 cursor-pointer items-center gap-3 rounded-xl p-2 text-left transition hover:bg-zinc-50 dark:hover:bg-zinc-900"
  >
    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-linear-to-br from-blue-500 to-violet-500 text-xs font-bold text-white">
      MK
    </div>

    <div className="min-w-0">
      <p className="truncate text-xs font-semibold">
        My Profile
      </p>

      <p className="truncate text-[11px] text-zinc-400">
        Career profile
      </p>
    </div>
  </button>

  <button
    type="button"
    onClick={onLogout}
    className="relative z-50 shrink-0 rounded-lg px-2 py-1 text-[11px] font-medium text-zinc-400 transition hover:bg-zinc-100 hover:text-red-500 dark:hover:bg-zinc-800"
  >
    Logout
  </button>
</div>
        </div>
      </div>
    </aside>
  );
}

function NavItem({
  item,
  active,
  onClick,
}: {
  item: {
    id: Page;
    label: string;
    icon: string;
  };
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        group flex w-full items-center gap-3
        rounded-xl px-3 py-2.5
        text-sm
        transition-all duration-200
        ${
          active
            ? "bg-zinc-100 font-semibold text-zinc-950 dark:bg-zinc-800/80 dark:text-white"
            : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-100"
        }
      `}
    >
      <span
        className={`
          flex h-7 w-7 items-center justify-center
          rounded-lg text-sm transition
          ${
            active
              ? "bg-white text-blue-600 shadow-sm dark:bg-zinc-700 dark:text-blue-400"
              : "text-zinc-400 group-hover:text-zinc-700 dark:group-hover:text-zinc-200"
          }
        `}
      >
        {item.icon}
      </span>

      <span>{item.label}</span>

      {active && (
        <span className="ml-auto h-1.5 w-1.5 rounded-full bg-blue-500" />
      )}
    </button>
  );
}