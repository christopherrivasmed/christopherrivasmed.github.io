#!/usr/bin/env python3
"""Start a new poster: creates posters/<slug>/poster.json to fill in.

Usage:  python scripts/new_poster.py my-slug

The slug becomes the permanent poster URL (/p/my-slug/) that the QR code points to.
Use lowercase letters, digits and hyphens only. Never rename a slug after printing a poster.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """{
  "title": "Poster title goes here",
  "conference": "Conference name",
  "date": "2026-01-31",
  "authors": "Rivas CA, Coauthor A, Coauthor B",
  "keywords": [],
  "pdf": "poster.pdf",
  "abstract": "",
  "abstract_url": "",
  "references_pdf": "",
  "references": [
    "Author A, Author B. Title of paper. Journal. 2024;12(3):45-52. doi:10.0000/example"
  ],
  "links": []
}
"""

NEXT = """
Created posters/{slug}/poster.json

Next steps:
  1. Edit posters/{slug}/poster.json (title, conference, date, references...).
     Delete any field you do not need; "title" and "conference" are required.
  2. Put the poster PDF at posters/{slug}/poster.pdf
     (optional: references.pdf, abstract.pdf, preview.jpg in the same folder; see README)
  3. python scripts/build_site.py        builds the poster page and the home-page tile
  4. python scripts/make_qr.py {slug}       makes qr/{slug}.svg and qr/{slug}.png
"""


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sys.argv[1]):
        print(__doc__)
        print("Error: give exactly one slug made of lowercase letters, digits and hyphens.")
        return 2
    slug = sys.argv[1]
    out = ROOT / "posters" / slug / "poster.json"
    if out.exists():
        print(f"Refusing to overwrite existing {out.relative_to(ROOT)}")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE, encoding="utf-8", newline="\n")
    print(NEXT.format(slug=slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
