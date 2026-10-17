#!/usr/bin/env python3
"""Sanity checks to run before every push:  python scripts/check_site.py

1. Each p/<slug>/ redirect points at an existing #poster-<slug> card on index.html (and vice versa).
2. Every local file linked from the pages exists (CV, poster PDFs, images...).
3. No phone numbers, email addresses or street addresses in any text file.
4. Lists every remaining PLACEHOLDER so you know what is still to fill in.

Exit code is 1 if checks 1-3 fail. Placeholders are only reported.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".css", ".js", ".md", ".py", ".svg", ".txt", ".json", ".xml"}
SKIP_DIRS = {".git", "__pycache__"}
problems = []


def text_files():
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


index = (ROOT / "index.html").read_text(encoding="utf-8")
card_ids = set(re.findall(r'<article[^>]*\bid="poster-([a-z0-9-]+)"', index))
redirect_slugs = {p.parent.name for p in (ROOT / "p").glob("*/index.html")}

# 1. redirects <-> poster cards
for slug in sorted(redirect_slugs):
    page = (ROOT / "p" / slug / "index.html").read_text(encoding="utf-8")
    if f"url=/#poster-{slug}" not in page:
        problems.append(f"p/{slug}/index.html: meta refresh does not point at /#poster-{slug}")
    if slug not in card_ids:
        problems.append(f"p/{slug}/: no <article id=\"poster-{slug}\"> in index.html")
for slug in sorted(card_ids - redirect_slugs):
    problems.append(f"index.html has poster-{slug} but p/{slug}/index.html is missing (run new_poster.py)")

# 2. local links exist
for page in [ROOT / "index.html", *(ROOT / "p").glob("*/index.html")]:
    html = re.sub(r"<!--.*?-->", "", page.read_text(encoding="utf-8"), flags=re.S)
    for ref in re.findall(r'(?:href|src)="([^"]+)"', html):
        if re.match(r"^(https?:|mailto:|#|//|data:)", ref) or "{" in ref:
            continue
        target = ref.split("#")[0].split("?")[0]
        base = ROOT if target.startswith("/") else page.parent
        if target and not (base / target.lstrip("/")).exists():
            problems.append(f"{page.relative_to(ROOT)}: missing file for '{ref}'")

# 3. personal data scan
phone = re.compile(r"(?<![\w.])(?:\+?1[\s.-]?)?\(?\b\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b")
email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
street = re.compile(r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s+){1,3}(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Dr|Drive|Ln|Lane|Way|Ct|Court)\b")
for p in text_files():
    if p.name == "check_site.py":
        continue
    for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for label, rx in (("phone number", phone), ("email address", email), ("street address", street)):
            if rx.search(line):
                problems.append(f"{p.relative_to(ROOT)}:{n}: possible {label}: {rx.search(line).group(0)}")

print("Checks")
print("  poster slugs :", ", ".join(sorted(redirect_slugs)) or "(none)")
print("  problems     :", len(problems))
for pr in problems:
    print("   -", pr)

# 4. placeholders
print("\nRemaining PLACEHOLDERs")
count = 0
for p in text_files():
    if p.suffix.lower() in {".py", ".md", ".css"}:
        continue
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if "PLACEHOLDER" in line and not line.lstrip().startswith("<!--"):
            count += 1
            attr = re.search(r'(?:href|src)="([^"]*PLACEHOLDER[^"]*)"', line)
            shown = attr.group(1) if attr else re.sub(r"<[^>]+>", "", line).strip()[:110]
            print(f"  {p.relative_to(ROOT)}:{n}: {shown}")
for pdf in (ROOT / "cv" / "Rivas_CV.pdf", ROOT / "posters" / "example.pdf"):
    if pdf.exists() and b"PLACEHOLDER" in pdf.read_bytes():
        count += 1
        print(f"  {pdf.relative_to(ROOT)}: still the stub file, replace it")
print(f"  total: {count}")

sys.exit(1 if problems else 0)
