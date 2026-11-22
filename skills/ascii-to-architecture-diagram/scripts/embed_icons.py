#!/usr/bin/env python3
"""Inline Simple Icons logos into a diagram HTML file.

Usage: python3 embed_icons.py <file.html> <slug> [<slug> ...]   (Windows: python)

Replaces the `<!--ICONS-->` placeholder (inside <defs>) with one
`<symbol id="i-<slug>" viewBox="0 0 24 24"><path fill="#hex" d="..."/></symbol>`
per slug, coloured with the brand hex from the simple-icons data file.
Reference them with `<use href="#i-<slug>" .../>`.

Prints `OK <slug> #<hex>` or `MISSING <slug>` per slug (MISSING is not fatal).
Exits non-zero only if the file can't be read or has no placeholder.
Python 3 standard library only.
"""
import json
import re
import sys
import unicodedata
import urllib.request

CDN = "https://cdn.jsdelivr.net/npm/simple-icons@latest/"
# v14+ ships data/simple-icons.json (a list with explicit slugs);
# older majors ship _data/simple-icons.json (a list, or {"icons": [...]}).
DATA_PATHS = ("data/simple-icons.json", "_data/simple-icons.json")
PLACEHOLDER = "<!--ICONS-->"
NEUTRAL = "94a3b8"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "embed-icons"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def title_to_slug(title):
    """Simple Icons' own titleToSlug, for data files without a slug field."""
    s = title.lower()
    for a, b in (("+", "plus"), (".", "dot"), ("&", "and"), ("đ", "d"),
                 ("ħ", "h"), ("ı", "i"), ("ĸ", "k"), ("ŀ", "l"), ("ł", "l"),
                 ("ß", "ss"), ("ŧ", "t")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFD", s)
    return re.sub(r"[^a-z0-9]", "", s)


def load_hexes():
    for path in DATA_PATHS:
        try:
            data = json.loads(fetch(CDN + path))
        except Exception:
            continue
        icons = data.get("icons", []) if isinstance(data, dict) else data
        hexes = {}
        for icon in icons:
            if not isinstance(icon, dict) or "hex" not in icon:
                continue
            slug = icon.get("slug") or title_to_slug(icon.get("title", ""))
            hexes[slug] = icon["hex"]
        if hexes:
            return hexes
    return {}


def main():
    if len(sys.argv) < 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    html_path, slugs = sys.argv[1], list(dict.fromkeys(sys.argv[2:]))

    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    if PLACEHOLDER not in html:
        print(f"ERROR: {PLACEHOLDER} placeholder not found in {html_path}", file=sys.stderr)
        return 1

    hexes = load_hexes()
    symbols = []
    for slug in slugs:
        try:
            svg = fetch(f"{CDN}icons/{slug}.svg")
        except Exception:
            svg = ""
        m = re.search(r'<path[^>]*\sd="([^"]+)"', svg) if svg.lstrip().startswith("<svg") else None
        if not m:
            print(f"MISSING {slug}")
            continue
        hex_ = hexes.get(slug, NEUTRAL)
        symbols.append(
            f'<symbol id="i-{slug}" viewBox="0 0 24 24">'
            f'<path fill="#{hex_}" d="{m.group(1)}"/></symbol>'
        )
        print(f"OK {slug} #{hex_}")

    html = html.replace(PLACEHOLDER, "\n    ".join(symbols), 1)
    with open(html_path, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
