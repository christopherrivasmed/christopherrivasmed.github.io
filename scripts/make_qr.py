#!/usr/bin/env python3
"""Generate a QR code for a poster: qr/<slug>.svg (vector) and qr/<slug>.png (600 dpi).

Usage:
  pip install segno
  python scripts/make_qr.py example
  python scripts/make_qr.py my-slug --size-in 2.5      # printed width of the whole code incl. quiet zone
  python scripts/make_qr.py my-slug --target references   # opens the poster page at its References
  python scripts/make_qr.py --site                        # QR for the home page itself (qr/site-home.*)

The QR encodes  <base_url>/p/<slug>/  (base_url comes from site.json) with error correction level Q
and a 4-module quiet zone (the minimum in the QR standard). Print it at least ~2 x 2 inches
(5 x 5 cm), dark on light. The page must exist first (python scripts/build_site.py). Works for posters and talks.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.exit("segno is not installed. Run:  pip install segno")

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))["base_url"]   # edit site.json to change
QUIET_ZONE = 4        # modules; QR standard minimum
DPI = 600


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?", help="poster or talk slug, e.g. my-poster (must match p/<slug>/ or t/<slug>/)")
    ap.add_argument("--site", action="store_true", help="make a QR code for the home page instead of a poster")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"site root (default {DEFAULT_BASE_URL})")
    ap.add_argument("--target", choices=["page", "references"], default="page",
                    help="page = top of the poster page (default); references = jump to its References section")
    ap.add_argument("--size-in", type=float, default=2.0, help="printed size in inches (default 2.0)")
    ap.add_argument("--dark", default="#000000", help="module color (default black)")
    ap.add_argument("--light", default="#ffffff", help="background color (default white)")
    args = ap.parse_args()

    if args.site:
        url, name = args.base_url.rstrip("/") + "/", "site-home"
    else:
        if not args.slug:
            sys.exit("Give a poster slug, or use --site for the home page.")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
            sys.exit("Slug must be lowercase letters, digits and hyphens only.")
        folder = next((f for f in ("p", "t") if (ROOT / f / args.slug / "index.html").exists()), None)
        if folder is None:
            sys.exit(f"No page for '{args.slug}' (looked in p/ and t/). Run: python scripts/build_site.py")
        url = f"{args.base_url.rstrip('/')}/{folder}/{args.slug}/" + ("#references" if args.target == "references" else "")
        name = args.slug + ("-references" if args.target == "references" else "")
    qr = segno.make(url, error="q", micro=False, boost_error=False)

    total_modules = qr.symbol_size(border=QUIET_ZONE)[0]
    scale = max(1, round(args.size_in * DPI / total_modules))   # whole pixels per module at 600 dpi

    out_dir = ROOT / "qr"
    out_dir.mkdir(exist_ok=True)
    svg_path = out_dir / f"{name}.svg"
    png_path = out_dir / f"{name}.png"

    qr.save(svg_path, scale=10, border=QUIET_ZONE, dark=args.dark, light=args.light,
            title=f"QR code for {url}", desc="Scan to open the page.")
    qr.save(png_path, scale=scale, border=QUIET_ZONE, dark=args.dark, light=args.light, dpi=DPI)

    px = total_modules * scale
    print(f"URL encoded : {url}")
    print(f"Version/ECC : {qr.designator}, error level Q, quiet zone {QUIET_ZONE} modules")
    print(f"SVG         : {svg_path.relative_to(ROOT)} (vector, scales to any size)")
    print(f"PNG         : {png_path.relative_to(ROOT)} ({px} x {px} px = {px / DPI:.2f} in at {DPI} dpi)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
