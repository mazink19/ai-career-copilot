export default function LoginBrand() {
  return (
    <section className="relative hidden min-h-screen overflow-hidden bg-zinc-950 text-white lg:flex lg:w-[52%]">
      {/* Decorative background */}
      <div className="absolute inset-0">
        <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="absolute -bottom-40 -right-20 h-112 w-md rounded-full bg-indigo-500/10 blur-3xl" />

        <div className="absolute inset-0 opacity-[0.035] bg-[linear-gradient(rgba(255,255,255,1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,1)_1px,transparent_1px)] bg-size-[64px_64px]" />
      </div>

      <div className="relative z-10 flex w-full flex-col justify-between p-10 xl:p-14">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-sm font-bold text-zinc-950">
            C
          </div>

          <div>
            <p className="text-sm font-semibold tracking-tight">
              Career Copilot
            </p>

            <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-500">
              AI career intelligence
            </p>
          </div>
        </div>

        {/* Main message */}
        <div className="max-w-xl">
          <p className="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-blue-400">
            Your career, understood
          </p>

          <h1 className="text-5xl font-semibold leading-[1.05] tracking-[-0.045em] xl:text-6xl">
            Turn your experience
            <br />
            into your next
            <br />
            <span className="text-zinc-500">opportunity.</span>
          </h1>

          <p className="mt-7 max-w-lg text-base leading-7 text-zinc-400">
            Analyze your resume, understand your strengths,
            and discover opportunities that actually match
            your profile.
          </p>

          {/* Career snapshot */}
          <div className="mt-12 max-w-md rounded-3xl border border-white/10 bg-white/4.5 p-5 backdrop-blur-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-zinc-500">
                  Career readiness
                </p>

                <p className="mt-1 text-sm font-medium">
                  Strong foundation
                </p>
              </div>

              <div className="text-right">
                <p className="text-2xl font-semibold">
                  78%
                </p>

                <p className="text-[10px] text-emerald-400">
                  +12% this month
                </p>
              </div>
            </div>

            <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-white/10">
              <div className="h-full w-[78%] rounded-full bg-white" />
            </div>

            <div className="mt-5 grid grid-cols-3 divide-x divide-white/10">
              <div className="px-3 first:pl-0">
                <p className="text-lg font-semibold">
                  84
                </p>

                <p className="mt-1 text-[10px] text-zinc-500">
                  Resume
                </p>
              </div>

              <div className="px-4">
                <p className="text-lg font-semibold">
                  12
                </p>

                <p className="mt-1 text-[10px] text-zinc-500">
                  Matches
                </p>
              </div>

              <div className="px-4 last:pr-0">
                <p className="text-lg font-semibold">
                  7
                </p>

                <p className="mt-1 text-[10px] text-zinc-500">
                  Skills
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-xs text-zinc-600">
          Build a career around what you can do.
        </p>
      </div>
    </section>
  );
}