import { signIn, signUp } from "./actions";

export const metadata = { title: "Parent sign in" };

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; message?: string }>;
}) {
  const { error, message } = await searchParams;

  return (
    <div className="mx-auto flex min-h-dvh max-w-sm flex-col justify-center gap-6 px-6">
      <div className="text-center">
        <p className="font-display text-xs font-bold uppercase tracking-[0.2em] text-brand">
          S.T.A.N.D Mentorship
        </p>
        <h1 className="mt-2 font-display text-2xl font-extrabold">
          Parent sign in
        </h1>
      </div>

      {error && (
        <p
          role="alert"
          className="rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive"
        >
          {error}
        </p>
      )}
      {message && (
        <p className="rounded-md bg-secondary px-3 py-2 text-sm text-muted-foreground">
          {message}
        </p>
      )}

      <form className="flex flex-col gap-3">
        <label className="flex flex-col gap-1 text-sm font-medium">
          Email
          <input
            name="email"
            type="email"
            required
            autoComplete="email"
            className="rounded-md border border-input bg-background px-3 py-2 text-base"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm font-medium">
          Password
          <input
            name="password"
            type="password"
            required
            minLength={8}
            autoComplete="current-password"
            className="rounded-md border border-input bg-background px-3 py-2 text-base"
          />
        </label>
        <button
          formAction={signIn}
          className="mt-2 rounded-md bg-brand px-4 py-2.5 font-medium text-brand-foreground transition-colors hover:bg-brand-deep"
        >
          Sign in
        </button>
        <button
          formAction={signUp}
          className="rounded-md border border-input px-4 py-2.5 font-medium transition-colors hover:bg-secondary"
        >
          Create account
        </button>
      </form>

      <p className="text-center text-xs text-muted-foreground">
        Smoke test — parent accounts only (v1).
      </p>
    </div>
  );
}
