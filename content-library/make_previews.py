#!/usr/bin/env python3
"""Generate web-optimized previews of the scraped originals (≤1600px long edge).
Previews are small enough to commit and to caption quickly with vision; the full-res
originals stay local + gitignored. Writes a clean manifest of real images only."""
import os, csv
from PIL import Image, ImageOps

BASE = "/home/nero/Clients/standmentorship/content-library"
SRC = os.path.join(BASE, "images")
DST = os.path.join(BASE, "preview")
MAXDIM = 1600
rows = []

for root, _, files in os.walk(SRC):
    for fn in sorted(files):
        sp = os.path.join(root, fn)
        rel = os.path.relpath(sp, SRC)               # e.g. events/2024-howard-county-workshop/83bafb_..._mv2.jpg
        try:
            im = Image.open(sp)
            im = ImageOps.exif_transpose(im)          # honor phone-photo orientation
        except Exception as e:
            print(f"!! open fail {rel}: {e}"); continue
        ow, oh = im.size
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        scale = min(1.0, MAXDIM / max(ow, oh))
        if scale < 1.0:
            im = im.resize((max(1, round(ow * scale)), max(1, round(oh * scale))), Image.LANCZOS)
        stem = os.path.splitext(rel)[0]
        if has_alpha:
            out_rel = stem + ".png"
            outp = os.path.join(DST, out_rel); os.makedirs(os.path.dirname(outp), exist_ok=True)
            im.save(outp, "PNG", optimize=True)
        else:
            out_rel = stem + ".jpg"
            outp = os.path.join(DST, out_rel); os.makedirs(os.path.dirname(outp), exist_ok=True)
            im.convert("RGB").save(outp, "JPEG", quality=82, optimize=True, progressive=True)
        pw, ph = im.size
        orient = "portrait" if ph > pw * 1.15 else ("landscape" if pw > ph * 1.15 else "square")
        rows.append([os.path.dirname(rel), fn, out_rel, ow, oh, orient,
                     round(os.path.getsize(sp) / 1024), round(os.path.getsize(outp) / 1024)])

rows.sort()
with open(os.path.join(BASE, "manifest.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["folder", "original_file", "preview_path", "orig_w", "orig_h", "orientation", "orig_kb", "preview_kb"])
    w.writerows(rows)

tot_prev = sum(r[7] for r in rows) / 1024
print(f"Generated {len(rows)} previews → {tot_prev:.1f} MB total in content-library/preview/")
import collections
byf = collections.Counter(r[0] for r in rows)
for k in sorted(byf):
    print(f"  {k}: {byf[k]}")
