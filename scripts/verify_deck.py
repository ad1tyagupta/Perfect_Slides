#!/usr/bin/env python3
"""
Check an HTML deck before anyone sees it.

Catches the failures that survive a careless build: text spilling out of its
box, panels sitting on top of each other, type too small to read from the back
of a room, and fonts that never loaded.

Usage:
    python verify_deck.py deck.html [--shots out_dir]

Requires:
    pip install playwright && playwright install chromium
"""

import argparse
import json
import sys
from pathlib import Path

CHECK_JS = r"""
() => {
    const problems = [];
    const slides = [...document.querySelectorAll('.slide')];

    /* --- Colour maths, for the contrast check ---------------------------- */
    const toRGBA = s => {
        const m = String(s || '').match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        const p = m[1].split(',').map(parseFloat);
        return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    };
    const chan = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    const lum = c => 0.2126 * chan(c[0]) + 0.7152 * chan(c[1]) + 0.0722 * chan(c[2]);
    const blend = (fg, bg) => {           // composite fg with alpha over bg
        const a = fg[3];
        return [fg[0] * a + bg[0] * (1 - a),
                fg[1] * a + bg[1] * (1 - a),
                fg[2] * a + bg[2] * (1 - a), 1];
    };
    const ratio = (a, b) => {
        const l1 = lum(a), l2 = lum(b);
        const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
        return (hi + 0.05) / (lo + 0.05);
    };

    // Walk up compositing background colours until one is fully opaque.
    // A background-image or gradient anywhere in the chain means we cannot
    // judge, so we say so rather than guessing.
    const effectiveBg = el => {
        const stack = [];
        let node = el, image = false;
        while (node && node !== document.documentElement) {
            const cs = getComputedStyle(node);
            if (cs.backgroundImage && cs.backgroundImage !== 'none') image = true;
            const c = toRGBA(cs.backgroundColor);
            if (c && c[3] > 0) { stack.push(c); if (c[3] >= 1) break; }
            node = node.parentElement;
        }
        if (!stack.length) return { color: [255, 255, 255, 1], image };
        let base = stack[stack.length - 1];
        if (base[3] < 1) base = blend(base, [255, 255, 255, 1]);
        for (let i = stack.length - 2; i >= 0; i--) base = blend(stack[i], base);
        return { color: base, image };
    };

    // Device mockups render a phone UI at true phone scale, so their internal
    // type is legitimately small. Everything else obeys the 18px floor.
    const inDevice = el => !!el.closest('.phone, .device, [data-device]');

    // Drive slides by class only. Setting inline visibility here would
    // outrank the stylesheet and leave the deck stuck after the check runs.
    const show = (s) => {
        slides.forEach(x => x.classList.remove('active', 'visible'));
        s.classList.add('active', 'visible');
    };

    const readable = (el) => {
        const t = (el.textContent || '').trim();
        return t.length > 0 && el.offsetParent !== null;
    };

    slides.forEach((slide, i) => {
        show(slide);
        const n = i + 1;

        // 1. Content overflowing the 1920x1080 stage.
        if (slide.scrollWidth > 1921 || slide.scrollHeight > 1081) {
            problems.push({
                slide: n, kind: 'overflow',
                detail: `content is ${slide.scrollWidth}x${slide.scrollHeight}, stage is 1920x1080`
            });
        }

        const stage = slide.getBoundingClientRect();

        // 2. Elements pushed outside the slide edges.
        [...slide.querySelectorAll('*')].forEach(el => {
            if (!readable(el)) return;
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) return;
            const over = [];
            if (r.right  > stage.right  + 2) over.push('right');
            if (r.left   < stage.left   - 2) over.push('left');
            if (r.bottom > stage.bottom + 2) over.push('bottom');
            if (r.top    < stage.top    - 2) over.push('top');
            if (over.length) {
                problems.push({
                    slide: n, kind: 'out-of-bounds',
                    detail: `<${el.tagName.toLowerCase()}${el.className ? '.' + String(el.className).split(' ')[0] : ''}> past ${over.join(' and ')} edge`,
                    text: (el.textContent || '').trim().slice(0, 50)
                });
            }
        });

        // 3. Type too small to read on a projector, and text nobody can see.
        //    18px on a 1920 stage is roughly 9pt on a real slide.
        [...slide.querySelectorAll('p,li,span,div,td,th,h1,h2,h3,h4,figcaption,blockquote,text')].forEach(el => {
            if (!readable(el)) return;
            if (el.children.length > 0) return;          // only leaf text
            const cs = getComputedStyle(el);
            const size = parseFloat(cs.fontSize);

            if (size && size < 18 && !inDevice(el)) {
                problems.push({
                    slide: n, kind: 'tiny-text',
                    detail: `${size.toFixed(0)}px`,
                    text: (el.textContent || '').trim().slice(0, 50)
                });
            }

            // Contrast. This is what catches a slide that renders blank,
            // which the empty-slide check cannot see because the text is
            // present, just invisible.
            const fg = toRGBA(cs.color);
            if (!fg) return;
            if (parseFloat(cs.opacity) === 0) return;
            const bg = effectiveBg(el);
            if (bg.image) return;                        // cannot judge over an image
            const solidFg = fg[3] < 1 ? blend(fg, bg.color) : fg;
            const r = ratio(solidFg, bg.color);

            // anti-slop.md: 4.5:1 for body, 3:1 for large text at 24px and up.
            const large = size >= 24;
            const floor = large ? 3 : 4.5;
            if (r < floor) {
                problems.push({
                    slide: n,
                    kind: r < 1.5 ? 'invisible' : 'low-contrast',
                    detail: `${r.toFixed(2)}:1, needs ${floor}:1 at ${size.toFixed(0)}px`,
                    text: (el.textContent || '').trim().slice(0, 50)
                });
            }
        });

        // 4. Panels covering each other.
        //    Only real content panels are compared. Full-bleed wrappers
        //    legitimately sit on top of each other, so anything covering more
        //    than 55% of the slide is treated as a container, not a panel.
        const slideArea = stage.width * stage.height;
        const panels = [...slide.querySelectorAll(
            '.panel,.card,.stat,.lift,.quadrant,.cmp,.flip,.face.front,.tab,.stage,.tl-stop'
        )].filter(el => {
            if (!readable(el)) return false;
            const r = el.getBoundingClientRect();
            if (r.width < 40 || r.height < 40) return false;
            return slideArea === 0 || (r.width * r.height) / slideArea < 0.55;
        });

        for (let a = 0; a < panels.length; a++) {
            for (let b = a + 1; b < panels.length; b++) {
                if (panels[a].contains(panels[b]) || panels[b].contains(panels[a])) continue;
                const p = panels[a].getBoundingClientRect();
                const q = panels[b].getBoundingClientRect();
                const ox = Math.min(p.right, q.right) - Math.max(p.left, q.left);
                const oy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
                if (ox > 8 && oy > 8) {
                    const area = ox * oy;
                    const smaller = Math.min(p.width * p.height, q.width * q.height);
                    if (smaller > 0 && area / smaller > 0.15) {
                        problems.push({
                            slide: n, kind: 'overlap',
                            detail: `${Math.round(area / smaller * 100)}% of one panel is covered by another`
                        });
                    }
                }
            }
        }

        // 5. Empty slide.
        if ((slide.textContent || '').trim().length < 3 &&
            !slide.querySelector('img,svg,canvas,video')) {
            problems.push({ slide: n, kind: 'empty', detail: 'no text and no media' });
        }
    });

    // 6. Fonts.
    //
    //    getComputedStyle returns the DECLARED stack, not the family the
    //    browser actually rendered with. Reading it tells you what the CSS
    //    asked for even when the webfont never arrived. The only reliable
    //    test is document.fonts.check(), which reports whether a family is
    //    genuinely available, whether from a loaded webfont or installed
    //    locally.
    const GENERIC = new Set([
        'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui',
        'ui-serif', 'ui-sans-serif', 'ui-monospace', 'ui-rounded',
        '-apple-system', 'BlinkMacSystemFont', 'math', 'emoji', 'fangsong'
    ]);

    // First choice per element is what the design intends. If that one is
    // missing the deck renders in a fallback, which is the failure we care
    // about even when the fallback is a real font like Arial.
    const wanted = new Set();
    slides.forEach(s => [...s.querySelectorAll('*')].forEach(el => {
        if (el.children.length > 0) return;                   // leaves only
        if (!(el.textContent || '').trim()) return;           // must have text
        const stack = getComputedStyle(el).fontFamily;
        if (!stack) return;
        const first = stack.split(',')[0].replace(/["']/g, '').trim();
        if (first && !GENERIC.has(first)) wanted.add(first);
    }));

    //    document.fonts.check() is not sufficient on its own: it returns true
    //    when NO matching @font-face rule exists, because nothing is pending
    //    to load. A blocked CDN removes the rules entirely and the check
    //    reports success. So measure instead. Render a string in the family
    //    against each generic baseline; if the width never changes, the
    //    family is not really being used.
    const measure = (() => {
        const ctx = document.createElement('canvas').getContext('2d');
        const probe = 'mmmmmmmmmmlliWWWWWWQ@1';
        const baselines = ['monospace', 'sans-serif', 'serif'];
        return (name) => baselines.some(base => {
            ctx.font = `72px ${base}`;
            const plain = ctx.measureText(probe).width;
            ctx.font = `72px "${name}", ${base}`;
            return ctx.measureText(probe).width !== plain;
        });
    })();

    const fontsOk = [], fontsMissing = [];
    wanted.forEach(name => {
        let available;
        try {
            available = measure(name);
            // Belt and braces: a pending webfont can measure as absent for a
            // moment even though it will arrive.
            if (!available && document.fonts && document.fonts.check) {
                const styleSheetsHaveIt = [...document.fonts].some(
                    f => f.family.replace(/["']/g, '') === name && f.status === 'loaded'
                );
                available = styleSheetsHaveIt;
            }
        } catch (e) {
            available = true;      // cannot test, do not cry wolf
        }
        (available ? fontsOk : fontsMissing).push(name);
    });

    // Leave the deck as we found it, on slide one.
    slides.forEach((s, i) => {
        s.style.visibility = '';
        s.classList.toggle('active', i === 0);
        s.classList.toggle('visible', i === 0);
    });

    return {
        slideCount: slides.length,
        fontsOk,
        fontsMissing,
        fontsStatus: document.fonts ? document.fonts.status : 'unknown',
        problems
    };
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--shots", help="also save a PNG of every slide to this directory")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed.\n"
              "  pip install playwright && playwright install chromium")
        sys.exit(2)

    deck = Path(args.deck).resolve()
    if not deck.exists():
        print(f"No such file: {deck}")
        sys.exit(2)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(deck.as_uri())

        # Wait for the font loading pipeline to settle rather than guessing.
        # Resolves immediately when there is nothing to load, and on failure
        # too, which is what makes the missing-font check meaningful.
        try:
            page.evaluate("document.fonts.ready")
        except Exception:
            pass
        page.wait_for_timeout(600)           # first paint

        result = page.evaluate(CHECK_JS)

        if args.shots:
            out = Path(args.shots)
            out.mkdir(parents=True, exist_ok=True)
            count = page.evaluate("document.querySelectorAll('.slide').length")
            for i in range(count):
                # Use the deck's own navigation when it exposes one, so the
                # progress bar, counter and counters all update the way they
                # will for a real viewer. Fall back to classes otherwise.
                blank = page.evaluate(
                    """(i) => {
                        if (typeof deck !== 'undefined' && deck && deck.show) {
                            deck.show(i);
                        } else {
                            [...document.querySelectorAll('.slide')].forEach((x, n) => {
                                x.style.visibility = '';   // clear inline overrides
                                x.classList.toggle('active', n === i);
                                x.classList.toggle('visible', n === i);
                            });
                        }
                        const cur = document.querySelectorAll('.slide')[i];
                        return getComputedStyle(cur).visibility !== 'visible';
                    }""", i)

                if blank:
                    print(f"  ! slide {i + 1} would not become visible. "
                          f"Check that slide switching uses .active/.visible, "
                          f"not display or inline styles.")

                # Long enough for the slowest built-in animation (path draw at
                # 1.8s plus delay) to settle. A screenshot caught mid-animation
                # is worse than useless, because it looks like a broken layout.
                page.wait_for_timeout(2600)
                page.screenshot(path=str(out / f"slide-{i + 1:02d}.png"))
            print(f"Saved {count} screenshots to {out}\n")

        browser.close()

    # --- Report -----------------------------------------------------------
    problems = result["problems"]
    missing = result["fontsMissing"]

    print(f"{result['slideCount']} slides")
    status = result["fontsStatus"]
    print(f"Fonts loaded: {', '.join(result['fontsOk'][:6]) or 'none'}"
          + ("" if status == "loaded" else f"   (status: {status})"))

    if missing:
        print(f"  ! NOT AVAILABLE: {', '.join(missing)}")
        print("    The deck is rendering in a fallback, so it does not look "
              "the way it was designed.")
        print("    Usually the font CDN is blocked or you are offline. "
              "Run scripts/embed_fonts.py to bake the fonts into the file.")

    if not problems and not missing:
        print("\nNo problems found.")
        return 0

    if not problems:
        print("\nNo layout problems, but fix the fonts before delivering.")
        return 1

    by_kind = {}
    for pr in problems:
        by_kind.setdefault(pr["kind"], []).append(pr)

    print(f"\n{len(problems)} problems:\n")
    labels = {
        "invisible": "TEXT NOBODY CAN SEE. The slide renders blank",
        "low-contrast": "Text too faint against its background",
        "overflow": "Content taller or wider than the slide",
        "out-of-bounds": "Element past the slide edge",
        "tiny-text": "Text too small to read from the back",
        "overlap": "Panels covering each other",
        "empty": "Empty slide",
    }
    severity = {"invisible": 0, "low-contrast": 1, "overflow": 2,
                "out-of-bounds": 3, "overlap": 4, "tiny-text": 5, "empty": 6}

    for kind, items in sorted(by_kind.items(), key=lambda kv: severity.get(kv[0], 9)):
        print(f"  {labels.get(kind, kind)}  ({len(items)})")
        for pr in items[:6]:
            text = f'  "{pr["text"]}"' if pr.get("text") else ""
            print(f"    slide {pr['slide']}: {pr['detail']}{text}")
        if len(items) > 6:
            print(f"    ... and {len(items) - 6} more")
        print()

    if "invisible" in by_kind:
        print("The invisible text is the urgent one. Almost always a slide variant\n"
              "written as `.divider` instead of `.slide.divider`, which loses to\n"
              "`.slide` in stage.css and silently paints the theme background back on.\n")

    print("Fix these before delivering. Splitting a slide is almost always the "
          "right answer, and shrinking type never is.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
