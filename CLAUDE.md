# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Website redesign for S.T.A.N.D Mentorship** (`standmentorship.org`) — a Maryland youth-mentorship nonprofit. This workspace currently holds **research + planning artifacts**; the codebase will be a **Next.js site deployed to Cloudflare**, built from a design produced in **claude.ai/design**.

**Workflow:** claude.ai/design (visual design) → build it as Next.js → host on Cloudflare (OpenNext).

## ⛳ Read first — canonical docs (single sources of truth)

Do **not** re-research or re-decide what these already settle. If something changes, update the doc.

| Doc | Authority over |
|---|---|
| `CLAUDE.md` (this file) | Locked decisions, status, conventions, drift control |
| `research/SUMMARY.md` | Who the org is — facts, people, funding, impact, **copy source of truth** |
| `research/README.md` | Index to the full research dossier (`research/website|external|people|raw`) |
| `redesign-brief.md` | IA/sitemap, navbar/footer, page specs, visual + tech direction |
| `brand-assets/README.md` | Logo files, current palette/fonts, the keep/adjust/change plan |
| `content-library/CATALOG.md` | Image/video asset library — captions + recommended hero/title-card per page |
| `/home/nero/Clients/NextJs/kevincameron/CLAUDE.md` | **The build conventions bible** — mirror it when coding |

## Build status (updated 2026-06-19)

- **Phase: PRE-BUILD.** No `package.json` / app code yet. Research, brief, and brand capture are done.
- **Git (2026-06-19):** initialized and pushed to **GitHub** — remote `origin` = `git@github.com:DVitsme/standmentorship.git`; working branch **`main`** tracks `origin/main`. (The interim `setup/foundation` branch was consolidated into `main`.) Commit/push only when asked.
- **Content library built (2026-06-19):** `content-library/CATALOG.md` — 136 scraped site images (≤1600px previews committed; 1.8 GB full-res originals kept local + gitignored) + per-image vision captions + a recommended hero/title-card per page + external image/video research with rights notes. Consult before sourcing imagery.
- **Next:** produce the claude.ai/design homepage, then scaffold the Next.js app (mirror `kevincameron`).
- Append dated notes here as work ships; never silently rewrite past status.

## Locked decisions (do not contradict without updating this list)

1. **Stack:** Next.js 16 (App Router, TS strict) + Tailwind v4 (CSS-first, tokens in `app/globals.css`, no config file) + shadcn/ui `new-york` + lucide. Mirror `kevincameron` / the `digitaldog-site-starter` pattern.
2. **Hosting:** Cloudflare Workers via **OpenNext** (`@opennextjs/cloudflare`, `wrangler.jsonc`, `open-next.config.ts`). Package manager **pnpm**.
3. **Brand:** keep the existing identity — **black + white + red (`#ED1C24`)**; **change the typeface** (off Cinzel/Helvetica → bold grotesque display + Inter, via `next/font`); only **slight** color adjustments. Reuse the STAND wordmark.
4. **Donations:** port `kevincameron`'s Stripe Payment-Element slice, **but flip the framing to tax-deductible** — STAND is a real **501(c)(3)**; show **EIN 82-1192567**. Add recurring gifts.
5. **Forms (enroll/contact):** native branded forms → `/api/*` → Resend + reCAPTCHA. Replace raw Google Forms.
6. **IA:** 10 core pages + 2 legal + an Event-Detail template (see `redesign-brief.md` §5). Content as typed `content/*.ts`.

## Org facts that must stay consistent (copy guardrails)

