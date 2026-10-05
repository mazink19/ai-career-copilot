import { useEffect, useState } from "react";

import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Resume from "./pages/Resume";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Jobs from "./pages/Jobs";
import Settings from "./pages/Settings";

import type { Page } from "./types/navigation";
import type { LoginResponse } from "./types/auth";

import {
  getCurrentUser,
  isAuthenticated,
} from "./services/api";

type AuthPage = "login" | "signup";

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });

  const [page, setPage] = useState<Page>("dashboard");

  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [authenticated, setAuthenticated] = useState(
    isAuthenticated()
  );

  const [authPage, setAuthPage] =
    useState<AuthPage>("login");

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  // Dark mode
  useEffect(() => {
    document.documentElement.classList.toggle(
      "dark",
      darkMode
    );

    localStorage.setItem(
      "theme",
      darkMode ? "dark" : "light"
    );
  }, [darkMode]);

  // Load current user
  useEffect(() => {
    if (!authenticated) return;

    async function loadUser() {
      try {
        const user = await getCurrentUser();

        setFirstName(user.first_name);
        setLastName(user.last_name);
      } catch {
        setFirstName("");
        setLastName("");
      }
    }

    loadUser();
  }, [authenticated]);

  // Login
  function handleLogin(response: LoginResponse) {
    localStorage.setItem(
      "access_token",
      response.access_token
    );

    setAuthenticated(true);
  }

  // Logout
  function handleLogout() {
    localStorage.removeItem("access_token");

    setAuthenticated(false);
    setAuthPage("login");
    setPage("dashboard");

    setFirstName("");
    setLastName("");
  }

  // Handle automatic logout
  useEffect(() => {
    function handleAuthLogout() {
      setAuthenticated(false);
      setAuthPage("login");
      setPage("dashboard");

      setFirstName("");
      setLastName("");
    }

    window.addEventListener(
      "auth:logout",
      handleAuthLogout
    );

    return () => {
      window.removeEventListener(
        "auth:logout",
        handleAuthLogout
      );
    };
  }, []);

  // Check token expiration
  useEffect(() => {
    if (!authenticated) {
      return;
    }

    const interval = window.setInterval(() => {
      const valid = isAuthenticated();

      console.log("Auth check:", valid);

      if (!valid) {
        setAuthenticated(false);
        setAuthPage("login");
        setPage("dashboard");

        setFirstName("");
        setLastName("");
      }
    }, 5000);

    return () => {
      window.clearInterval(interval);
    };
  }, [authenticated]);

  // Authentication pages
  if (!authenticated) {
    if (authPage === "signup") {
      return (
        <Signup
          onSignupSuccess={() => setAuthPage("login")}
          onLoginClick={() => setAuthPage("login")}
        />
      );
    }

    return (
      <Login
        onLoginSuccess={handleLogin}
        onSignupClick={() => setAuthPage("signup")}
      />
    );
  }

  // Main application
  return (
    <AppLayout
      currentPage={page}
      darkMode={darkMode}
      sidebarOpen={sidebarOpen}
      firstName={firstName}
      lastName={lastName}
      onNavigate={setPage}
      onToggleTheme={() =>
        setDarkMode((value) => !value)
      }
      onOpenSidebar={() => setSidebarOpen(true)}
      onCloseSidebar={() =>
        setSidebarOpen(false)
      }
      onLogout={handleLogout}
    >
      {page === "dashboard" && (
        <Dashboard onNavigate={setPage} />
      )}

      {page === "resume" && <Resume />}

      {page === "jobs" && <Jobs />}

      {page === "settings" && (
      <Settings
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onProfileUpdated={(firstName, lastName) => {
        setFirstName(firstName);
        setLastName(lastName);
        }}
      />
      )}
    </AppLayout>
  );
}

export default App;