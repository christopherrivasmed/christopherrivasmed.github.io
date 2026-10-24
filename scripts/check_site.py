#!/usr/bin/env python3
"""Sanity checks to run before every push:  python scripts/check_site.py

1. Poster pages, talk pages, the presentations page and the home-page list are up to date with
   posters/<slug>/poster.json and talks/<slug>/talk.json (if not, run: python scripts/build_site.py).
2. Every local file linked from the pages exists (CV, poster PDFs, images...).
3. No phone numbers, unexpected email addresses or street addresses in any text file.
4. Lists every remaining PLACEHOLDER so you know what is still to fill in.

Exit code is 1 if checks 1-3 fail. Placeholders are only reported.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".css", ".js", ".md", ".py", ".svg", ".txt", ".json", ".xml"}
SKIP_DIRS = {".git", "__pycache__"}
problems = []
ALLOWED_EMAILS = {"car452@drexel.edu"}   # addresses you deliberately publish on the page
ALLOWED_PHONES = {"6267207847"}          # phone numbers you deliberately publish (digits only), e.g. on your CV


def text_files():
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.suffix.lower() in TEXT_EXT and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


poster_slugs = sorted(p.parent.name for p in (ROOT / "posters").glob("*/poster.json"))
talk_slugs = sorted(p.parent.name for p in (ROOT / "talks").glob("*/talk.json"))
slugs = poster_slugs + talk_slugs

# 1. generated files current?
res = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py"), "--check"],
                     capture_output=True, text=True, cwd=ROOT)
for line in (res.stdout + res.stderr).splitlines():
    if line.startswith(("error:", "out of date:", "warning:")):
        problems.append(line if not line.startswith("out of date:") else line + " (run build_site.py)")
for folder, group in (("p", poster_slugs), ("t", talk_slugs)):
    for slug in group:
        if not (ROOT / folder / slug / "index.html").exists():
            problems.append(f"{folder}/{slug}/index.html is missing (run build_site.py)")

# 2. local links exist
pages = [ROOT / "index.html", ROOT / "presentations" / "index.html",
         *sorted((ROOT / "p").glob("*/index.html")), *sorted((ROOT / "t").glob("*/index.html"))]
for page in pages:
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
def is_allowed(rx, value):
    if rx is email:
        return value in ALLOWED_EMAILS
    if rx is phone:
        return re.sub(r"\D", "", value) in ALLOWED_PHONES
    return False


for p in text_files():
    if p.name == "check_site.py":
        continue
    for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for label, rx in (("phone number", phone), ("email address", email), ("street address", street)):
            m = rx.search(line)
            if m and not is_allowed(rx, m.group(0)):
                problems.append(f"{p.relative_to(ROOT)}:{n}: possible {label}: {m.group(0)}")

# 3b. the same scan inside PDFs (CV, posters, abstracts); needs: pip install pymupdf
try:
    import pymupdf
except ImportError:
    pymupdf = None
    print("note: PDFs were NOT scanned for phone numbers/addresses (pip install pymupdf to enable)")
if pymupdf:
    for pdf in sorted(ROOT.rglob("*.pdf")):
        if set(pdf.relative_to(ROOT).parts) & SKIP_DIRS:
            continue
        doc = pymupdf.open(pdf)
        meta = " ".join(str(v) for v in doc.metadata.values() if v)
        text = "\n".join(page.get_text() for page in doc) + "\n" + meta
        for label, rx in (("phone number", phone), ("email address", email), ("street address", street)):
            for m in rx.finditer(text):
                if not is_allowed(rx, m.group(0)):
                    problems.append(f"{pdf.relative_to(ROOT)}: possible {label} inside the PDF: {m.group(0)}")

print("Checks")
print("  posters      :", ", ".join(poster_slugs) or "(none)")
print("  talks        :", ", ".join(talk_slugs) or "(none)")
print("  problems     :", len(problems))
for pr in problems:
    print("   -", pr)

# 4. placeholders (skip generated copies: p/ pages and the tile list)
print("\nRemaining PLACEHOLDERs")
count = 0
for p in text_files():
    rel = p.relative_to(ROOT)
    if p.suffix.lower() in {".py", ".md", ".css", ".js"} or rel.parts[0] in ("p", "t") or rel.as_posix() == "presentations/index.html":
        continue
    text = p.read_text(encoding="utf-8")
    if rel.name == "index.html":
        text = re.sub(r"<!-- PRESENTATIONS:START.*?<!-- PRESENTATIONS:END -->", "", text, flags=re.S)
    for n, line in enumerate(text.splitlines(), 1):
        if "PLACEHOLDER" in line and not line.lstrip().startswith("<!--"):
            attr = re.search(r'(?:href|src)="([^"]*PLACEHOLDER[^"]*)"', line)
            shown = attr.group(1) if attr else re.sub(r"<[^>]+>", "", line).strip()[:110]
            count += 1
            print(f"  {rel}:{n}: {shown}")
for pdf in sorted((ROOT / "cv").glob("*.pdf")) + sorted((ROOT / "posters").glob("*/*.pdf")):
    if b"PLACEHOLDER" in pdf.read_bytes():
        count += 1
        print(f"  {pdf.relative_to(ROOT)}: still the stub file, replace it")
print(f"  total: {count}")

sys.exit(1 if problems else 0)
