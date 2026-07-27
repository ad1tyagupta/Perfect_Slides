#!/usr/bin/env python3
"""
Pull the content out of a document so it can become a deck.

Handles PDF, DOCX, PPTX, XLSX, CSV, Markdown and plain text. Writes a JSON
digest and saves any embedded images to an assets folder.

Usage:
    python ingest.py report.pdf out_dir/

Install what you need:
    pip install pypdf python-docx python-pptx openpyxl
"""

import csv
import json
import sys
from pathlib import Path


def _need(module, package):
    try:
        return __import__(module)
    except ImportError:
        print(f"Needs {package}.  pip install {package}")
        sys.exit(2)


# --- PDF ------------------------------------------------------------------
def read_pdf(path, assets):
    _need("pypdf", "pypdf")
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    sections = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            sections.append({"kind": "page", "index": i, "text": text})

    meta = reader.metadata or {}
    return {
        "title": (meta.get("/Title") or path.stem),
        "pages": len(reader.pages),
        "sections": sections,
    }


# --- DOCX -----------------------------------------------------------------
def read_docx(path, assets):
    _need("docx", "python-docx")
    from docx import Document

    doc = Document(str(path))
    sections, tables = [], []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = (para.style.name or "").lower()
        sections.append({
            "kind": "heading" if "heading" in style or "title" in style else "paragraph",
            "level": int(style.split()[-1]) if style.startswith("heading") and style.split()[-1].isdigit() else None,
            "text": text,
        })

    for t in doc.tables:
        rows = [[c.text.strip() for c in row.cells] for row in t.rows]
        if rows:
            tables.append({"headers": rows[0], "rows": rows[1:]})

    saved = _save_images(doc.part.package, assets, path.stem)
    return {"title": path.stem, "sections": sections, "tables": tables, "images": saved}


# --- PPTX -----------------------------------------------------------------
def read_pptx(path, assets):
    _need("pptx", "python-pptx")
    from pptx import Presentation

    prs = Presentation(str(path))
    slides, images = [], []

    for i, slide in enumerate(prs.slides, start=1):
        texts, tables = [], []

        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if text:
                    texts.append(text)

            if getattr(shape, "has_table", False):
                rows = [[c.text.strip() for c in r.cells] for r in shape.table.rows]
                if rows:
                    tables.append({"headers": rows[0], "rows": rows[1:]})

            if shape.shape_type == 13:  # PICTURE
                try:
                    img = shape.image
                    name = f"{path.stem}-s{i}-{len(images) + 1}.{img.ext}"
                    (assets / name).write_bytes(img.blob)
                    images.append(name)
                except Exception:
                    pass

        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()

        slides.append({
            "kind": "slide",
            "index": i,
            "headline": texts[0] if texts else "",
            "text": "\n".join(texts[1:]),
            "tables": tables,
            "notes": notes,
        })

    return {"title": path.stem, "sections": slides, "images": images}


# --- Spreadsheets ---------------------------------------------------------
def read_xlsx(path, assets):
    _need("openpyxl", "openpyxl")
    from openpyxl import load_workbook

    wb = load_workbook(str(path), data_only=True)
    tables = []

    for ws in wb.worksheets:
        rows = [[("" if c is None else c) for c in row]
                for row in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(str(c).strip() for c in r)]
        if rows:
            tables.append({"sheet": ws.title, "headers": rows[0], "rows": rows[1:]})

    return {"title": path.stem, "sections": [], "tables": tables}


def read_csv(path, assets):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = [r for r in csv.reader(fh) if any(c.strip() for c in r)]
    if not rows:
        return {"title": path.stem, "sections": [], "tables": []}
    return {"title": path.stem, "sections": [],
            "tables": [{"sheet": path.stem, "headers": rows[0], "rows": rows[1:]}]}


# --- Text and Markdown ----------------------------------------------------
def read_text(path, assets):
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            sections.append({"kind": "heading", "level": level,
                             "text": stripped.lstrip("#").strip()})
        else:
            sections.append({"kind": "paragraph", "text": stripped})

    return {"title": path.stem, "sections": sections}


# --- Shared ---------------------------------------------------------------
def _save_images(package, assets, stem):
    saved = []
    for part in package.iter_parts():
        name = str(part.partname)
        if "/media/" in name:
            out = assets / f"{stem}-{Path(name).name}"
            try:
                out.write_bytes(part.blob)
                saved.append(out.name)
            except Exception:
                pass
    return saved


READERS = {
    ".pdf": read_pdf, ".docx": read_docx, ".pptx": read_pptx,
    ".xlsx": read_xlsx, ".xlsm": read_xlsx, ".csv": read_csv,
    ".md": read_text, ".markdown": read_text, ".txt": read_text,
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    out = Path(sys.argv[2] if len(sys.argv) > 2 else ".")

    if not src.exists():
        print(f"No such file: {src}")
        sys.exit(2)

    reader = READERS.get(src.suffix.lower())
    if reader is None:
        print(f"Cannot read {src.suffix}. Supported: {', '.join(sorted(READERS))}")
        sys.exit(2)

    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    result = reader(src, assets)
    result["source_file"] = str(src)
    result.setdefault("images", [])
    result.setdefault("tables", [])

    digest = out / "ingested.json"
    digest.write_text(json.dumps(result, indent=2, ensure_ascii=False,
                                 default=str), encoding="utf-8")

    words = sum(len(str(s.get("text", "")).split()) for s in result["sections"])
    # Slide formats nest their tables inside sections; documents keep them
    # at the top level. Count both or the summary lies.
    tables = len(result["tables"]) + sum(len(s.get("tables", [])) for s in result["sections"])
    notes = sum(1 for s in result["sections"] if s.get("notes"))

    print(f"Read {src.name}")
    print(f"  {len(result['sections'])} sections, about {words:,} words")
    print(f"  {tables} tables, {len(result['images'])} images"
          + (f", {notes} with speaker notes" if notes else ""))
    print(f"  Digest: {digest}")
    if result["images"]:
        print(f"  Images: {assets}")
    print("\nA document is not an outline. Find the argument, then build slides "
          "for it. Do not turn 20 pages into 20 slides.")


if __name__ == "__main__":
    main()
