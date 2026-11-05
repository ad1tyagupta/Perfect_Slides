#!/usr/bin/env python3
"""
Turn an HTML deck into pictures.

Two things a deck needs that a browser cannot hand you: clean stills of every
slide for a README, a handout or a thumbnail, and a short animated GIF that
shows the motion a still cannot. This does both from the same file.

The deck scales itself to the window, so the browser window is set to the
output size and every slide renders natively at that size. Nothing is resampled
and the type stays sharp.

Usage:
    python shoot_deck.py deck.html
    python shoot_deck.py deck.html --out docs/images --width 1600
    python shoot_deck.py deck.html --slides 1,3,5 --gif docs/images/deck.gif

Requires:
    pip install playwright && playwright install chromium
    ffmpeg, for --gif only
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Deck furniture: real for a viewer, noise in a still. Hidden unless --chrome.
CHROME_CSS = """
.deck-progress, .deck-controls, .edit-toggle, .edit-hint, .edit-bar {
    display: none !important;
}
"""

# Long enough for the slowest built-in animation to settle. The path draw runs
# 1.8s and the last reveal starts at .45s, so a shorter wait photographs a
# half-built slide, which looks like a broken layout rather than a slow one.
SETTLE_MS = 2600

SHOW_SLIDE_JS = """
(i) => {
    if (typeof deck !== 'undefined' && deck && deck.show) {
        deck.show(i);
    } else {
        [...document.querySelectorAll('.slide')].forEach((x, n) => {
            x.style.visibility = '';
            x.classList.toggle('active', n === i);
            x.classList.toggle('visible', n === i);
        });
    }
}
"""

# Replaying a slide's entrance for the GIF. Removing the class and forcing a
# reflow before adding it back restarts the CSS animation from zero; without
# the reflow the browser coalesces both changes and nothing replays.
REPLAY_JS = """
() => {
    const slide = document.querySelector('.slide.active') ||
                  document.querySelector('.slide.visible');
    if (!slide) return;
    slide.querySelectorAll('.reveal').forEach(el => {
        el.classList.remove('reveal');
        void el.offsetWidth;
        el.classList.add('reveal');
    });
}
"""


def parse_slides(spec, total):
    """'1,3,5' or '2-6' or both, 1-based, into sorted 0-based indices."""
    if not spec:
        return list(range(total))
    picked = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, _, hi = part.partition("-")
            try:
                lo, hi = int(lo), int(hi)
            except ValueError:
                sys.exit(f"Cannot read --slides value: {part!r}")
            if lo > hi:
                lo, hi = hi, lo
            picked.update(range(lo, hi + 1))
        else:
            try:
                picked.add(int(part))
            except ValueError:
                sys.exit(f"Cannot read --slides value: {part!r}")
    out = [n - 1 for n in sorted(picked) if 1 <= n <= total]
    if not out:
        sys.exit(f"--slides {spec!r} selects nothing. The deck has {total} slides.")
    return out


def open_deck(playwright, deck, width, keep_chrome):
    """A browser window sized to the output, with the deck loaded and settled."""
    height = round(width * 9 / 16)
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": width, "height": height})
    page.goto(deck.as_uri())
    if not keep_chrome:
        page.add_style_tag(content=CHROME_CSS)
    try:
        page.evaluate("document.fonts.ready")
    except Exception:
        pass
    page.wait_for_timeout(600)
    return browser, page


def shoot_stills(page, indices, out_dir, prefix):
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for i in indices:
        page.evaluate(SHOW_SLIDE_JS, i)
        page.wait_for_timeout(SETTLE_MS)
        path = out_dir / f"{prefix}-{i + 1:02d}.png"
        page.screenshot(path=str(path))
        written.append(path)
    return written


def shoot_gif(page, indices, gif_path, fps, hold_seconds, frame_dir):
    """Sample each slide's entrance as frames, then let ffmpeg build the GIF."""
    step_ms = max(int(1000 / fps), 1)
    frames_per_slide = max(int(hold_seconds * fps), 1)
    n = 0
    for i in indices:
        page.evaluate(SHOW_SLIDE_JS, i)
        page.wait_for_timeout(120)
        page.evaluate(REPLAY_JS)
        for _ in range(frames_per_slide):
            page.screenshot(path=str(frame_dir / f"f{n:05d}.png"))
            n += 1
            page.wait_for_timeout(step_ms)
    if not n:
        return 0

    gif_path.parent.mkdir(parents=True, exist_ok=True)
    palette = frame_dir / "palette.png"
    pattern = str(frame_dir / "f%05d.png")

    # Two passes. A GIF holds 256 colours, and a palette built from these exact
    # frames keeps gradients and antialiased type from banding into mush.
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", pattern,
         "-vf", "palettegen=stats_mode=diff", str(palette)],
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", pattern,
         "-i", str(palette),
         "-lavfi", "paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
         "-loop", "0", str(gif_path)],
        check=True,
    )
    return n


