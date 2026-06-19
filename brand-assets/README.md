# Brand Assets — starting point (from standmentorship.org)

**Captured:** 2026-06-19 from the live Wix site. Plan per client: **keep the existing brand as the starting point, change the typeface, make slight color adjustments.**

## Files in this folder
| File | What it is | Dimensions |
|---|---|---|
| `stand-logo-source.png` | High-res source of the **STAND** logo graphic (the site's wordmark is a crop of this) | 3508 × 2480, RGBA PNG |
| `icon-01c3aff.png` | Square logo mark / social-profile icon | 200 × 200, RGBA PNG |
| `icon-11062b.png` | Square logo mark / icon (2nd variant) | 201 × 200, RGBA PNG |

> ⚠️ The logo we have is **raster (PNG)**. Ask the client for a **vector original (SVG/AI/EPS)** if one exists — needed for crisp scaling, favicon, and the new wordmark. If none exists, we recrop/retrace from `stand-logo-source.png`.

## Current color palette (extracted from the Wix theme)
The site's real brand swatches (`--color_1..5`), plus key UI grays:

| Token | RGB | HEX | Role today |
|---|---|---|---|
| Black | 0,0,0 | **#000000** | Primary / ink, backgrounds |
| White | 255,255,255 | **#FFFFFF** | Paper / reversed text |
| **Brand Red** | 237,28,36 | **#ED1C24** | Signature accent (the STAND red) |
| Deep Red | 139,0,0 | **#8B0000** | Found in CSS — depth/hover red |
| Blue (legacy) | 0,136,203 | **#0088CB** | Minor/legacy secondary — likely drop |
| Dark gray | 51,51,51 | **#333333** | Body text on light |
| Mid gray | 89,89,89 | **#595959** | Secondary text |
| Light gray | 176,176,176 | **#B0B0B0** | Borders/muted |
| Off-white | 232,230,230 | **#E8E6E6** | Section tint |

**Read:** the identity is essentially **black + white + red** (bold, athletic, high-contrast). The blue is incidental. We'll keep black/white/red and refine.

## Current typography (what we're replacing)
- **Cinzel** (serif, Roman capitals) — display/headings & logo feel.
- **Helvetica W01** (bold/roman) — body & headings.
- **DIN Next W01 Light** — small/caption text.
- Arial Black — occasional display.

## Proposed adjustments for the redesign

### Color — keep black/white/red, refine for accessibility (slight changes)
| New token | HEX (proposed) | Notes |
|---|---|---|
| `--ink` | #0A0A0A | Near-black for large fills; true #000 for crisp type |
| `--paper` | #FFFFFF | Base |
| `--paper-tint` | #F6F6F5 | Subtle section background (replaces #E8E6E6) |
| `--brand` (red) | #E11D24 | Slightly refined STAND red; **verify 4.5:1 contrast** on white for text use, otherwise reserve for fills/CTAs |
| `--brand-deep` | #8B0000 | Hover/active, depth |
| neutrals | #171717→#FAFAFA | Clean 50–900 gray ramp |
| `--accent` (optional) | TBD | Only if a 2nd accent is needed (e.g., a refined blue/gold); default = **no second color**, keep discipline |

> Tailwind v4 / shadcn pattern (mirror `kevincameron/app/globals.css`): repoint shadcn semantic tokens (`--primary`, `--accent`, `--background`, `--foreground`, `--ring`…) to these brand tokens in `:root`, expressed in **oklch**, plus brand utilities (`bg-ink`, `text-brand`, `bg-paper`, etc.). Convert the hex above to oklch at build time.

### Typography — new pairing (final choice in claude.ai/design)
Moving off Cinzel/Helvetica. Recommended directions (all Google Fonts → load via `next/font/google` like the starter):
- **A — Athletic/Bold (recommended for STAND's energy):** Display **Archivo** (use Archivo Expanded/Black for big headings) + Body **Inter**.
- **B — Modern grotesque:** Display **Sora** or **Familjen Grotesk** + Body **Inter**.
- **C — Dignified editorial (keeps a hint of Cinzel's class):** Display **Fraunces** (serif) + Body **Inter / Public Sans**.

**Lean:** Option A (bold sans display + Inter) suits the black/white/red, sports-and-trades, youth-empowerment identity. Confirm during design.

## Logo deliverables to produce
- Horizontal **wordmark** (light + reversed/white versions).
- Square **mark/avatar** (from icon PNGs) for favicon, social, app icon.
- Favicon set (16/32/180/192/512) + `site.webmanifest`.
- Export to `public/` in the Next.js build (e.g., `public/brand/`).

## Other brand imagery on the site (URLs, not yet downloaded)
The homepage uses several portrait/people photos (`static.wixstatic.com/media/83bafb_*~mv2.{png,jpg}`, ~326×454 and 652×908) — real youth/mentor photography we can reuse **with photo-release consent**. Full URL list is in the scraped HTML; pull these when building the relevant pages.
