# S.T.A.N.D Mentorship — Content Library Catalog

**Compiled:** 2026-06-19 · Purpose: a categorized index of every usable image/video for the website redesign (claude.ai/design + the Next.js build), so we know **what each asset is** and **which images work as hero/title-cards** for specific pages.

> **How to use this:** Pick heroes/gallery shots per page from the event sections below. Local previews live in `content-library/preview/<folder>/`; full-res originals in `content-library/images/<folder>/` (gitignored — large). Every image's stable Wix CDN URL + the page(s) it appears on are in `catalog.csv`; per-image dimensions + the preview path are in `manifest.csv`; detailed per-image vision captions are in `captions/<event>.md`.

## Library at a glance (scraped from standmentorship.org)

136 unique images, deduped, organized by source page/event:

| Folder | Count | What it is |
|---|---|---|
| `events/2023-camping-trip/` | 23 | Camping Trip 2023 (MD) |
| `events/2023-ravens-training-camp/` | 20 | Ravens Training Camp 2023 |
| `events/2023-ny-philly-trip/` | 18 | New York / Philadelphia Trip 2023 |
| `events/2024-howard-county-workshop/` | 12 | Howard County Workshop 2024 (Columbia) |
| `events/2024-baltimore-workshop/` | 12 | Baltimore Workshop 2024 |
| `events/2017-unity-basketball/` | 12 | Unity Community Basketball Game 2017 |
| `events/2014-orioles-game-night/` | 7 | Orioles Game Night 2014 |
| `events/2017-ocean-city/` | 6 | Ocean City Summer Trip 2017 |
| `team/` | 9 | Team & board headshots/portraits |
| `misc/` | 7 | Program / donate / registration page images & graphics |
| `home/` | 6 | Homepage hero/section imagery |
| `_brand/` | 4 | Logo wordmark + profile/social icons (site-wide chrome) |

## Methodology & integrity
- **Scrape:** all 19 site pages fetched; Wix media IDs extracted from the embedded page data (galleries render via JS but the item IDs are server-embedded), deduped globally, originals downloaded untransformed. Site-wide chrome (logo/icons) auto-separated into `_brand/`.
- **Previews:** ≤1600px JPEG/PNG derivatives (40 MB total, committed) for fast captioning + design use; 1.8 GB of full-res originals kept local + gitignored.
- **Captions/hero scores:** produced by a vision pass (agents view each preview). Hero score 1–5 (5 = excellent wide hero: landscape, crisp, clear subject, room for text overlay).
- **56 regex false-positives** (0-byte 403s) were removed — not real media.

## Site photos by event — recommended hero / title-card picks
Full per-image tables (description · scene · orientation · quality · hero-score 1–5 · suggested use) are in `captions/<event>.md`. Paths below are relative to `content-library/preview/` (full-res twins in `images/`).

| Page / Event | Recommended hero | Why | Detail file |
|---|---|---|---|
| **Homepage** | `home/83bafb_ba0f7781448340979a092693aecf60d7_mv2.jpg` | Founder with young men in **graduation caps holding diplomas** — the most on-mission wide image (score 5). Alt: `home/83bafb_a46d8468361a4d549a935a73c1a348cf_mv2.png` (kids in zorb balls). | `captions/team-home-misc.md` |
| **Howard County Workshop 2024** | `events/2024-howard-county-workshop/83bafb_08c603b4d57945b1b4c8c1cf6594ec91_mv2.jpg` | Mentor seated mid-gesture addressing the group — clean landscape, well-lit, room for text overlay. The archetypal "mentor mid-session" title card. | `captions/2024-workshops.md` |
| **Baltimore Workshop 2024** | `events/2024-baltimore-workshop/83bafb_da3247634f9a442bb08cf370c4e3d037_mv2.jpg` | Two mentors leading a finance-planning session (whiteboard behind). NOTE: this set tops out at hero-3 — borrow Howard County imagery for the highest-impact slots. | `captions/2024-workshops.md` |
| **Camping Trip 2023** | `events/2023-camping-trip/83bafb_cd355939b1a0454482208e88dfd30d6e_mv2.jpg` | Wide campsite with colorful tents + the full group seated; clean tree-canopy space up top for a title. | `captions/2023-camping-trip.md` |
| **Ravens Training Camp 2023** | `events/2023-ravens-training-camp/83bafb_16f7b29b83804692a8a76309f043070c_mv2.png` | The **only** landscape in the set — teens in branded shirts on the field, practice facility + open sky behind. | `captions/2023-ravens-training-camp.md` |
| **NY/Philadelphia Trip 2023** | `events/2023-ny-philly-trip/83bafb_8cf3b8b8e94d4568ab4f1d222e5e2593_mv2.jpg` | Group + mentor at the **Rocky statue** at night — iconic landmark, dark sky for overlay. | `captions/2023-ny-philly-and-ocean-city.md` |
| **Ocean City Trip 2017** | `events/2017-ocean-city/83bafb_54869f09200b41c6beb4317f9eaddda6_mv2.jpg` | Teens donning red life jackets on a bay dock — bright summer energy, water backdrop. | `captions/2023-ny-philly-and-ocean-city.md` |
| **Unity Basketball 2017** | `events/2017-unity-basketball/83bafb_b36016ef58dc4f7d9d942b1642929edc_mv2.jpg` | Players moving up the court (also `…4065eaf6…` ceremonial tip-off). Clean 4:3 gym shots — crop for wide banners. | `captions/2017-unity-and-2014-orioles.md` |
| **Orioles Game Night 2014** | `events/2014-orioles-game-night/83bafb_ef57a8b1e17f4e0aaff1ed6ba9c3fac5_mv2.jpg` | Group in Orioles gear in the stands (older/softer). The 1600×611 strip `…fec88073…` is the best true wide-aspect asset here. | `captions/2017-unity-and-2014-orioles.md` |

