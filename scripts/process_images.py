#!/usr/bin/env python3
"""
Prepare images for a deck.

Shrinks oversized photos, crops logos to circles, and reports anything that will
look soft at 1920x1080. A 4MB phone photo does not belong in a slide deck, and a
400px logo will look blurry on a projector.

Usage:
    python process_images.py assets/                 # report only, changes nothing
    python process_images.py assets/ --resize        # shrink anything oversized
    python process_images.py assets/logo.png --circle
    python process_images.py assets/ --resize --max 1600

Originals are never overwritten. Output gets a _deck suffix.

Requires:
    pip install Pillow
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageOps
except ImportError:
    print("Needs Pillow.\n  pip install Pillow")
    sys.exit(2)

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}

# A full-bleed image spans the 1920px stage. Anything much larger is wasted
# bytes; anything much smaller will visibly soften when scaled up.
STAGE_W = 1920
SOFT_BELOW = 900          # width under which a half-slide image looks soft
FAT_ABOVE_KB = 900        # file size worth flagging


def out_path(p, tag):
    return p.with_name(f"{p.stem}_{tag}{p.suffix}")


def resize(p, max_dim, quality=88):
    img = Image.open(p)
    img = ImageOps.exif_transpose(img)          # honour phone rotation
    if max(img.size) <= max_dim:
        return None

    before = p.stat().st_size / 1024
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    dst = out_path(p, "deck")

    if dst.suffix.lower() in {".jpg", ".jpeg"}:
        img.convert("RGB").save(dst, quality=quality, optimize=True)
    else:
        img.save(dst, optimize=True)

    after = dst.stat().st_size / 1024
    return dst, before, after, img.size


def circle(p):
    """Square crop with a circular alpha mask. For logos on rounded aesthetics."""
    img = Image.open(p).convert("RGBA")
    img = ImageOps.exif_transpose(img)
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w - side) // 2 + side, (h - side) // 2 + side))

    # Supersample the mask so the edge is not jagged.
    scale = 4
    mask = Image.new("L", (side * scale, side * scale), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, side * scale, side * scale], fill=255)
    mask = mask.resize((side, side), Image.LANCZOS)

    img.putalpha(mask)
    dst = out_path(p, "circle").with_suffix(".png")
    img.save(dst)
    return dst


def inspect(p):
    try:
        img = Image.open(p)
        img = ImageOps.exif_transpose(img)
    except Exception as e:
        return {"path": p, "error": str(e)[:60]}
    return {
        "path": p,
        "size": img.size,
        "kb": p.stat().st_size / 1024,
        "mode": img.mode,
        "alpha": img.mode in ("RGBA", "LA") or "transparency" in img.info,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="an image, or a folder of images")
    ap.add_argument("--resize", action="store_true", help="shrink anything oversized")
    ap.add_argument("--circle", action="store_true", help="crop to a circle")
    ap.add_argument("--max", type=int, default=STAGE_W, help="longest edge, default 1920")
    ap.add_argument("--deck", help="only report images this HTML deck actually "
                                   "references, so working files are ignored")
    args = ap.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"No such path: {target}")
        sys.exit(2)

    files = ([target] if target.is_file()
             else sorted(f for f in target.rglob("*")
                         if f.suffix.lower() in EXTS
                         and not f.name.startswith(".")
                         and not any(tag in f.stem for tag in
                                     ("_deck", "_circle", "_processed", "_orig"))))

    # Scoping to a deck stops every stray working file in assets/ being
    # reported as a problem when nothing on a slide points at it.
    if args.deck:
        deck = Path(args.deck)
        if not deck.exists():
            print(f"No such deck: {deck}")
            sys.exit(2)
        html = deck.read_text(encoding="utf-8", errors="replace")
        used = {f for f in files if f.name in html}
        skipped = len(files) - len(used)
        files = sorted(used)
        if skipped:
            print(f"Ignoring {skipped} images {deck.name} does not reference.\n")

    if not files:
        print(f"No images found in {target}")
        sys.exit(0)

    print(f"{len(files)} images\n")
    warnings, total_saved = [], 0

    for f in files:
        info = inspect(f)
        if "error" in info:
            print(f"  ! {f.name}: {info['error']}")
            continue

        w, h = info["size"]
        note = []
        if max(w, h) > args.max:
            note.append("oversized")
        if w < SOFT_BELOW:
            note.append("will look soft")
        if info["kb"] > FAT_ABOVE_KB:
            note.append("heavy")

        flag = "  <- " + ", ".join(note) if note else ""
        print(f"  {f.name[:42]:<44} {w}x{h}  {info['kb']:>6.0f} KB{flag}")

        if note and "will look soft" in note:
            warnings.append(f"{f.name} is {w}px wide. Below about {SOFT_BELOW}px it "
                            f"softens noticeably when scaled onto a 1920px slide.")

        if args.circle:
            dst = circle(f)
            print(f"      circle -> {dst.name}")

        if args.resize:
            r = resize(f, args.max)
            if r:
                dst, before, after, newsize = r
                total_saved += before - after
                print(f"      resized -> {dst.name}  {newsize[0]}x{newsize[1]}  "
                      f"{before:.0f} KB -> {after:.0f} KB")

    if total_saved:
        print(f"\nSaved {total_saved / 1024:.1f} MB. Point the deck at the _deck files.")

    if warnings:
        print("\nWorth telling the user:")
        for w in warnings:
            print(f"  - {w}")

    if not args.resize and not args.circle:
        print("\nReport only. Add --resize to shrink, --circle to crop a logo.")


if __name__ == "__main__":
    main()
