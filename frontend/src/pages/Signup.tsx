import SignupBrand from "../components/auth/SignupBrand";
import SignupForm, {
  type SignupData,
} from "../components/auth/SignupForm";

interface SignupProps {
  onSignupSuccess: () => void;
  onLoginClick: () => void;
}

function Signup({
  onSignupSuccess,
  onLoginClick,
}: SignupProps) {
  async function handleSignup(data: SignupData) {
    const response = await fetch(
      "http://localhost:8000/auth/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    if (!response.ok) {
      let message = "Unable to create your account.";

      try {
        const result = await response.json();

        if (typeof result.detail === "string") {
          message = result.detail;
        }
      } catch {
        // Ignore invalid JSON responses.
      }

      throw new Error(message);
    }

    onSignupSuccess();
  }

  return (
    <main className="min-h-screen bg-zinc-50 text-zinc-950 dark:bg-zinc-950 dark:text-white">
      <div className="flex min-h-screen">
        <SignupBrand />

        <section className="flex min-h-screen flex-1 items-center justify-center px-6 py-10 sm:px-10 lg:px-14 xl:px-20">
          <div className="w-full max-w-md">

            {/* Mobile logo */}
            <div className="mb-10 flex items-center gap-3 lg:hidden">
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
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-blue-600 dark:text-blue-400">
                Get started
              </p>

              <h2 className="mt-3 text-3xl font-semibold tracking-[-0.035em] sm:text-4xl">
                Build your career profile.
              </h2>

              <p className="mt-3 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
                Create your account and let Career Copilot
                turn your experience into actionable career
                insights.
              </p>
            </div>

            {/* Form */}
            <SignupForm onSubmit={handleSignup} />

            {/* Login link */}
            <p className="mt-7 text-center text-sm text-zinc-500 dark:text-zinc-400">
              Already have an account?{" "}
              <button
                type="button"
                onClick={onLoginClick}
                className="font-semibold text-zinc-900 hover:underline dark:text-white"
              >
                Sign in
              </button>
            </p>

            <p className="mt-6 text-center text-[11px] leading-5 text-zinc-400">
              By creating an account, you can securely
              access your career profile and resume analysis.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}

export default Signup;