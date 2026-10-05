import { useState } from "react";

export interface SignupData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

interface SignupFormProps {
  onSubmit: (data: SignupData) => Promise<void>;
}

export default function SignupForm({
  onSubmit,
}: SignupFormProps) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError(null);

    if (
      !firstName.trim() ||
      !lastName.trim() ||
      !email.trim() ||
      !password
    ) {
      setError("Please complete all fields.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    try {
      setLoading(true);

      await onSubmit({
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        email: email.trim(),
        password,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to create your account."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 space-y-5">
      {/* Name */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label
            htmlFor="first-name"
            className="mb-2 block text-xs font-semibold text-zinc-700 dark:text-zinc-300"
          >
            First name
          </label>

          <input
            id="first-name"
            type="text"
            autoComplete="given-name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            // placeholder="John"
            disabled={loading}
            className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 text-sm outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white"
          />
        </div>

        <div>
          <label
            htmlFor="last-name"
            className="mb-2 block text-xs font-semibold text-zinc-700 dark:text-zinc-300"
          >
            Last name
          </label>

          <input
            id="last-name"
            type="text"
            autoComplete="family-name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            // placeholder="Doe"
            disabled={loading}
            className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 text-sm outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white"
          />
        </div>
      </div>

      {/* Email */}
      <div>
        <label
          htmlFor="signup-email"
          className="mb-2 block text-xs font-semibold text-zinc-700 dark:text-zinc-300"
        >
          Email address
        </label>

        <input
          id="signup-email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          disabled={loading}
          className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 text-sm outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white"
        />
      </div>

      {/* Password */}
      <div>
        <label
          htmlFor="signup-password"
          className="mb-2 block text-xs font-semibold text-zinc-700 dark:text-zinc-300"
        >
          Password
        </label>

        <div className="relative">
          <input
            id="signup-password"
            type={showPassword ? "text" : "password"}
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Create a password"
            disabled={loading}
            className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 pr-16 text-sm outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white"
          />

          <button
            type="button"
            onClick={() =>
              setShowPassword((value) => !value)
            }
            className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-medium text-zinc-400 hover:text-zinc-900 dark:hover:text-white"
          >
            {showPassword ? "Hide" : "Show"}
          </button>
        </div>

        <p className="mt-2 text-[11px] text-zinc-400">
          Use at least 8 characters.
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-xs font-medium text-red-700 dark:border-red-900/50 dark:bg-red-950/20 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="group flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-zinc-950 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-60 dark:bg-white dark:text-zinc-950"
      >
        {loading ? (
          <>
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            Creating account...
          </>
        ) : (
          <>
            Create account
            <span className="transition-transform group-hover:translate-x-1">
              →
            </span>
          </>
        )}
      </button>
    </form>
  );
}