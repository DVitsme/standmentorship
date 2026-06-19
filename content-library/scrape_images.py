#!/usr/bin/env python3
"""Scrape every image from standmentorship.org (Wix), dedup, organize by page/event, build a manifest.
Wix server-embeds gallery media IDs in page HTML/JSON, so a regex over the fetched HTML captures them
even though galleries render via JS. Downloads the ORIGINAL (untransformed) media for each unique id."""
import os, re, urllib.request, collections, csv

BASE = "/home/nero/Clients/standmentorship/content-library"
IMG = os.path.join(BASE, "images")
PAGES_DIR = os.path.join(BASE, "_pages_html")
UA = "Mozilla/5.0 (X11; Linux x86_64) standmentorship-image-scraper"

# slug -> (folder, human label, priority [lower = more specific, wins when an image is on multiple pages])
PAGES = {
    "": ("home", "Homepage", 50),
    "about": ("team", "About / Team & Board", 20),
    "program-information": ("misc", "Vision & Mission", 80),
    "programs": ("misc", "Programs", 80),
    "regis": ("misc", "Program Registration", 80),
    "enrollment": ("misc", "Enrollment", 80),
    "services": ("misc", "Events hub", 80),
    "upcoming-events": ("misc", "Upcoming Events", 80),
    "past-events": ("misc", "Past Events index", 70),
    "contact": ("misc", "Contact", 80),
    "donate-now": ("misc", "Donate", 80),
    "howard-county-workshop": ("events/2024-howard-county-workshop", "Howard County Workshop 2024", 10),
    "baltimore-city-workshop": ("events/2024-baltimore-workshop", "Baltimore Workshop 2024", 10),
    "s-t-a-n-d-new-york-philly-trip": ("events/2023-ny-philly-trip", "S.T.A.N.D New York/Philadelphia Trip 2023", 10),
    "ravens-training-camp": ("events/2023-ravens-training-camp", "Ravens Training Camp 2023", 10),
    "camping-trip": ("events/2023-camping-trip", "Camping Trip 2023", 10),
    "unity-the-community-basketball-game": ("events/2017-unity-basketball", "Unity The Community Basketball Game 2017", 10),
    "ocean-city-trip": ("events/2017-ocean-city", "Ocean City Trip 2017", 10),
    "s-t-a-n-d-orioles-baseball-game-night": ("events/2014-orioles-game-night", "S.T.A.N.D Orioles Baseball Game Night 2014", 10),
}

MEDIA_RE = re.compile(r"[0-9a-f]{6}_[0-9a-z]{20,}~mv2\.[a-z]{2,4}|[0-9a-f]{32}\.(?:png|jpg|jpeg|gif)")

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "ignore")

os.makedirs(PAGES_DIR, exist_ok=True)
page_media = {}
for slug in PAGES:
    url = "https://www.standmentorship.org/" + slug
    try:
        html = fetch(url)
    except Exception as e:
        print(f"!! fetch fail {slug or 'home'}: {e}"); page_media[slug] = set(); continue
    with open(os.path.join(PAGES_DIR, (slug or "home") + ".html"), "w") as f:
        f.write(html)
    page_media[slug] = set(m.group(0) for m in MEDIA_RE.finditer(html))
    print(f"  {slug or 'home'}: {len(page_media[slug])} media ids")

# global frequency -> chrome (logo/icons/UI appearing on most pages)
freq = collections.Counter()
for ids in page_media.values():
    freq.update(ids)
chrome = {i for i, c in freq.items() if c >= max(6, len(PAGES) * 0.5)}

appears = collections.defaultdict(list)
for slug, ids in page_media.items():
    for i in ids:
        appears[i].append(slug)

assign = {}
for i, slugs in appears.items():
    assign[i] = "_brand" if i in chrome else min(slugs, key=lambda s: (PAGES[s][2], s))

manifest, total_bytes, ok = [], 0, 0
for i, target in sorted(assign.items()):
    folder = "_brand" if target == "_brand" else PAGES[target][0]
    d = os.path.join(IMG, folder); os.makedirs(d, exist_ok=True)
    fname = i.replace("~", "_")
    path = os.path.join(d, fname)
    url = "https://static.wixstatic.com/media/" + i
    status = "ok"
    if not os.path.exists(path):
        try:
            with open(path, "wb") as f:
                f.write(fetch(url, binary=True))
        except Exception as e:
            status = f"FAIL:{type(e).__name__}"
    size = os.path.getsize(path) if os.path.exists(path) else 0
    if status == "ok" and size > 0:
        ok += 1; total_bytes += size
    label = "Brand/UI (site-wide)" if target == "_brand" else PAGES[target][1]
    manifest.append([folder, fname, label, ";".join(sorted(set(appears[i]))) or "?", url, size, status])

with open(os.path.join(BASE, "catalog.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["folder", "file", "source_label", "appears_on_pages", "wix_url", "bytes", "status", "caption_TODO", "hero_score_TODO"])
    w.writerows([row + ["", ""] for row in manifest])

print(f"\nDownloaded {ok}/{len(manifest)} images, {total_bytes/1_048_576:.1f} MB total")
byf = collections.Counter(m[0] for m in manifest)
for k in sorted(byf):
    print(f"  {k}: {byf[k]}")
fails = [m for m in manifest if m[6] != "ok"]
if fails:
    print(f"  !! {len(fails)} failures: {[m[1] for m in fails][:8]}")
