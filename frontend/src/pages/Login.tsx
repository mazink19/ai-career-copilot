import LoginBrand from "../components/auth/LoginBrand";
import LoginForm from "../components/auth/LoginForm";
import type { LoginRequest } from "../types/auth";
import type { LoginResponse } from "../types/auth";

interface LoginProps {
  onLoginSuccess: (response: LoginResponse) => void;
  onSignupClick?: () => void;
}

export default function Login({
  onLoginSuccess, onSignupClick
}: LoginProps) {
  async function handleLogin(
    credentials: LoginRequest
  ) {
    const response = await fetch(
      "http://localhost:8000/auth/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      }
    );

    if (!response.ok) {
      let message = "Invalid email or password.";

      try {
        const data = await response.json();

        if (typeof data.detail === "string") {
          message = data.detail;
        }
      } catch {
        // Ignore invalid JSON response.
      }

      throw new Error(message);
    }

    const data: LoginResponse = await response.json();

    localStorage.setItem(
      "access_token",
      data.access_token
    );

    onLoginSuccess(data);
  }

  return (
    <main className="min-h-screen bg-zinc-50 text-zinc-950 dark:bg-zinc-950 dark:text-white">
      <div className="flex min-h-screen">
        {/* Brand panel */}
        <LoginBrand />

        {/* Login panel */}
        <section className="flex min-h-screen flex-1 items-center justify-center px-6 py-12 sm:px-10 lg:px-14 xl:px-20">
          <div className="w-full max-w-md">
            {/* Mobile logo */}
            <div className="mb-12 flex items-center gap-3 lg:hidden">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-950 text-sm font-bold text-white dark:bg-white dark:text-zinc-950">
                C
              </div>

              <div>
                <p className="text-sm font-semibold">
                  Career Copilot
                </p>

                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-400">
                  AI career intelligence
                </p>
              </div>
            </div>

            {/* Heading */}
            <div>
              <p className="text-xs font-semibold  tracking-[0.16em] text-blue-600 dark:text-blue-400">
                Don't ever let somebody tell you you can't do something. Not even me. All right? You got a dream, you gotta protect it. 
              </p>

              <h2 className="mt-3 text-3xl font-semibold tracking-[-0.035em] sm:text-4xl">
                Continue your journey.
              </h2>

              <p className="mt-3 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
                Sign in to access your resume insights,
                career profile, and matched opportunities.
              </p>
            </div>

            <LoginForm onSubmit={handleLogin} />

            {/* Divider */}
            <div className="my-7 flex items-center gap-4">
              <div className="h-px flex-1 bg-zinc-200 dark:bg-zinc-800" />

              <span className="text-[10px] font-medium uppercase tracking-[0.14em] text-zinc-400">
                Secure access
              </span>

              <div className="h-px flex-1 bg-zinc-200 dark:bg-zinc-800" />
            </div>

            <p className="text-center text-xs text-zinc-400">
              Your career data is protected by authenticated
              access.
            </p>

            {/* Sign up */}
            <p className="mt-8 text-center text-sm text-zinc-500 dark:text-zinc-400">
              Don't have an account?{" "}
              <button
                type="button"
                onClick={onSignupClick}
                className="font-semibold text-zinc-900 hover:underline dark:text-white"
              >
                Create one
              </button>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}