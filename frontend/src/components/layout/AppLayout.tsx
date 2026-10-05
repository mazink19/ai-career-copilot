import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";
import type { Page } from "../../types/navigation";

interface AppLayoutProps {
  children: ReactNode;
  currentPage: Page;
  darkMode: boolean;
  sidebarOpen: boolean;
  firstName: string;
  lastName: string;
  onNavigate: (page: Page) => void;
  onToggleTheme: () => void;
  onOpenSidebar: () => void;
  onCloseSidebar: () => void;
  onLogout: () => void;
}

export default function AppLayout({
  children,
  currentPage,
  darkMode,
  sidebarOpen,
  firstName,
  lastName,
  onNavigate,
  onToggleTheme,
  onOpenSidebar,
  onCloseSidebar,
  onLogout,
}: AppLayoutProps) {
  const titles: Record<Page, string> = {
    dashboard: "Dashboard",
    resume: "Resume",
    jobs: "Jobs",
    settings: "Settings",
  };

  const handleNavigate = (page: Page) => {
    onNavigate(page);
    onCloseSidebar();
  };

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="min-h-screen bg-zinc-50 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">

        {/* Background overlay */}
        {sidebarOpen && (
          <button
            type="button"
            aria-label="Close sidebar"
            onClick={onCloseSidebar}
            className="
              fixed inset-0 z-30
              bg-black/40
              backdrop-blur-[2px]
            "
          />
        )}

        {/* Sidebar */}
        <aside
          className={`
            fixed inset-y-0 left-0 z-100
            w-64
            transform
            transition-transform duration-300 ease-in-out
            ${
              sidebarOpen
                ? "translate-x-0"
                : "-translate-x-full"
            }
          `}
        >
          <Sidebar
            currentPage={currentPage}
            onNavigate={handleNavigate}
            onLogout={onLogout}
            onClose={onCloseSidebar}
          />
        </aside>

        {/* Main application */}
        <div
          className={`
            min-h-screen
            transition-[padding] duration-300 ease-in-out
            ${
              sidebarOpen
                ? "lg:pl-64"
                : "lg:pl-0"
            }
          `}
        >
          <Header
            title={titles[currentPage]}
            darkMode={darkMode}
            firstName={firstName}
            lastName={lastName}
            onToggleTheme={onToggleTheme}
            onOpenSidebar={onOpenSidebar}
          />

          <main className="mx-auto max-w-7xl px-4 py-8 md:px-8">
            {children}
          </main>
        </div>

      </div>
    </div>
  );
}