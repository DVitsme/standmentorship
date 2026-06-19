# S.T.A.N.D — Enrollment App Architecture & Free-Stack Plan

**Date:** 2026-06-19 (rev. Supabase) · **Owner of:** the application stack (auth, data, storage, e-sign). Canonical over the older marketing-only framing in `redesign-brief.md`.
**Primary goal:** **easy enrollment.** **Hard constraint:** everything **free** (open-source + free tiers; no fixed monthly cost).
**Decision (2026-06-19):** data/auth/storage = **Supabase**; app still runs on **Next.js → Cloudflare Workers (OpenNext)**.

## What we're building (scope)
- **Parent portal:** register / log in · manage child profile(s) · **e-sign consent/registration forms** · enroll a child in a program · RSVP to events · get location / "where to go" updates.
- **Admin portal (Coach D + staff):** create/manage **programs** · create/manage **events** (location, times, details) · view **rosters** · track **who has signed which forms** · post updates/announcements.
- **Public marketing pages** (from the brief) remain, funneling into the portal.

## The stack
Next.js 16 (App Router, TS) on **Cloudflare Workers via OpenNext**; UI = shadcn/ui + Tailwind v4. Data layer = Supabase. `supabase-js` talks to Supabase over HTTPS, so it runs cleanly from Workers.

| Layer | Choice | Free? |
|---|---|---|
| Hosting / SSR / API | Cloudflare Workers + OpenNext | ✅ 100k req/day |
| **Auth + roles** | **Supabase Auth** (email/password + magic link, MFA available) | ✅ 50k MAU |
| **Database** | **Supabase Postgres** + **Row-Level Security** | ✅ 500 MB |
| **Authorization** | **RLS policies** — DB-enforced "parents see only their child's rows" | ✅ |
| **File storage** | **Supabase Storage** (signed-form PDFs, uploads) | ✅ 1 GB |
| Schema / types | Supabase CLI **SQL migrations** (incl. RLS) + `supabase gen types` (typed `supabase-js`) | ✅ |
| E-signature | `signature_pad` (capture) + `pdf-lib` (PDF in Worker) → Supabase Storage + audit row | ✅ OSS |
| Forms / validation | react-hook-form + zod + shadcn Form | ✅ OSS |
| Rosters / signature tables | TanStack Table + shadcn DataTable | ✅ OSS |
| Email (auth + transactional + updates) | **Resend** (as Supabase custom SMTP **and** our sender) | ✅ ~100/day |
| Reminders + **keep-warm** | **Cloudflare Cron Triggers** | ✅ |
| Bot/spam protection | **Cloudflare Turnstile** | ✅ |
| Payments (donations / paid events only) | Stripe | per-txn only, $0 fixed |

> **Dropped from the earlier plan:** Better Auth, Cloudflare D1, Cloudflare R2, and Drizzle — all replaced by Supabase (Auth + Postgres + Storage) and `supabase-js` + generated types.

## Why Supabase (recap of the decision)
A kids'-PII app is exactly where you don't want to hand-roll auth or authz. **Supabase Auth** (battle-tested) + **Postgres RLS** gives database-enforced row isolation that maps perfectly to "a parent can only touch their own children's enrollments and signed forms," and consolidates auth + DB + storage into one platform → faster, smaller surface area. Trade accepted: PII lives in Supabase (reputable/SOC2, exportable) and we add one external dependency + a keep-warm chore.

## Running Supabase on Cloudflare Workers (integration notes)
- **`@supabase/ssr`** for cookie-based sessions: a **server client** (Server Components / Route Handlers / Server Actions — note Next 16 `cookies()` is **async**, `await` it), a **browser client**, and a session-refresh in an **Edge `middleware.ts`**. ⚠️ **Gotcha (hit in P0):** OpenNext/Cloudflare rejects Next 16's nodejs `proxy.ts` ("Node.js middleware is not currently supported") — use **Edge `middleware.ts`** instead (Supabase's SSR refresh is edge-safe). The full bundle now builds for workerd.
- **Query as the user** through `supabase-js`/the SSR server client so **RLS applies**. Use the **service-role key only** in server-guarded admin/system paths (PDF generation, cron, webhooks) — it **bypasses RLS**, so gate it carefully.
- **Env/secrets** (Cloudflare): `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (public — safe with RLS), `SUPABASE_SERVICE_ROLE_KEY` (**server secret, never client**), `RESEND_API_KEY`, `TURNSTILE_*`, `STRIPE_*`. `wrangler.jsonc` no longer needs D1/R2 bindings (keep `ASSETS`/`IMAGES`).

## Data model (Postgres + RLS)
- **profiles** (id→`auth.users`, role `parent|staff|admin`, full_name, phone) — 1:1 with the auth user; `role` drives RLS.
- **participants** (id, parent_id→profiles, name, dob, grade, school) — a parent's child(ren).
- **programs** (id, name, region `baltimore|howard`, location, description, schedule, capacity, status, created_by).
- **events** (id, program_id?→programs, title, description, location, address, starts_at, ends_at, capacity, status).
- **enrollments** (id, participant_id→participants, program_id→programs, status `applied|enrolled|waitlist`).
- **event_rsvps** (id, event_id→events, participant_id→participants, status).
- **form_templates** (id, key, title, version, body, fields_json, requires_signature).
- **form_submissions** (id, template_id→form_templates, version, participant_id, submitted_by→profiles, data_json, signed_at, signer_name, signature_path, pdf_path, ip, user_agent, content_hash) — **append-only** signed/audit record.
- **announcements** (id, scope `all|program|event`, ref_id, title, body, created_by, created_at).

**RLS pattern** (representative — full SQL lands in migrations during P0):
```sql
-- a parent reads/writes only their own children
alter table participants enable row level security;
create policy parent_rw_own on participants
  for all using ( parent_id = auth.uid() )
  with check ( parent_id = auth.uid() );

