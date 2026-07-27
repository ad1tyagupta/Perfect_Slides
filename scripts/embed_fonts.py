#!/usr/bin/env python3
"""
Bake webfonts into a deck so it works with no network.

Downloads every font the deck links to and inlines it as base64, then removes
the CDN link tags. The result is one file that renders identically on a plane,
behind a corporate firewall, or on a conference machine with no wifi.

Usage:
    python embed_fonts.py deck.html                 # writes deck.offline.html
    python embed_fonts.py deck.html out.html
    python embed_fonts.py deck.html --subsets latin,latin-ext,greek

No dependencies beyond the standard library.
"""

import argparse
import base64
import re
import sys
import urllib.request
from pathlib import Path

# Google serves woff2 only to browsers it recognises. Ask as one.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

LINK_RE = re.compile(
    r'<link[^>]+href=["\'](https://(?:fonts\.googleapis\.com|api\.fontshare\.com)[^"\']+)["\'][^>]*>',
    re.I)
PRECONNECT_RE = re.compile(
    r'<link[^>]+rel=["\']preconnect["\'][^>]*(?:googleapis|gstatic|fontshare)[^>]*>\s*',
    re.I)
URL_RE = re.compile(r'url\((["\']?)(https?://[^)"\']+)\1\)')
# Google's CSS labels each @font-face block with its subset.
BLOCK_RE = re.compile(r'(/\*\s*([a-z0-9\-]+)\s*\*/\s*)?@font-face\s*\{[^}]*\}', re.I)


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def keep_subsets(css, subsets):
    """Drop @font-face blocks for subsets we do not need, to control size."""
    if not subsets:
        return css

    kept, dropped = [], 0
    for match in BLOCK_RE.finditer(css):
        label = (match.group(2) or "").lower()
        # Unlabelled blocks are kept; only drop what we can positively identify.
        if label and label not in subsets:
            dropped += 1
            continue
        kept.append(match.group(0))

    if not kept:
        return css          # labelling was not what we expected, keep everything
    if dropped:
        print(f"    dropped {dropped} unused subset blocks")
    return "\n".join(kept)


def inline_font_urls(css, cache):
    """Replace every url(...) in the CSS with a base64 data URI."""
    total = [0]

    def swap(match):
        url = match.group(2)
        if url not in cache:
            try:
                cache[url] = fetch(url, binary=True)
            except Exception as e:
                print(f"    ! could not fetch {url[:70]}: {e}")
                cache[url] = None
        blob = cache[url]
        if blob is None:
            return match.group(0)

        total[0] += len(blob)
        ext = url.rsplit(".", 1)[-1].split("?")[0].lower()
        mime = {"woff2": "font/woff2", "woff": "font/woff",
                "ttf": "font/ttf", "otf": "font/otf"}.get(ext, "font/woff2")
        b64 = base64.b64encode(blob).decode("ascii")
        return f'url(data:{mime};base64,{b64})'

    out = URL_RE.sub(swap, css)
    return out, total[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--subsets", default="latin,latin-ext",
                    help="comma separated, or 'all' to keep every subset. "
                         "Use 'all' for non-Latin decks.")
    args = ap.parse_args()

    src = Path(args.deck)
    if not src.exists():
        print(f"No such file: {src}")
        sys.exit(2)

    out = Path(args.out) if args.out else src.with_suffix(".offline.html")
    html = src.read_text(encoding="utf-8")

    links = LINK_RE.findall(html)
    if not links:
        print("No font CDN links found. Either the deck already embeds its "
              "fonts, or it uses system fonts.")
        sys.exit(0)

    subsets = None if args.subsets.strip().lower() == "all" else {
        s.strip().lower() for s in args.subsets.split(",") if s.strip()
    }

    cache, blocks, grand_total = {}, [], 0
    for url in links:
        print(f"  {url[:80]}")
        try:
            css = fetch(url)
        except Exception as e:
            print(f"    ! could not fetch stylesheet: {e}")
            continue

        css = keep_subsets(css, subsets)
        css, size = inline_font_urls(css, cache)
        grand_total += size
        blocks.append(css)
        print(f"    embedded {size / 1024:.0f} KB")

    if not blocks:
        print("\nNothing embedded. The deck still depends on the network.")
        sys.exit(1)

    # Swap the CDN links for the inlined CSS, and drop the now-useless
    # preconnect hints.
    style = ("<style>\n/* Fonts embedded by scripts/embed_fonts.py. "
             "This deck needs no network. */\n" + "\n".join(blocks) + "\n</style>")

    html = LINK_RE.sub(lambda m: style if m.group(1) == links[0] else "", html, count=len(links))
    html = PRECONNECT_RE.sub("", html)

    out.write_text(html, encoding="utf-8")

    before = src.stat().st_size / 1024
    after = out.stat().st_size / 1024
    print(f"\nWrote {out}")
    print(f"  {before:.0f} KB  ->  {after:.0f} KB  (+{grand_total / 1024:.0f} KB of fonts)")
    print("\nThis file renders identically with no network. Verify it:")
    print(f"  python scripts/verify_deck.py {out}")


if __name__ == "__main__":
    main()
