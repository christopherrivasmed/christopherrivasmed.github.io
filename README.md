# Christopher A. Rivas: academic landing page

A single-page, mobile-first site for research posters. Plain HTML and CSS, no framework, no build step.
Live at **https://jsjkymcs2s-maker.github.io/** (GitHub Pages, deployed from the `main` branch).

```
index.html            the whole page (About, Publications, Links, CV, Posters)
css/style.css         styles (light and dark mode)
cv/Rivas_CV.pdf       your CV
posters/<slug>.pdf    one PDF per poster
p/<slug>/index.html   permanent redirect that a poster's QR code points to
qr/<slug>.svg|.png    QR codes (not linked from the page)
assets/               headshot (photo.jpg), favicon, link-preview image
scripts/              new_poster.py, make_qr.py, check_site.py, update_date.py
```

## Finding what still needs filling in

```bash
python scripts/check_site.py
```

Lists every remaining `PLACEHOLDER` and checks that redirects, linked files and posters line up.
Run it before each push. It also warns if a phone number, email address or street address ever
appears in a file. Your email will appear on the page because you put it there on purpose.

## Test locally

```bash
python -m http.server 8000
```

Open <http://localhost:8000/>, then <http://localhost:8000/p/example/>. It should bounce to
`/#poster-example` with the poster highlighted. Stop the server with Ctrl+C.
Always serve from the repo root. Redirects use root-relative paths (`/#poster-...`), so opening
the files by double-clicking will not work.

## Add a new poster (about 5 minutes)

Pick a short slug: lowercase letters, digits and hyphens, for example `aans-2026`.
**A slug is permanent.** It is printed on the poster, so never rename it.

1. **Create the redirect page.**
   ```bash
   python scripts/new_poster.py aans-2026
   ```
   This makes `p/aans-2026/index.html` and prints a card to paste.
2. **Add the poster card.** Paste the printed `<article>` into the Posters section of `index.html`
   (newest first). Its `id` must be `poster-aans-2026`. Fill in title, conference, date and links.
   Delete the "Related paper" line if there is none, or point it at a publication's `id`
   (for example `#pub-rivas-2025`).
3. **Add the poster PDF** as `posters/aans-2026.pdf`.
4. **Generate the QR code.**
   ```bash
   pip install segno          # once
   python scripts/make_qr.py aans-2026
   ```
   This writes `qr/aans-2026.svg` (vector, use this for print) and `qr/aans-2026.png` (600 dpi).
   It encodes `https://jsjkymcs2s-maker.github.io/p/aans-2026/` at error-correction level Q with a
   4-module quiet zone. Use `--size-in 3` to set the PNG's printed size. Keep the white border
   when placing it on the poster, print dark on light, and make it at least about 2 x 2 inches (5 x 5 cm).
5. **Check and publish.**
   ```bash
   python scripts/check_site.py
   python scripts/update_date.py        # refreshes the footer "Last updated" date
   git add -A
   git commit -m "Add aans-2026 poster"
   git push
   ```
   GitHub Pages updates in about a minute. Scan the QR code from your phone **before** you print.

The QR files in `qr/` are not linked from the page, but they are in the repository and therefore
reachable by anyone who guesses the path. They contain nothing private (only the poster URL).
If you would rather not publish them, add `qr/` to a `.gitignore` and keep them on your computer only.

### What visitors see

`/p/<slug>/` redirects (meta refresh, with a JavaScript fallback and a visible link) to
`/#poster-<slug>`. On the main page, a small script highlights that poster card and shows a
"You scanned a poster" box at the top with the poster PDF, abstract and related-paper buttons.
Without JavaScript they still land on the highlighted card.

## Swap the CV

Replace `cv/Rivas_CV.pdf` with your new file, keeping the same filename, then commit and push.
The link on the page and any printed references keep working. Keep it under a few MB for slow Wi-Fi.

## Edit links and text

* **Profile and social buttons:** in the `Links` and `Social media` sections of `index.html`, edit the
  `href` of the button. Delete a whole `<li>...</li>` to remove one, or copy one to add another.
  Use clean profile URLs without tracking parameters such as `?ev=...` or `?isSelfProfile=true`.
* **Email:** edit the address in the header (both the `mailto:` and the visible text). If you
  change it, add it to `ALLOWED_EMAILS` in `scripts/check_site.py` so the privacy scan accepts it.
* **Photo:** `assets/photo.jpg` is a 420 x 420 square crop. To change it, save a new square JPEG
  with the same name (strip location metadata first; re-saving through Pillow or an image
  editor's "export" does this). Keep the `alt` text meaningful.
* **Publications:** copy the `<li id="pub-...">` block and edit it. Newest first.
* **Link-preview image:** replace `assets/og-image.png` (1200 x 630 PNG or JPG). Chat apps cache previews, so a
  changed image can take a while to appear.

## Analytics (optional, off by default)

[GoatCounter](https://www.goatcounter.com) is free and does not use cookies. To count scans per poster:

1. Create a GoatCounter site and note its code.
2. In `index.html` and in each `p/<slug>/index.html`, uncomment the `<script data-goatcounter=...>` tag and replace `YOURCODE`.
3. In each `p/<slug>/index.html`, change `content="0; url=..."` to `content="1; url=..."` so the visit is
   recorded before the redirect.

Each `/p/<slug>/` path then shows up as its own row in your GoatCounter dashboard. Remove the snippet to turn it off.

## Deploying

GitHub Pages is set to serve the `main` branch, root folder. Every push to `main` goes live automatically.
Check the status with `gh api repos/jsjkymcs2s-maker/jsjkymcs2s-maker.github.io/pages`.
