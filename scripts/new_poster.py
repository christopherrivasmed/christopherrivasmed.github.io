#!/usr/bin/env python3
"""Create the permanent redirect page p/<slug>/index.html for a new poster.

Usage:  python scripts/new_poster.py my-slug

The slug becomes the QR-code path (/p/my-slug/) and the poster anchor (/#poster-my-slug).
Use lowercase letters, digits and hyphens only. Never rename a slug after printing a poster.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirecting to poster...</title>
  <meta name="robots" content="noindex">
  <meta name="color-scheme" content="light dark">
  <!--
    Permanent redirect for poster "{slug}". Do not rename or delete this folder once the poster is printed.
    The delay is 0 seconds. If you enable GoatCounter below, change content="0; ..." to content="1; ..."
    so the page view has time to be counted before the redirect.
  -->
  <meta http-equiv="refresh" content="0; url=/#poster-{slug}">
  <link rel="canonical" href="https://christopherrivasmed.github.io/#poster-{slug}">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{ font: 1.1rem/1.6 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; margin: 0; padding: 2rem 1rem; text-align: center; }}
    a {{ font-weight: 700; }}
  </style>
  <!-- OPTIONAL ANALYTICS (GoatCounter), disabled. Uncomment and replace YOURCODE to count scans of this poster.
  <script data-goatcounter="https://YOURCODE.goatcounter.com/count"
          async src="https://gc.zgo.at/count.js"></script>
  -->
</head>
<body>
  <p>Taking you to the poster page&hellip;</p>
  <p><a href="/#poster-{slug}">Tap here if you are not redirected</a></p>
  <script>location.replace("/#poster-{slug}");</script>
</body>
</html>
"""

CARD = """
Now add this card inside the Posters section of index.html (newest first):

      <article class="poster" id="poster-{slug}">
        <h3>POSTER TITLE</h3>
        <p class="meta">CONFERENCE &middot; MONTH YYYY</p>
        <ul>
          <li><a href="posters/{slug}.pdf">Poster PDF</a></li>
          <li><a href="ABSTRACT_URL">Abstract</a></li>
          <li><a href="#pub-rivas-2025">Related paper</a></li>   <!-- delete if none -->
        </ul>
      </article>

Then copy your poster PDF to posters/{slug}.pdf and run:  python scripts/make_qr.py {slug}
"""


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", sys.argv[1]):
        print(__doc__)
        print("Error: give exactly one slug made of lowercase letters, digits and hyphens.")
        return 2
    slug = sys.argv[1]
    out = ROOT / "p" / slug / "index.html"
    if out.exists():
        print(f"Refusing to overwrite existing {out.relative_to(ROOT)}")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(slug=slug), encoding="utf-8", newline="\n")
    print(f"Created {out.relative_to(ROOT)}")
    print(CARD.format(slug=slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
