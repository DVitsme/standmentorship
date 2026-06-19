import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { signOut } from "../login/actions";

export const metadata = { title: "Dashboard" };

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // RLS-scoped read: returns only THIS user's profile if policies work.
  const { data: profile, error } = await supabase
    .from("profiles")
    .select("id, role, full_name")
    .eq("id", user.id)
    .single();

  return (
    <div className="mx-auto flex min-h-dvh max-w-xl flex-col justify-center gap-5 px-6">
      <h1 className="font-display text-2xl font-extrabold">Dashboard</h1>
      <div className="rounded-lg border border-border p-4 text-sm">
        <p>
          <span className="text-muted-foreground">Signed in as</span>{" "}
          <strong>{user.email}</strong>
        </p>
        <p className="mt-1">
          <span className="text-muted-foreground">Role</span>{" "}
          <strong>{profile?.role ?? "—"}</strong>
        </p>
        {error ? (
          <p className="mt-2 text-destructive">RLS read error: {error.message}</p>
        ) : (
          <p className="mt-2 font-medium text-brand">
            ✓ Auth session + RLS-scoped profile read succeeded on this runtime.
          </p>
        )}
      </div>
      <form action={signOut}>
        <button className="rounded-md border border-input px-4 py-2 text-sm font-medium transition-colors hover:bg-secondary">
          Sign out
        </button>
      </form>
    </div>
  );
}
