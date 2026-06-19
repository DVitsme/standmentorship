# P0 Setup — Supabase project + live auth/RLS validation

A one-time runbook to stand up the Supabase backend and prove the foundation works end-to-end (auth + Row-Level Security) on both Node and the Cloudflare workerd runtime. Architecture context: `docs/app-architecture.md`.

**State going in:** the app is scaffolded, dependencies are installed, and it builds for Next **and** Cloudflare (`pnpm build`, `pnpm exec opennextjs-cloudflare build`). What's missing is a Supabase project to point it at.

---

## 1. Create a free Supabase project
1. Go to **supabase.com** → **New project**.
2. Name it (e.g., `standmentorship`), set a **database password** (save it — needed for the CLI), and pick a region near Maryland: **East US (North Virginia)**.
3. Wait ~2 min for it to provision.

## 2. Grab the API keys
**Project Settings → API**, copy three values:
| Value | Env var | Sensitivity |
|---|---|---|
| Project URL (`https://<ref>.supabase.co`) | `NEXT_PUBLIC_SUPABASE_URL` | public |
| `anon` `public` key | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | public (RLS protects data) |
| `service_role` key | `SUPABASE_SERVICE_ROLE_KEY` | **SECRET — server only** |

## 3. Fill the env files (gitignored)
Both `.env.local` (for `pnpm dev`) and `.dev.vars` (for `pnpm preview` / workerd) already exist from the template. Put the **same three values in both**:
```
NEXT_PUBLIC_SUPABASE_URL=https://<ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon key>
SUPABASE_SERVICE_ROLE_KEY=<service_role key>
```
- `RESEND_API_KEY`, `TURNSTILE_*`, Stripe — **not needed for P0** (password sign-in needs no email). Leave blank for now.
- ⚠️ Never commit these files (they're in `.gitignore`). The `service_role` key bypasses RLS — keep it out of chat and the client bundle.

## 4. Apply the schema + RLS (`supabase/migrations/0001_init.sql`)
**Option A — SQL Editor (fastest):** open the Supabase dashboard → **SQL Editor** → paste the entire contents of `supabase/migrations/0001_init.sql` → **Run**. You should see the tables under **Table Editor** and "RLS enabled" on each.

**Option B — Supabase CLI (repeatable, recommended long-term):**
```bash
pnpm dlx supabase login                       # opens a browser for an access token
pnpm dlx supabase link --project-ref <ref>    # <ref> = the subdomain in your project URL
pnpm dlx supabase db push                      # applies supabase/migrations/* (asks for the DB password)
pnpm run db:types                              # optional: generate lib/supabase/database.types.ts
```

## 5. Auth settings for the smoke test
Dashboard → **Authentication → Sign In / Providers → Email**: toggle **"Confirm email" OFF** so a new account is usable immediately (naming may vary slightly by Supabase version). Re-enable it (and wire **Resend as custom SMTP** under Auth → Emails) before real use — see `app-architecture.md`.

## 6. Run the live validation
**On Node (quick):**
```bash
pnpm dev
```
Visit `http://localhost:3000/login` → **Create account** (email + 8+ char password) → you land on `/dashboard`.

**On Cloudflare's runtime (the real target):**
```bash
pnpm preview        # opennextjs-cloudflare build + serves on workerd
```
Same flow at the previewed URL.

### ✅ Success looks like
`/dashboard` shows your email, role **parent**, and:
> ✓ Auth session + RLS-scoped profile read succeeded on this runtime.

That confirms: session cookies via Edge middleware, the `on_auth_user_created` trigger created your `profiles` row, and the RLS `profiles: self read` policy returned exactly your row. **P0 is done.**

## 7. (Optional) Keep-warm so the free project never pauses
Add two **GitHub repo secrets** (Settings → Secrets and variables → Actions): `SUPABASE_URL` and `SUPABASE_ANON_KEY`. The `.github/workflows/keepalive.yml` action then pings every 3 days. You can also run it once now via **Actions → Supabase keep-warm → Run workflow**.

---

## Troubleshooting
| Symptom | Cause / fix |
|---|---|
| `supabaseUrl is required` / 500 on every page | env vars not loaded — confirm they're in **both** `.env.local` and `.dev.vars`; restart the dev/preview server. |
| Sign-in says **"Email not confirmed"** | Step 5 not applied — toggle "Confirm email" off, or click the confirmation email. |
| Dashboard shows **role —** / RLS read returns nothing | the signup trigger didn't run — re-check `0001_init.sql` applied (the `on_auth_user_created` trigger + `handle_new_user()` exist). |
| `Node.js middleware is not currently supported` | you re-introduced a nodejs `proxy.ts` — Cloudflare needs the Edge `middleware.ts` (already in the repo). |
| CLI `db push` auth error | run `pnpm dlx supabase login` first; `--project-ref` is the subdomain of your project URL. |

## Security notes
- `.env.local` / `.dev.vars` are gitignored — never commit them.
- `SUPABASE_SERVICE_ROLE_KEY` is server-only and **bypasses RLS**; use it only in guarded server code (PDF generation, admin tasks). If it ever leaks, rotate it in Project Settings → API.

## Next: P1 — enrollment core
Parent child-profiles, program browse + apply, admin program CRUD + roster view — all RLS-gated. See `app-architecture.md` → "Phased build".
