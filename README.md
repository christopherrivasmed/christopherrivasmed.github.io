# Christopher A. Rivas: academic landing page

A single-page, mobile-first site for research posters. Plain HTML and CSS, no framework, no hosting build step.
Live at **https://christopherrivasmed.github.io/** (GitHub Pages, deployed from the `main` branch).

How posters work:

* The home page shows only the **newest few posters** (3 by default) as tiles, with a **"View all posters" button**.
* That button opens `/posters/`, the full list with a **search box**.
* Each tile opens that poster's own page at `/p/<slug>/`: poster title at the top, then the conference and
  date, the poster PDF, the abstract, and the **references**.
* The **QR code on the printed poster points straight at that page**, so people scanning it can see your references.

```
index.html               the home page (About, CV, Publications, Posters, Links, Social media)
site.json                site name, base URL, contact email, how many posters show on the home page, optional GoatCounter code
js/poster-search.js      the search box on the all-posters page
css/style.css            styles (light and dark mode)
cv/Rivas_CV.pdf          your CV
posters/<slug>/          everything for one poster:
    poster.json            title, conference, date, references... (you edit this)
    poster.pdf             the poster (required)
    references.pdf         optional standalone references document
    preview.jpg            optional preview image of the poster
p/<slug>/index.html      GENERATED poster page (the QR target). Do not edit by hand.
posters/index.html       GENERATED list of all posters with search. Do not edit by hand.
qr/<slug>.svg|.png       QR codes (not linked from the page)
assets/                  headshot (photo.jpg), favicon, link-preview image
scripts/                 new_poster.py, build_posters.py, make_qr.py, check_site.py, update_date.py
```

## Add a new poster (about 5 minutes)

Pick a short slug: lowercase letters, digits and hyphens, for example `aans-2026`.
**A slug is permanent.** It is printed on the poster as part of the QR code, so never rename it.

1. **Create the poster folder.**
   ```bash
   python scripts/new_poster.py aans-2026
   ```
   This creates `posters/aans-2026/poster.json`.
2. **Fill in `poster.json`** (see the field list below). Only `title` and `conference` are required.
3. **Add the poster PDF** as `posters/aans-2026/poster.pdf`.
4. **Build the pages.**
   ```bash
   python scripts/build_posters.py
   ```
   This writes `p/aans-2026/index.html`, adds the poster to the all-posters page, and updates the newest-posters
   list on the home page (newest poster first).
   Run it again every time you edit a `poster.json`.
5. **Generate the QR code.**
   ```bash
   pip install segno          # once
   python scripts/make_qr.py aans-2026
   ```
   This writes `qr/aans-2026.svg` (vector, use this for print) and `qr/aans-2026.png` (600 dpi). It encodes
   `https://christopherrivasmed.github.io/p/aans-2026/` at error-correction level Q with a 4-module quiet zone.
   Use `--size-in 3` to set the PNG's printed size. Keep the white border when you place it on the poster, print
   dark on light, and make it at least about 2 x 2 inches (5 x 5 cm).
   If you want a second QR that opens the page scrolled straight to the references, use
   `python scripts/make_qr.py aans-2026 --target references`.
6. **Check and publish.**
   ```bash
   python scripts/check_site.py
   python scripts/update_date.py        # refreshes the footer "Last updated" date
   git add -A
   git commit -m "Add aans-2026 poster"
   git push
   ```
   GitHub Pages updates in about a minute. Scan the QR code from your phone **before** you print.

The QR files in `qr/` are not linked from the page, but they are in the repository and therefore reachable by anyone
who guesses the path. They contain nothing private (only the poster URL). If you would rather not publish them, add
`qr/` to a `.gitignore` and keep them on your computer only.

### `poster.json` fields

```json
{
  "title": "Poster title",
  "conference": "Conference name",
  "date": "2026-04-25",
  "authors": "Rivas CA, Coauthor A",
  "affiliation": "College of Medicine, Drexel University, Philadelphia, PA, USA",
  "keywords": ["stroke", "thrombectomy"],
  "pdf": "poster.pdf",
  "abstract": "Abstract text shown on the page (optional).",
  "abstract_url": "https://doi.org/... or abstract.pdf (optional)",
  "references": [
    "Author A, Author B. Title of article. *Journal Abbrev*. 2024;12(3):45-52. doi:10.1000/example"
  ],
  "references_pdf": "references.pdf",
  "preview": "preview.jpg",
  "links": [ { "label": "Related paper", "url": "/#pub-rivas-2025" } ]
}
```