**Cross-library standouts**
- **Best "mentorship moment" portrait:** `misc/83bafb_f09503add6934bd5a929741b6bea04ca_mv2.jpg` — a young man helping a boy tie a necktie (vertical; crop for a feature block).
- **"Experience" story shot:** `misc/83bafb_e60511857984402c8297007f73159dd2_mv2.jpg` — youth meeting Orioles players at the ballpark.
- **Official logo graphic (with tagline):** `misc/83bafb_d8edacddf6a047a29d8c7a7f7c17c423_mv2.jpeg` — "S.T.A.N.D. — Stepping Towards A New Destiny."
- **Event flyers found (not galleries):** STAND **Mother's Day Brunch** (May 17 2025) + **Father's Day Banquet** (June 14 2025) save-the-dates in `misc/` — evidence of recurring family events beyond the 8 galleries.

**⚠️ Designer caveats (from the vision pass)**
- **Orientation:** the large majority of event photos are **vertical phone shots**; true landscapes are scarce, so each event's hero above is usually its *only* clean wide frame. Plan to crop / blur-extend, or lean on the homepage graduation shot + Howard County workshop shot for the strongest wide heroes.
- **Avoid for public pages:** `events/2023-ny-philly-trip/83bafb_547e1c73b8064f3a9fe4050691b4c56c_mv2.jpg` (lingerie billboard behind youth in Times Square); `misc/83bafb_1fb4c0ae…` (generic stock photo); dark/blurry frames flagged hero-1 in the caption tables.
- **Team headshots** (`team/`) are 8 single portraits; a few carry social-media overlays/screenshot bars — **crop before use**; one is a "Coming Soon" placeholder.

## `_brand/` (logo & icons)
The STAND wordmark + square profile/social icons (duplicates of `brand-assets/`). Use `brand-assets/stand-logo-source.png` (3508×2480) as the master logo. See `brand-assets/README.md`.

---

## External images (beyond the site) — `external-images.md`
Catalog of public images of/about STAND with **rights notes** (nothing downloaded). Highlights:

**Likely usable (partner / government / org-owned — request originals or use with credit):**
- **"United We STAND" wellness-circle photo** (mentors + mentees) — best authentic external event shot — Columbia Community Care, Sept 2025.
- **Jahlil Jarrett mentoring a youth on a football field** — Columbia Community Care, 2024.
- **Coach Tigana Duncan headshot** (`.../2025/05/Tigana.webp`) + **team headshots** (Jeffries, Jarrett, Dickerson, Stokes, Kamara) — Columbia Community Care.
- **Black Philanthropy Circle first-ever-grant photo** (award to Duncan) — CFHoCo, Jan 2026.
- **Howard County govt**: YES! Council photo (w/ Exec. Calvin Ball) + a **9-photo Flickr album** (`flickr.com/photos/hocogov/albums/72177720328814974`) — usable with credit (verify per-photo license).
- **Father/Son Basketball flyer** (STAND promo) — wildelake.org, June 2024.

**Reference-only (news — permission required):** WMAR-2 father-son basketball features (2021, 2022 — show Duncan + son **Jeremiah**); FOX45 "Champions of Courage" segment.

**⚠️ Sensitive — NOT for marketing:** CBS Baltimore Angelo Little coverage (2024).

> New intel surfaced here (cross-ref research): Duncan's son **Jeremiah**; additional team names **Dickerson, Stokes, Kamara** (beyond the website's About page).

## External video — `external-video.md`
**Org-owned (usable):** Instagram reel **"STAND Gear coming soon"** (@_standmentorship, Oct 22 2025).
**Third-party, positive (embed/permission):**
- **"Project 365" Day 204** (youtube.com/watch?v=wxSDrJ1VAXs) & **Day 205** (youtube.com/watch?v=YqnaXE0L2SQ) — founder spotlights of Coach Duncan, by **Portia Wheatley** (likely related to COO Dr. Tracey Wheatley), Jul 2021.
- **WMAR-2** father-son basketball segments (2021, 2022) — station-owned; link/license, don't re-host.
**⚠️ Sensitive — NOT for marketing:** WBAL-TV (`47-3rvPN0CI`) + CBS Baltimore segments on the Angelo Little tragedy.
**Gaps:** no org-owned YouTube/TikTok/Vimeo; the richest *usable* pool (IG reels + FB videos) is login-walled — a logged-in pass or an export from the org is needed to inventory it.

## Rights & sensitivity (read before publishing anything)
1. **Site photos** (`images/`, `preview/`) are STAND's own — **but depict minors**; confirm **photo-release consent** with the org before public use.
2. **External "usable" images** are partner/government/org-held — request originals or credit appropriately; verify Flickr/government licenses.
3. **News images/video** = reference-only; license or link-out, don't re-host.
4. **⚠️ The Angelo Little (2024) material is excluded from marketing use** — handle only with the family's/org's blessing and dignity.
