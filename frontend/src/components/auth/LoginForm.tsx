import { useState } from "react";
import type { LoginRequest } from "../../types/auth";

interface LoginFormProps {
  onSubmit: (credentials: LoginRequest) => Promise<void>;
}

export default function LoginForm({
  onSubmit,
}: LoginFormProps) {
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

    if (!email.trim() || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      await onSubmit({
        email: email.trim(),
        password,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to sign in."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 space-y-5">
      {/* Email */}
      <div>
        <label
          htmlFor="email"
          className="mb-2 block text-xs font-semibold text-zinc-700 dark:text-zinc-300"
        >
          Email address
        </label>

        <input
          id="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="you@example.com"
          disabled={loading}
          className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white dark:focus:ring-white/5"
        />
      </div>

      {/* Password */}
      <div>
        <div className="mb-2 flex items-center justify-between">
          <label
            htmlFor="password"
            className="text-xs font-semibold text-zinc-700 dark:text-zinc-300"
          >
            Password
          </label>

          <button
            type="button"
            className="text-xs font-medium text-zinc-400 transition hover:text-zinc-900 dark:hover:text-white"
          >
            Forgot password?
          </button>
        </div>

        <div className="relative">
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            placeholder="Enter your password"
            disabled={loading}
            className="h-12 w-full rounded-xl border border-zinc-200 bg-white px-4 pr-12 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 focus:border-zinc-950 focus:ring-4 focus:ring-zinc-950/5 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:text-white dark:focus:border-white dark:focus:ring-white/5"
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
            Signing in...
          </>
        ) : (
          <>
            Sign in

            <span className="transition-transform group-hover:translate-x-1">
              →
            </span>
          </>
        )}
      </button>
    </form>
  );
}