| Field | Notes |
|---|---|
| `title`, `conference` | Required. |
| `date` | Optional. `2026-04-25`, `2026-04` or `2026`. Posters are listed newest first; a poster with no date (or a date in any other form) is listed last, and no date is shown. |
| `pdf` | The poster PDF in the same folder (defaults to `poster.pdf` if that file exists). The page shows its size so people on slow Wi-Fi know what to expect. Leave it out until the poster is finished: the page then has no poster buttons yet. |
| `authors`, `affiliation` | Optional author line and affiliation line under the conference. |
| `abstract` | Optional text shown on the page, either one string or a list of paragraphs (a leading `Background:`, `Methods:`, `Results:` or `Conclusions:` is bolded). `abstract_url` adds an Abstract button: a web link, or a file in the poster's folder such as `abstract.pdf`. Use either or both. |
| `references` | Optional list, shown as a numbered list in the order given. Web addresses and `doi:10.xxxx/...` become clickable links automatically, and `*Journal Name*` (text between asterisks) is shown in italics, as AMA style requires for journal and book titles. Write each reference without its number. |
| `references_pdf` | Optional standalone document (a file in the poster's folder). Adds a "References (PDF)" button and a download button in the References section. Use it instead of, or in addition to, the list. |
| `preview` | Optional image of the poster (jpg or png, ideally under 300 KB) shown on the page, linking to the PDF. Handy on phones, where PDFs open slowly. Export the first page of your poster to an image. |
| `links` | Optional extra buttons. A `url` starting with `/` or `#` points at your own site (for example `/#pub-rivas-2025` for the paper in your Publications list). |
| `keywords` | Optional words that only the search box looks at. |

A conference name that already contains a year-only date (for example "Drexel Discovery Day 2026" with `"date": "2026"`)
shows the name once. Give the exact date (`2026-04-25`) and it is shown too. Delete any field you do not need. Do not edit `p/<slug>/index.html`, `posters/index.html` or the part between the `POSTERS:START` and
`POSTERS:END` markers in `index.html`: they are overwritten each time you run `build_posters.py`.

### Search

The all-posters page (`/posters/`) has a search box (it appears when JavaScript is on; without JavaScript every poster is
simply listed). It matches every word you type against the title, conference, date, authors and keywords, ignoring
case and accents, so `aans 2026` or `thrombectomy cns` both work. Opening
`https://christopherrivasmed.github.io/posters/?q=aans` pre-fills the search.

### How many posters show on the home page

Set `"home_poster_limit"` in `site.json` (default 3), then run `python scripts/build_posters.py`. The home page shows
that many of the newest posters, then the "View all posters" button. Posters are ordered by `date`, newest first. A
poster with only a year (such as `2026`) sorts after posters with a full date in the same year, so give the exact date
when you know it.

## Test locally

```bash
python -m http.server 8000
```

Open <http://localhost:8000/>, click a poster tile, use the back link, and try the "View all posters" button. Stop the server with Ctrl+C.
Always serve from the repo root; opening the files by double-clicking will not work for some links.

## Before every push

```bash
python scripts/check_site.py
```

It checks that the poster pages and tiles are up to date with the `poster.json` files, that every linked file exists
(poster PDFs, CV, images), and that no phone number, unexpected email address or street address appears in any text
file. It also lists every remaining `PLACEHOLDER`.

## Swap the CV

Replace `cv/Rivas_CV.pdf` with your new file, keeping the same filename, then commit and push.
The link on the page and any printed references keep working. Keep it under a few MB for slow Wi-Fi.

## Edit links and text

* **Profile and social buttons:** in the `Links` and `Social media` sections of `index.html`, edit the
  `href` of the button. Delete a whole `<li>...</li>` to remove one, or copy one to add another.
  Use clean profile URLs without tracking parameters such as `?ev=...` or `?isSelfProfile=true`.
* **Email:** edit the address in the header of `index.html` (both the `mailto:` and the visible text) and in
  `site.json` (shown on poster pages). If you change it, add it to `ALLOWED_EMAILS` in `scripts/check_site.py`
  so the privacy scan accepts it, then run `python scripts/build_posters.py`.
* **Photo:** `assets/photo.jpg` is a 420 x 420 square crop. To change it, save a new square JPEG with the same
  name (strip location metadata first; re-saving through Pillow or an image editor's "export" does this).
  Keep the `alt` text meaningful.
* **Publications:** copy the `<li id="pub-...">` block and edit it. Newest first.
* **Link-preview image:** replace `assets/og-image.png` (1200 x 630 PNG or JPG). Chat apps cache previews, so a
  changed image can take a while to appear.
* **Site address:** if the site ever moves (for example to a custom domain), update `base_url` in `site.json`, the
  `canonical` and `og:` tags in `index.html`, run `python scripts/build_posters.py`, and **regenerate every QR code**.

## Analytics (optional, off by default)

[GoatCounter](https://www.goatcounter.com) is free and does not use cookies. Poster pages are now the real
destination of each QR code, so each `/p/<slug>/` shows up as its own row in your dashboard: that is your scan count
per poster.

1. Create a GoatCounter site and note its code (the part before `.goatcounter.com`).
2. Put it in `site.json` as `"goatcounter_code": "yourcode"` and run `python scripts/build_posters.py`.
   Every poster page then includes the counter. To turn it off, set it back to `""` and rebuild.
3. To count home-page visits too, uncomment the snippet in the `<head>` of `index.html` and replace `YOURCODE`.

## Deploying

GitHub Pages is set to serve the `main` branch, root folder. Every push to `main` goes live automatically.
Check the status with `gh api repos/christopherrivasmed/christopherrivasmed.github.io/pages`.
