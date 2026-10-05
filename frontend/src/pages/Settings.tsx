import { useEffect, useState } from "react";
import type { Dispatch, SetStateAction } from "react";
import {
  getCurrentUser,
  updateProfile,
} from "../services/api";
import type { User } from "../types/auth";

interface SettingsProps {
  darkMode: boolean;
  setDarkMode: Dispatch<SetStateAction<boolean>>;
  onProfileUpdated: (firstName: string, lastName: string) => void;
}
export default function Settings({
  darkMode,
  setDarkMode,
  onProfileUpdated,
}: SettingsProps)  {
  const [user, setUser] = useState<User | null>(null);

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function loadProfile() {
      try {
        setLoading(true);
        setError(null);

        const data = await getCurrentUser();

        setUser(data);
        setFirstName(data.first_name);
        setLastName(data.last_name);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load profile."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    try {
      setSaving(true);
      setError(null);
      setSuccess(null);

      const updatedUser = await updateProfile(
        firstName,
        lastName
      );

      setUser(updatedUser);
      setFirstName(updatedUser.first_name);
      setLastName(updatedUser.last_name);
      onProfileUpdated(updatedUser.first_name, updatedUser.last_name);
      setSuccess("Profile updated successfully.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to update profile."
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold tracking-tight">
          Settings
        </h1>

        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          Loading your settings...
        </p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="mx-auto max-w-4xl">
        <h1 className="text-3xl font-bold tracking-tight">
          Settings
        </h1>

        <p className="mt-4 text-sm text-red-500">
          {error ?? "Unable to load profile."}
        </p>
      </div>
    );
  }

  const initials =
    `${user.first_name[0] ?? ""}${user.last_name[0] ?? ""}`.toUpperCase();

  return (
    <div className="mx-auto max-w-4xl">
      {/* Page header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Settings
        </h1>

        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          Manage your Career Copilot preferences and account.
        </p>
      </div>

      {/* Profile */}
      <section className="mb-6 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-950">
        <div className="mb-6">
          <h2 className="text-base font-semibold">
            Profile
          </h2>

          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Manage your personal information.
          </p>
        </div>

        {/* Profile header */}
        <div className="mb-6 flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-blue-500 to-violet-500 text-lg font-bold text-white">
            {initials}
          </div>

          <div>
            <h3 className="text-xl font-semibold">
              {user.first_name} {user.last_name}
            </h3>

            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
              {user.email}
            </p>
          </div>
        </div>

        {/* Personal information */}
        <div className="border-t border-zinc-100 pt-6 dark:border-zinc-800">
          <h3 className="text-sm font-semibold">
            Personal Information
          </h3>

          <form onSubmit={handleSubmit}>
            <div className="mt-5 grid gap-5 sm:grid-cols-2">
              <div>
                <label className="mb-2 block text-sm font-medium">
                  First name
                </label>

                <input
                  value={firstName}
                  onChange={(event) =>
                    setFirstName(event.target.value)
                  }
                  required
                  className="w-full rounded-xl border border-zinc-200 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 dark:border-zinc-700 dark:bg-zinc-900"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium">
                  Last name
                </label>

                <input
                  value={lastName}
                  onChange={(event) =>
                    setLastName(event.target.value)
                  }
                  required
                  className="w-full rounded-xl border border-zinc-200 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-blue-500 dark:border-zinc-700 dark:bg-zinc-900"
                />
              </div>
            </div>

            <div className="mt-5">
              <label className="mb-2 block text-sm font-medium">
                Email
              </label>

              <input
                value={user.email}
                disabled
                className="w-full cursor-not-allowed rounded-xl border border-zinc-200 bg-zinc-50 px-4 py-2.5 text-sm text-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-400"
              />

              <p className="mt-2 text-xs text-zinc-400">
                Email address cannot be changed here.
              </p>
            </div>

            {error && (
              <p className="mt-5 text-sm text-red-500">
                {error}
              </p>
            )}

            {success && (
              <p className="mt-5 text-sm text-green-600 dark:text-green-400">
                {success}
              </p>
            )}

            <div className="mt-6 flex justify-end">
              <button
                type="submit"
                disabled={saving}
                className="rounded-xl bg-zinc-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-white dark:text-zinc-950 dark:hover:bg-zinc-200"
              >
                {saving ? "Saving..." : "Save changes"}
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Appearance */}
      <section className="mb-6 rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-950">
        <div className="mb-6">
          <h2 className="text-base font-semibold">
            Appearance
          </h2>

          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Choose how Career Copilot looks.
          </p>
        </div>

        <div className="flex items-center justify-between border-t border-zinc-100 pt-5 dark:border-zinc-800">
          <div>
            <p className="text-sm font-medium">
              Dark mode
            </p>

            <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
              Use a darker appearance throughout the application.
            </p>
          </div>

          <button
            type="button"
            onClick={() => setDarkMode((value) => !value)}
            aria-label="Toggle dark mode"
            className={`relative h-6 w-11 rounded-full transition ${
              darkMode
                ? "bg-blue-600"
                : "bg-zinc-300 dark:bg-zinc-700"
            }`}
          >
            <span
              className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
                darkMode ? "left-6" : "left-1"
              }`}
            />
          </button>
        </div>
      </section>
    </div>
  );
}