- **Legal name:** Stepping Towards A New Destiny Corporation. **EIN 82-1192567.** 501(c)(3) since **April 2017**. **990-N filer (<$50K/yr)** — *no public financials exist; never invent revenue/budget numbers.*
- **Acronym:** "**Stepping Towards A New Destiny**" (legal) — the site also uses the backronym *Strengthening, Training, Advancing, Nurturing, Developing*. Both are valid.
- **Who/where:** mentorship for **young men of color** in **Baltimore City, Baltimore County, and Howard County, MD.**
- **Founder:** **Tigana S. ("Coach") Duncan**, ED/CEO, born Trinidad & Tobago.
- **Programs:** free **Leadership Academies** (Baltimore + Howard County); **4 pillars** — Entrepreneurship/financial literacy, Overall Health, Life Skills, Trades & Innovation (HVAC, CDL, plumbing, electrical, carpentry, barbering).
- **Impact stats (cite as-is):** 96% summer attendance · 92% "more confident" · zero re-arrest.
- **Key relationships:** **Columbia Community Care** (umbrella/host), PUSH, **Howard County government** funding, **Black Philanthropy Circle of Howard County** (first-ever grant).
- **Contact:** info@standmentorship.org · 443-473-3605. **Social:** IG `@_standmentorship` (+ a duplicate `@standmentorship` to consolidate), FB `/standmentorship1`. No org LinkedIn/YouTube yet.
- **⚠️ Sensitivity:** a 17-year-old mentee (Angelo Little) was murdered at the Mall in Columbia, July 2024. Central to the mission but reference **only with dignity, never as a marketing device.**
- **UNVERIFIED items** flagged in `research/SUMMARY.md` (e.g., exact founding year, MD SDAT/charity registration, four board bios) stay flagged — don't promote to fact.

## Commands

**The app is not scaffolded yet** — there is nothing to build/run in this folder today. Once scaffolded mirroring `kevincameron`, these apply (verify against that repo's `package.json`):

| Task | Command | Notes |
|---|---|---|
| Dev | `pnpm dev` | Next 16 Turbopack, http://localhost:3000 |
| Build | `pnpm build` | `next build` |
| Lint | `pnpm lint` | runs `eslint` directly (`next lint` removed in 16) |
| CF preview | `pnpm preview` | builds + serves on Cloudflare **workerd** (OpenNext) |
| Deploy | `pnpm run deploy` | **NOT** `pnpm deploy` (pnpm shadows it). Needs `wrangler login` / `CLOUDFLARE_*` |
| CF types | `pnpm cf-typegen` | after editing `wrangler.jsonc` bindings |

## Conventions (when we build — from the `kevincameron` bible)

- **Next.js 16 ≠ training data.** Request APIs are async-only (`await` `params`/`searchParams`/`cookies()`); `middleware`→`proxy`; Turbopack default; `next/image` uses `remotePatterns`. Read `node_modules/next/dist/docs/01-app/02-guides/upgrading/version-16.md` before writing app code.
- **Tailwind v4:** no `tailwind.config.js`; brand tokens + `@theme inline` + oklch vars live in `app/globals.css`. Repoint shadcn semantic tokens (`--primary`/`--accent`/`--background`…) to the STAND palette.
- **Workers runtime ≠ full Node** (e.g., Stripe webhook must use `constructEventAsync` / Web Crypto). Secrets: `.dev.vars` (preview) / `.env.local` (dev) / `wrangler secret put` (prod).
- `cn()` from `lib/utils`; content lives in typed `content/*.ts` as the single source of truth.

## 🧭 Anti-drift & memory strategy

**Goal:** keep decisions and facts stable across sessions and context resets. Two tiers, one canonical source:

1. **`CLAUDE.md` is canonical** for the project (decisions, status, facts, conventions). **Read it first every session.** When a decision is made or work ships, **update the relevant section here in the same change** — especially *Locked decisions* and *Build status*. Never contradict a locked decision without editing it here (with a dated note).
2. **Persistent project memory** (`~/.claude/projects/-home-nero-Clients-standmentorship/memory/`, surfaced via `MEMORY.md`) stays **thin and non-duplicative**: a pointer that this file is canonical, plus Derrick's working preferences/feedback. **Do not copy project facts into memory** — two copies drift; keep facts here.
3. **Canonical research/specs** (`research/SUMMARY.md`, `redesign-brief.md`, `brand-assets/README.md`) own their domains. Cite them instead of re-deriving. If new info conflicts, **update the doc + note it in Build status** — don't leave two answers.
4. **Preserve uncertainty:** keep `UNVERIFIED`/confidence flags from the research; don't launder them into facts.
5. **Append, don't erase:** Build status is a dated log. New entries on top or bottom, but keep the history.
