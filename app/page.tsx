import Link from "next/link";

export default function Home() {
  return (
    <div className="mx-auto flex min-h-dvh max-w-2xl flex-col items-center justify-center gap-6 px-6 text-center">
      <p className="font-display text-sm font-bold uppercase tracking-[0.2em] text-brand">
        S.T.A.N.D Mentorship
      </p>
      <h1 className="font-display text-4xl font-extrabold tracking-tight sm:text-5xl">
        Stepping Towards A New Destiny
      </h1>
      <p className="max-w-prose text-muted-foreground">
        Free youth leadership, life-skills, and skilled-trades mentorship in
        Baltimore &amp; Howard County. The enrollment portal is being built.
      </p>
      <Link
        href="/login"
        className="rounded-md bg-brand px-5 py-2.5 font-medium text-brand-foreground transition-colors hover:bg-brand-deep"
      >
        Parent login
      </Link>
    </div>
  );
}