-- admins/staff can read everything (helper checks profiles.role)
create policy staff_read_all on participants
  for select using ( (select role from profiles where id = auth.uid()) in ('admin','staff') );

-- signed forms are immutable: insert allowed, no update/delete policy granted
create policy parent_insert_submission on form_submissions
  for insert with check (
    exists (select 1 from participants p where p.id = participant_id and p.parent_id = auth.uid())
  );
```
Storage: a **private `signed-forms` bucket** with policies mirroring the above (parent reads their own path; admin/staff read all). PDFs are generated in the Worker (`pdf-lib`) and uploaded via `supabase-js`.

## E-signatures (unchanged approach)
Render form → parent affirms (typed name + "I agree" + optional drawn signature via `signature_pad`) → `pdf-lib` stamps a PDF in the Worker → upload to Supabase Storage → write an **append-only audit row** (signer, profile id, timestamp, IP/UA, template **version**, content hash). Follows the US **E-SIGN** pattern (intent + attribution + retention). **Consent-form wording needs org/legal review before go-live.**

## Keep-warm (required, free)
Free Supabase projects pause after ~7 days idle. A **GitHub Actions scheduled workflow** (`.github/workflows/keepalive.yml`, every 3 days) pings the public `keepalive` table to reset the timer — needs repo secrets `SUPABASE_URL` + `SUPABASE_ANON_KEY`. (During active cohorts, real logins keep it warm anyway.) Event reminder emails (P3) can reuse this or a Cloudflare Cron worker.

## Email
Supabase's built-in auth email is rate-limited/testing-only, so configure **Resend as Supabase's custom SMTP** for magic-link/verification mail, and use Resend for our own confirmations/announcements. **Watch the ~100 emails/day free cap** (now covers auth emails too); if parent-wide blasts grow, move to **Brevo (300/day)** or batch over time.

## Free-tier limits (all comfortably within a small-org scale)
Supabase: 500 MB DB · 1 GB storage · 50k MAU · 5 GB egress · **2 active projects** (prod + staging) · pauses at 7 days idle (mitigated). Cloudflare Workers/Cron/Turnstile free. Resend ~100/day. **Total fixed cost: $0.** Domain already owned. (Supabase Pro $25/mo removes the pause + raises caps **if ever needed** — not required now.)

## Risks & caveats
1. ~~`@supabase/ssr` session-refresh on workerd~~ — **RESOLVED in P0:** OpenNext needs an **Edge `middleware.ts`** (nodejs `proxy.ts` is unsupported); the bundle now builds for workerd. Remaining: the *live* sign-in + RLS read against a real Supabase project.
2. **Minors' PII now in Supabase** — needs RLS (have it), least-data, a real **privacy + retention policy**, and (parent-signed mitigates) **COPPA** awareness. **Not legal advice — counsel reviews consent + privacy.**
3. **RLS only protects you if you query as the user**; the service-role key bypasses RLS — confine it to guarded server paths.
4. **Free-tier pause** — neutralized by the keep-warm cron, but it must ship in P0.
5. **Resend ~100/day** cap now also covers auth emails.
6. **No free SMS** — "where to go" via email + in-app (+ optional free web push), not texts.
7. This is a small **SaaS** now — more to build, secure, and maintain than a brochure.

## Phased build
- **P0 — Foundation** ✅ *scaffolded 2026-06-19* (builds for Next + workerd): app + `@supabase/ssr` (server/browser + **Edge `middleware.ts`**), first migration (schema + RLS), keep-warm GitHub Action, auth smoke-test pages (`/login`, `/dashboard`). **Remaining:** create the Supabase project + run the live sign-in/RLS test on `pnpm preview`.
- **P1 — Enrollment core:** parent register/login + child profiles; browse programs; apply/enroll; admin **program CRUD** + **roster** view (RLS-gated).
- **P2 — Forms & e-sign:** templates (enrollment, consent, photo release) → in-app sign → PDF in Storage → admin **signature-completion tracking**.
- **P3 — Events & updates:** event CRUD (location/times); RSVP; announcements + Resend + Cron reminders; "where to go".
- **P4 — Public/marketing pages** (the brief's IA), funneling to the portal.
- **P5 — Hardening:** a11y, privacy/retention policy, security review.

## Decisions remaining
1. **Consent-form language** gets an org/legal review before the signed-forms feature goes live. *(Required.)*
2. **Parents-only login for v1** (youth/mentees don't log in) — assumed yes.
3. Keep **Resend free** for now (revisit if email volume climbs) — assumed yes.
