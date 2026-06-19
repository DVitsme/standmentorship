# S.T.A.N.D Mentorship — Website Redesign Brief

> **⚠️ UPDATE 2026-06-19 — PRIMARY GOAL CHANGED to EASY ENROLLMENT; scope expanded to a parent/admin portal app.** The goal hierarchy in §1–§4 below (which led with funding/credibility) is **superseded** — see `docs/app-architecture.md` for the app architecture + free stack. The sitemap, navbar/footer, brand, visual, and base-tech sections remain valid, with authenticated portal pages added.

**Date:** 2026-06-17 · **Basis:** `research/SUMMARY.md` and the full research dossier · **Stage:** pre-design (no code/design started yet)
**Org:** S.T.A.N.D Mentorship — legal name *Stepping Towards A New Destiny Corporation* · 501(c)(3) (EIN 82-1192567) · Baltimore City/County + Howard County, MD

---

## 1. Why we're redesigning (problem statement)
The current Wix site under-sells a strong organization. It has a near-empty homepage (just a founder quote), an empty "Upcoming Events" page, photo-only event pages with no stories, a bare donation form with no trust signals, enrollment dumped to raw Google Forms, and **no place for its real credibility** — county funding, a first-ever giving-circle grant, a partner "Outstanding Partnership" award, and hard outcomes (96% attendance, 92% "more confident," zero re-arrest). We're rebuilding to **recruit youth/families, drive donations, earn funder trust, and tell the transformation story** clearly.

## 2. Audiences (in priority order)
1. **Youth & their parents/guardians** — prospective participants (young men of color, ~middle/high-school age) in Baltimore & Howard County. *Mobile-first, plain language, "is this for me / how do I join."*
2. **Donors** — individuals who can give online (recurring + one-time).
3. **Funders & institutional partners** — foundations, county agencies, corporations doing due diligence. *Need credibility, outcomes, transparency.*
4. **Volunteers / mentors / trades partners.**
5. **Media & community.**

## 3. Positioning & messaging
**Positioning line (draft):** *"Stepping Towards A New Destiny — free leadership, life-skills, and skilled-trades mentorship for young men in Baltimore and Howard County."*

**Five messaging pillars:**
1. **Free & comprehensive** — 4 pillars, up to 6 days/week, at no cost.
2. **Real outcomes** — 96% attendance · 92% more confident · zero re-arrest.
3. **Future-ready / trades** — concrete paths: HVAC, CDL, plumbing, electrical, carpentry, barbering + financial literacy.
4. **Rooted & full-circle** — alumni now lead (Darryl Jeffries Jr.); county-backed; community-trusted.
5. **Dignity & transformation** — *"birthed out of brokenness, even though we are not broken."*

**Voice/tone:** warm, direct, hopeful, dignified, action-oriented; faith-rooted but inclusive; speaks to youth *and* parents *and* donors; uses the founder's authentic quotes; no jargon.

## 4. Goals & success metrics
- ↑ **Enrollment applications** submitted online.
- ↑ **Online donations** (esp. recurring donors) and a path to non-county funding.
- **Funder credibility:** clear impact, leadership, transparency (501(c)(3)/EIN).
- **Clarity:** a first-time visitor instantly understands *who it's for, where, what age, what it costs, how to start.*
- **Mobile-first**, **WCAG 2.1 AA** accessible, fast, locally discoverable (SEO).

---

## 5. Sitemap — page count & labels

**Total: 10 core pages + 2 legal/utility pages + 1 reusable "Event Detail" template** (the template generates additional URLs as events are added).

