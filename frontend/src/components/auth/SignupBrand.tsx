export default function SignupBrand() {
  return (
    <section className="relative hidden min-h-screen overflow-hidden bg-zinc-950 text-white lg:flex lg:w-[52%]">
      <div className="absolute inset-0">
        <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="absolute -bottom-40 -right-20 h-112 w-md rounded-full bg-indigo-500/10 blur-3xl" />

        <div className="absolute inset-0 opacity-[0.035] bg-[linear-gradient(rgba(255,255,255,1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,1)_1px,transparent_1px)] bg-size-[64px_64px]" />
      </div>

      <div className="relative z-10 flex w-full flex-col justify-between p-10 xl:p-14">
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

        <div className="max-w-xl">
          <p className="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-blue-400">
            Start with your potential
          </p>

          <h1 className="text-5xl font-semibold leading-[1.05] tracking-[-0.045em] xl:text-6xl">
            Build a career
            <br />
            around what
            <br />
            <span className="text-zinc-500">you can do.</span>
          </h1>

          <p className="mt-7 max-w-lg text-base leading-7 text-zinc-400">
            Create your profile once. Career Copilot helps
            you understand your experience and turn it into
            better opportunities.
          </p>

          <div className="mt-12 grid max-w-md grid-cols-3 gap-3">
            <FeatureCard
              number="01"
              title="Analyze"
              description="Understand your profile"
            />

            <FeatureCard
              number="02"
              title="Improve"
              description="Find your gaps"
            />

            <FeatureCard
              number="03"
              title="Discover"
              description="Find better matches"
            />
          </div>
        </div>

        <p className="text-xs text-zinc-600">
          Your next opportunity starts here.
        </p>
      </div>
    </section>
  );
}

function FeatureCard({
  number,
  title,
  description,
}: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/4.5 p-4 backdrop-blur-sm">
      <p className="text-[10px] font-semibold text-zinc-600">
        {number}
      </p>

      <p className="mt-6 text-sm font-semibold">
        {title}
      </p>

      <p className="mt-1 text-[10px] leading-4 text-zinc-500">
        {description}
      </p>
    </div>
  );
}