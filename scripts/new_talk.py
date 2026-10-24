#!/usr/bin/env python3
"""Start a new talk: creates talks/<slug>/talk.json to fill in.

Usage:  python scripts/new_talk.py my-slug

The slug becomes the permanent talk URL (/t/my-slug/) that a QR code can point to.
Use lowercase letters, digits and hyphens only. Never rename a slug after sharing or printing it.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """{
  "title": "Talk title goes here",
  "venue": "Who it was for / where it was given",
  "date": "2026-01-31",
  "presenter": "Christopher A. Rivas",
  "keywords": [],
  "background": [
    "Two or three sentences of context: when, for whom, and what the talk covers."
  ],
  "video": {
    "youtube_id": "ELEVENCHARS",
    "thumbnail": "thumb.jpg",
    "duration": "30 min",
    "credit": "Who published the recording"
  },
  "chapters": [
    { "time": "0:00", "title": "Introduction" }
  ],
  "slides": "",
  "references": [],
  "links": []
}
"""

NEXT = """
Created talks/{slug}/talk.json

Next steps:
  1. Edit talks/{slug}/talk.json. "title" and "venue" are required; delete any field you do not need
     (for a talk without a video, delete "video" and "chapters").
  2. If there is a video: save a 960 x 540 JPEG of its thumbnail as talks/{slug}/thumb.jpg
     (the page shows it until someone taps play, so nothing loads from YouTube first).
     "youtube_id" is the 11 characters after v= in the video's web address.
  3. python scripts/build_site.py        builds the talk page and updates the lists
  4. python scripts/make_qr.py {slug}       makes qr/{slug}.svg and qr/{slug}.png (optional)
"""


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sys.argv[1]):
        print(__doc__)
        print("Error: give exactly one slug made of lowercase letters, digits and hyphens.")
        return 2
    slug = sys.argv[1]
    out = ROOT / "talks" / slug / "talk.json"
    if out.exists():
        print(f"Refusing to overwrite existing {out.relative_to(ROOT)}")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE, encoding="utf-8", newline="\n")
    print(NEXT.format(slug=slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
