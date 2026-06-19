# S.T.A.N.D — Enrollment App Architecture & Free-Stack Plan

**Date:** 2026-06-19 · **Owner of:** the application stack (auth, data, e-sign, hosting) — canonical over the older marketing-only framing in `redesign-brief.md`.
**Primary goal:** **easy enrollment.** **Hard constraint:** everything **free** (open-source + free tiers; no fixed monthly cost).

## What we're actually building (scope)
A **portal app**, not a brochure:
- **Parent portal:** register/log in · manage their child profile(s) · **e-sign consent/registration forms** · enroll a child in a program · RSVP to events · get location / "where to go" updates.
- **Admin portal (Coach D + staff):** create/manage **programs** · create/manage **events** (edit location, times, details) · view **rosters** (who signed up) · track **who has signed which forms** · post updates/announcements.
- **Public marketing pages** (from the brief) remain, but now funnel into the portal.

## Stress test — current stack vs. requirements
Current stack (from `kevincameron`): Next.js 16 + OpenNext → **Cloudflare Workers**, **D1** (SQLite), shadcn/ui, **Resend**, Stripe. Verdict per requirement:

| Requirement | Stack today | Verdict | Gap fill (free) |
|---|---|---|---|
| Hosting / SSR / API | Workers + OpenNext (free: 100k req/day) | ✅ covers | — |
| Relational data (users, programs, events, enrollments, forms) | D1 (free: 5GB, 100k writes/day) | ✅ covers | + **Drizzle ORM** + drizzle-kit migrations |
| **Auth + roles (parent/admin)** | **none** in starter | ❌ **biggest gap** | **Better Auth** (OSS, self-host on D1) |
| **E-signature on forms** | none | ❌ gap | **signature_pad** + **pdf-lib** + R2 + D1 audit |
| File storage (signed PDFs, uploads) | none | ❌ gap | **Cloudflare R2** (free: 10GB, no egress fees) |
| Forms + validation | none | ⚠️ partial | **react-hook-form + zod** + shadcn Form |
| Roster / signature tables (admin) | shadcn only | ⚠️ partial | **TanStack Table** + shadcn DataTable |
| Email (confirmations, magic links, updates) | Resend (free: ~100/day, 3k/mo) | ⚠️ cap | keep Resend; **Brevo (300/day)** or **Cloudflare Email** if blasts grow |
| Scheduled reminders ("event tomorrow") | none | ❌ gap | **Cloudflare Cron Triggers** (free, built into Workers) |
| Bot/spam protection on signup | reCAPTCHA (starter) | ⚠️ swap | **Cloudflare Turnstile** (free) |
| Payments (only if events charge / donations) | Stripe | ✅ keep | per-transaction only; $0 fixed |

**Net:** the Cloudflare base is a great fit and stays 100% free at this scale. The real gaps are **auth, e-signature, and file storage** — all fillable with open-source libs + Cloudflare's own free R2/Cron/Turnstile.

## Recommended additions (all free / open-source / free-tier on existing infra)
- **Auth → Better Auth** (open-source, self-hosted on D1 via Drizzle adapter, edge/workerd-compatible): email+password, magic link, email verification, **roles** (parent/admin/staff). **Keeps minors' PII in our own D1** — no third party. *(Alt: Clerk free tier = 10k MAU, offloads security but sends PII to a 3rd party and is a free-tier dependency. Better Auth preferred for ownership + privacy.)*
- **ORM → Drizzle** on D1 (+ drizzle-kit for migrations).
- **Storage → Cloudflare R2** (signed PDFs, uploaded docs, photos).
- **E-sign → in-app**: `signature_pad` (typed name + optional drawn signature) → `pdf-lib` stamps a PDF of the completed form → store PDF in R2 + an **immutable audit row** in D1 (signer, user id, timestamp, IP/UA, form-template **version**, content hash). This follows the US **E-SIGN** pattern (intent + attribution + retention). *Not DocuSign-grade workflow, but appropriate and free — consent language should get org/legal review.*
- **Forms → react-hook-form + zod**; **Tables → TanStack Table**; **Reminders → Cron Triggers**; **Bot → Turnstile**.

