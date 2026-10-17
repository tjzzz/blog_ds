#!/usr/bin/env python3
"""Verify a root-sourced MkDocs build contains only intended public paths."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT.parent / "Z_Project_DS_site"
ALLOWED_ROOT_FILES = {"index.html", "404.html", "sitemap.xml", "sitemap.xml.gz"}
ALLOWED_DIRS = {
    "about", "wiki-log", "wiki-schema", "topics", "relationships",
    "syntheses", "media", "js", "assets", "search",
}

if not (SITE / "index.html").is_file():
    raise SystemExit(f"Missing built homepage: {SITE / 'index.html'}")
if not list((SITE / "assets").rglob("*.js")):
    raise SystemExit("Missing MkDocs theme scripts")

unexpected = []
for path in SITE.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(SITE)
    if rel.parts[0] not in ALLOWED_DIRS and rel.as_posix() not in ALLOWED_ROOT_FILES:
        unexpected.append(rel.as_posix())

if unexpected:
    for item in unexpected[:20]:
        print("Unexpected site file:", item)
    raise SystemExit(f"Unexpected site files: {len(unexpected)}")
print(f"Site output verified: {sum(1 for p in SITE.rglob('*') if p.is_file())} public files")