def main():
    ap = argparse.ArgumentParser(
        description="Render an HTML deck to clean PNG stills, and optionally a GIF.")
    ap.add_argument("deck")
    ap.add_argument("--out", default="shots",
                    help="directory for the PNG stills (default: shots)")
    ap.add_argument("--prefix", default="slide",
                    help="filename prefix for the stills (default: slide)")
    ap.add_argument("--width", type=int, default=1600,
                    help="still width in pixels, 16:9 (default: 1600)")
    ap.add_argument("--slides",
                    help="which slides, 1-based, e.g. 1,3,5 or 2-6 (default: all)")
    ap.add_argument("--chrome", action="store_true",
                    help="keep the progress bar, navigation and edit hint in shot")
    ap.add_argument("--no-stills", action="store_true",
                    help="skip the PNGs, useful with --gif")
    ap.add_argument("--gif", help="also write an animated GIF to this path")
    ap.add_argument("--gif-width", type=int, default=900,
                    help="GIF width in pixels (default: 900)")
    ap.add_argument("--fps", type=int, default=10,
                    help="GIF frame rate (default: 10)")
    ap.add_argument("--hold", type=float, default=1.8,
                    help="seconds of animation captured per slide (default: 1.8)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed.\n"
              "  pip install playwright && playwright install chromium")
        sys.exit(2)

    if args.gif and not shutil.which("ffmpeg"):
        print("ffmpeg is not installed, and --gif needs it.\n"
              "  macOS:  brew install ffmpeg\n"
              "  Debian: sudo apt install ffmpeg")
        sys.exit(2)

    if args.no_stills and not args.gif:
        print("Nothing to do: --no-stills without --gif.")
        sys.exit(2)

    deck = Path(args.deck).resolve()
    if not deck.exists():
        print(f"No such file: {deck}")
        sys.exit(2)

    with sync_playwright() as p:
        browser, page = open_deck(p, deck, args.width, args.chrome)
        total = page.evaluate("document.querySelectorAll('.slide').length")
        if not total:
            print("No .slide elements found. Is this an HTML deck?")
            browser.close()
            sys.exit(2)
        indices = parse_slides(args.slides, total)

        if not args.no_stills:
            written = shoot_stills(page, indices, Path(args.out), args.prefix)
            print(f"{len(written)} still{'s' if len(written) != 1 else ''} "
                  f"at {args.width}px in {Path(args.out)}")
        browser.close()

        if args.gif:
            browser, page = open_deck(p, deck, args.gif_width, args.chrome)
            with tempfile.TemporaryDirectory() as tmp:
                frames = shoot_gif(page, indices, Path(args.gif),
                                   args.fps, args.hold, Path(tmp))
            browser.close()
            size_mb = Path(args.gif).stat().st_size / 1_000_000
            print(f"GIF from {frames} frames at {args.gif_width}px: "
                  f"{args.gif} ({size_mb:.1f} MB)")
            if size_mb > 10:
                print("  That is large for a README. Try a lower --fps, "
                      "a smaller --gif-width, or fewer --slides.")


if __name__ == "__main__":
    main()