### Core pages (10)
| # | Page | Nav label | Purpose & key modules |
|---|---|---|---|
| 1 | **Home** | Home | Conversion hub; story + impact at a glance. (Section breakdown in §6.) |
| 2 | **About / Our Story** | About | The S.T.A.N.D meaning (both expansions), mission & vision, the 2014→today transformation timeline, founder's "why," service area & who it's for. |
| 3 | **Team & Board** | About ▸ Team & Board | Leadership + board bios with photos; the alumnus-now-leader spotlight; youth-rep board seat; credibility (ex-FDA chair, etc.). |
| 4 | **Programs** | Programs | The **4 Pillars** (detailed), the two **Leadership Academies** (Baltimore & Howard County), schedule/format, "no cost," CTA → Enroll. |
| 5 | **Impact & Recognition** | Impact | Outcome stats, testimonials, awards/grants (Black Philanthropy Circle, Howard County, CCC "Outstanding Partnership"), press mentions, partner logos. *(Combines impact + press so neither looks thin.)* |
| 6 | **Events** | Events | One page: **Upcoming** (graceful "follow us" empty-state) + **Past Events** with short stories + a photo **Gallery**. Links to Event Detail pages. |
| 7 | **Enroll / Join the Academy** | Get Involved ▸ Enroll | Eligibility (age, location, who), "what to expect," timeline, and a **branded application** (replacing raw Google Forms). The key youth conversion. |
| 8 | **Get Involved** | Get Involved ▸ Volunteer / Partner | Volunteer/mentor, partner/sponsor, and trades-partner opportunities; clear asks + forms. |
| 9 | **Donate / Support Us** | Donate (button) | Optimized giving: suggested **tiers**, **recurring** option, "your gift funds X," multiple payment methods, **501(c)(3)/EIN trust block**, employer-match note. |
| 10 | **Contact** | Contact | Form, email, phone, service areas, map of locations, newsletter signup, socials. |

### Legal / utility pages (2)
| # | Page | Where linked | Purpose |
|---|---|---|---|
| 11 | **Privacy Policy** | Footer | Required for forms/donations/analytics; covers minors' data + photo consent. |
| 12 | **Accessibility Statement** | Footer | WCAG commitment + contact for accommodations. |

### Reusable template (1)
- **Event Detail** template — title, date, location, partners, a short narrative, a youth quote/outcome, and the photo gallery. Replaces today's caption-less galleries.