## Data model (sketch — Drizzle/D1)
- **users** (Better Auth: id, email, role[parent|staff|admin], name, phone) + Better Auth `sessions`/`accounts`/`verification`.
- **participants** (id, parent_user_id→users, name, dob, grade, school) — a parent's child(ren).
- **programs** (id, name, region[Baltimore|Howard], location, description, schedule, capacity, status, created_by).
- **events** (id, program_id?→programs, title, description, location, address, starts_at, ends_at, capacity, status).
- **enrollments** (id, participant_id→participants, program_id→programs, status[applied|enrolled|waitlist]).
- **event_rsvps** (id, event_id→events, participant_id→participants, status).
- **form_templates** (id, key, title, **version**, body, fields_json, requires_signature).
- **form_submissions** (id, template_id→form_templates, version, participant_id, submitted_by→users, data_json, signed_at, signer_name, signature_r2_key, pdf_r2_key, ip, user_agent, content_hash) — the signed/audit record.
- **announcements** (id, scope[all|program|event], ref_id, title, body, created_by, created_at).

## Risks & caveats (the honest stress points)
1. **Auth on the edge is the #1 integration risk.** Better Auth + Drizzle + D1 on workerd must be verified in `pnpm preview` **early** (before building portal UI).
2. **Minors' PII + signed consents = sensitive.** Requires RBAC, least-data, a real **privacy policy + retention policy**, and encrypted-at-rest (D1/R2 provide). If any data is collected directly from under-13s, mind **COPPA**; consents are signed by the **parent**, which mitigates. **Not legal advice — have counsel review.**
3. **Self-hosting auth = we own its security** (session config, password hashing [Better Auth uses scrypt], verification, rate-limit). Acceptable; the trade for $0 + data ownership.
4. **Resend free = ~100 emails/day.** Fine for transactional + a small org; a blast to *all* families could exceed it — batch over time or move to Brevo/Cloudflare Email.
5. **PDF generation on Workers** (pdf-lib) is fine for simple one-page forms; keep templates light to stay within Worker CPU limits, or generate on-demand.
6. **SMS is NOT free** (Twilio etc.). For "where to go" use **email + in-app + (optional, free) web push** — not SMS.
7. **Scope/maintenance:** this is a small SaaS now — more to build, secure, and maintain than a marketing site.

## Phased build
- **P0 — Foundation:** scaffold from the starter; add Better Auth + Drizzle + D1 schema + R2 + Turnstile; verify auth on workerd.
- **P1 — Enrollment core:** parent register/login + child profiles; browse programs; apply/enroll; admin **program CRUD** + **roster** view.
- **P2 — Forms & e-sign:** templates (enrollment, consent, photo release) → in-app sign → PDF in R2 → admin **signature-completion tracking**.
- **P3 — Events & updates:** event CRUD (location/times); RSVP; announcements + Resend + Cron reminders; "where to go".
- **P4 — Public/marketing pages** (the brief's IA), funneling to the portal.
- **P5 — Hardening:** a11y, privacy/retention policy, security review.

## Cost = $0 fixed
Cloudflare Workers/D1/R2/Cron/Turnstile **free tiers** · open-source libs (Better Auth, Drizzle, pdf-lib, signature_pad, RHF, zod, TanStack) · Resend **free tier** · Stripe (only per-transaction, if any). Domain already owned.

## Decisions to confirm
1. **Auth:** Better Auth (self-host, owns PII) — or Clerk free tier (offload security)? *(Recommend Better Auth.)*
2. **Parents-only login for v1**, or do youth/mentees log in too? *(Recommend parents-only.)*
3. **E-sign consent language** will get an org/legal review before go-live? (Required for the signed-forms feature.)
4. OK to keep **Resend free** now and revisit email volume later?
