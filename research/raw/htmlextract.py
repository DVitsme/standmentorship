#!/usr/bin/env python3
"""Minimal HTML -> text extractor for archived pages. Usage: htmlextract.py file.html"""
import sys, re, html
from html.parser import HTMLParser

SKIP = {"script", "style", "head", "noscript", "svg"}

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self.skip_depth = 0
    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip_depth += 1
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr"):
            self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in SKIP and self.skip_depth:
            self.skip_depth -= 1
    def handle_data(self, data):
        if self.skip_depth == 0:
            t = data.strip()
            if t:
                self.out.append(t + " ")

for path in sys.argv[1:]:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
    except Exception as e:
        print(f"!! could not read {path}: {e}")
        continue
    p = Extract()
    p.feed(raw)
    text = "".join(p.out)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]*\n+", "\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    print(f"\n========== {path} ==========\n")
    print(text.strip())