> **Optional Phase-2 pages:** a **News/Blog** (only once there's a content cadence), an **alumni** page, and a **financial transparency** page.

---

## 6. Homepage — section-by-section
1. **Hero** — bold headline (positioning), one-line subhead, **dual CTA** (`Enroll a Youth` / `Donate`), strong authentic photo. Founder's tagline as supporting line, not the whole hero.
2. **Who/what/where strip** — *Free · young men · Baltimore & Howard County · ages [TBD] · up to 6 days/week.*
3. **Impact stat band** — 96% attendance · 92% more confident · zero re-arrest · $0 cost · since 2014.
4. **The 4 Pillars** — four cards (icons + one line each) → Programs.
5. **Transformation story teaser** — "from one after-school room to a regional leadership pipeline," with the alumnus-now-leader hook → About.
6. **The Academies** — Baltimore + Howard County cards with locations → Enroll.
7. **Testimonials** — youth/parent/alumni quotes *(to gather)*.
8. **Recognition band** — Howard County, Black Philanthropy Circle, CCC award, delegate endorsement, "as seen on WMAR-2."
9. **Events + Instagram feed** — upcoming teaser + embedded `@_standmentorship` feed (social proof + freshness).
10. **Donate CTA band** — concise case for giving + 501(c)(3) trust.
11. **Newsletter signup** → footer.

---

## 7. Recommended primary navigation (navbar)
**Layout:** Logo (left) · links (center/right) · persistent **Donate** button (accent color, right). Sticky on scroll; hamburger on mobile with the Donate button kept visible.

```
[S.T.A.N.D Logo]   Home   About ▾   Programs   Impact   Events   Get Involved ▾   Contact     [ Donate ]
                          │                                        │
                          ├─ Our Story                             ├─ Enroll (Join the Academy)
                          └─ Team & Board                          ├─ Volunteer & Mentor
                                                                   └─ Partner & Sponsor
```
- **Donate** is a visually distinct button (not a plain link) and is always present.
- Consider a secondary **`Enroll`** button next to Donate, since enrollment is the other primary conversion.

## 8. Recommended footer
Four columns + a legal bottom bar:

```
┌ S.T.A.N.D Mentorship ──────┬ Explore ───────┬ Get Involved ─────┬ Connect ──────────────────┐
│ Logo                       │ Home           │ Enroll            │ info@standmentorship.org  │
│ One-line mission           │ About          │ Volunteer & Mentor│ 443-473-3605              │
│ "Stepping Towards A        │ Programs       │ Partner & Sponsor │ Baltimore City & County · │
│  New Destiny"              │ Impact         │ Donate            │ Howard County, MD         │
│ [IG] [Facebook] [LinkedIn] │ Events         │                   │ [ Join our newsletter ]   │
└────────────────────────────┴────────────────┴───────────────────┴───────────────────────────┘
── © 2026 S.T.A.N.D Mentorship · 501(c)(3) nonprofit · EIN 82-1192567 · Privacy Policy · Accessibility ──
```
- Include a small **"Donations are tax-deductible"** trust line.
- Social: consolidate to **one** Instagram handle; add an **org LinkedIn** page (currently only the founder has one).

---

## 9. Visual & brand direction
**Starting point = the existing brand** (captured in `brand-assets/`). We **keep the identity, change the typeface, and adjust color slightly.**
- **Mood:** bold, athletic, high-contrast, dignified, hopeful. Modernize and clean up the current look — *evolve*, don't discard.
- **Color:** keep the existing **black + white + signature red (`#ED1C24` → refined `#E11D24`)** palette; add a disciplined neutral gray ramp + deep red (`#8B0000`) for depth/hover. Drop the incidental legacy blue unless a second accent proves necessary. Ensure **WCAG-AA contrast** (reserve red for fills/CTAs where it fails 4.5:1 as text). Full token plan: `brand-assets/README.md`.
- **Type — CHANGE the font** (off Cinzel/Helvetica). Recommended: a **bold grotesque display + Inter body** (e.g., Archivo/Sora + Inter), loaded via `next/font/google`. Final pick in claude.ai/design.
- **Logo:** reuse the **STAND wordmark** (`brand-assets/stand-logo-source.png`); request a vector original; produce light/reversed wordmark + square mark + favicon set.
- **Imagery:** **authentic photography** from their real event galleries (youth, mentors, trips, trades, sports) — never stock faces; photo-release consent for minors. Build a 4-pillar / trades **icon set** (lucide).
- **Layout:** generous whitespace, large type, big tap targets, mobile-first.

## 10. Content to create or gather (dependencies)
- **Brand assets:** logo files, official colors, fonts.
- **Program facts currently hidden in Google Forms:** age range, eligibility, cohort dates, locations, what-to-expect.
- **Testimonials/quotes** from youth, parents, alumni (with consent).
- **Outcome stat sourcing** (cite Howard County / CCC reports).
- **Photos** cleared for web use — **photo-release consent for minors** is essential.
- **Partner/funder logos** (with permission to display).
- **Board completion:** photos + bios for the four thin profiles; fill the "TBD" seat or remove it.
- **Donation processor** content (tiers, impact statements).
- **Privacy Policy** + **Accessibility Statement** copy.

## 11. Technical stack & workflow (LOCKED)
**Workflow:** design in **claude.ai/design** → build that design as a **Next.js site** → host on **Cloudflare**.
**Reference implementation to mirror:** `/home/nero/Clients/NextJs/kevincameron` (the `digitaldog-site-starter` pattern) — a near-perfect structural match (nonprofit/creator site with Donate, supporters, team, partners, press, gallery, legal).
- **Framework:** **Next.js 16** (App Router, no `src/`, `@/*` alias) + **React 19** + **TypeScript** (strict; `params`/`searchParams` are async Promises).
- **Styling:** **Tailwind CSS v4** (CSS-first; all theme tokens + `@theme inline` + oklch vars in `app/globals.css`; no `tailwind.config.js`) + **shadcn/ui** (`new-york` style, Radix). Icons: **lucide-react**. `cn()` from `lib/utils`.
- **Fonts:** `next/font/google` exposed as a CSS variable (as the starter does with Newsreader) — swap in the new STAND display + Inter pairing.
- **Hosting:** **Cloudflare Workers via OpenNext** (`@opennextjs/cloudflare` + `wrangler.jsonc` + `open-next.config.ts`; `nodejs_compat`; `ASSETS`/`IMAGES` bindings; D1 if we persist data). **pnpm**. Deploy with `pnpm run deploy`; preview on workerd with `pnpm preview`.
- **Content model:** typed TS in `content/*.ts` as the single source of truth (pillars, team, board, events, tiers) — easy for us to edit; no heavyweight CMS for v1.
- **Forms:** replace raw Google Forms with **branded forms** (can still pipe to a sheet/email/CRM) so enrollment feels native and trustworthy.
- **Donations:** **port the starter's Stripe slice** (Payment Element, `/api/payment-intent` + webhook via `constructEventAsync`, Resend receipts) — add **recurring gifts**, suggested tiers, Apple/Google Pay. ⚠️ **Flip the framing:** kevincameron uses "rewards crowdfunding, never tax-deductible" because a film isn't a charity — **STAND is a real 501(c)(3), so gifts ARE tax-deductible**; show **EIN 82-1192567** and a tax-deductibility line. (Givebutter/Donorbox remain a no-code fallback.)
- **Forms (enroll/contact):** branded Next.js forms → `/api/*` route → Resend + reCAPTCHA (starter pattern), replacing raw Google Forms.
- **Performance, SEO, analytics:** fast Core Web Vitals; **local SEO** ("free youth mentorship Howard County / Baltimore," "teen trades program Maryland"); add analytics + conversion tracking (enroll + donate).
- **Accessibility:** WCAG 2.1 AA (contrast, keyboard nav, alt text, captions on video).
- **Social:** embed Instagram; consolidate the two IG handles; add org LinkedIn.

## 12. Sensitivity & ethics
- The **2024 loss of a mentee (Angelo Little)** may inform the "why," but reference it **only with the family's/org's blessing, with dignity, never as a marketing device.**
- **Minors' images & data:** explicit photo-release consent; privacy-first forms.

## 13. Suggested phasing
- **Phase 1 (launch):** Home, About, Team & Board, Programs, Enroll, Impact & Recognition, Donate, Contact + footer/legal. (Covers all primary conversions.)
- **Phase 2:** Get Involved depth, Events with per-event stories, Instagram automation, News/Blog, alumni page, transparency page.

## 14. Open decisions to confirm before/during design
- ~~Platform~~ ✅ **DECIDED:** claude.ai/design → Next.js 16 → Cloudflare (OpenNext), mirroring `kevincameron`.
- **Brand assets** ✅ *captured* (logo + palette + fonts in `brand-assets/`) — remaining: (a) is there a **vector logo**? (b) final **font pick**; (c) exact **degree of color adjustment**.
1. **Audience framing:** keep the explicit "young men of color" focus front-and-center, or broaden?
2. **Age range / cohort details** to publish (currently hidden in Google Forms).
3. **Enroll & contact forms:** native branded forms (recommended) — confirm we move off Google Forms.
4. **Donations:** confirm Stripe (port the starter) + **recurring**; confirm tax-deductible framing + EIN display.
5. **Tone on faith:** how prominent should the faith/ministry thread be on the public site?
6. Confirm the **manual research gaps** (MD SDAT/charity registration, exact founding year) if we cite them as trust signals.
