#!/usr/bin/env python3
"""Set the footer "Last updated" date in index.html to today:  python scripts/update_date.py"""
import re
from datetime import date
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "index.html"
today = date.today()
html = path.read_text(encoding="utf-8")
new, n = re.subn(
    r'(Last updated: <time datetime=")[^"]*(">)[^<]*(</time>)',
    lambda m: f'{m.group(1)}{today.isoformat()}{m.group(2)}{today.strftime("%B")} {today.day}, {today.year}{m.group(3)}',
    html,
)
if n != 1:
    raise SystemExit("Could not find the 'Last updated' footer line.")
path.write_text(new, encoding="utf-8", newline="\n")
print(f"Footer date set to {today.isoformat()}")
