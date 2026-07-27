# Converting a Document

When the user has a PDF, Word file, spreadsheet or existing PowerPoint.

```bash
pip install pypdf python-docx python-pptx openpyxl
python scripts/ingest.py report.pdf out_dir/
```

Writes `out_dir/ingested.json` with sections, tables, images and any speaker
notes, and saves embedded images to `out_dir/assets/`.

---

## A document is not an outline

The most common failure in the whole tool. Twenty pages become twenty slides,
each one a paragraph shrunk to fit, and the result is unreadable and unpresentable.

A document and a deck do different jobs. A document argues in sentences and
supports being re-read. A deck argues in headlines and supports a person talking.

**Read the whole thing. Find the argument. Then build slides for the argument.**
The document is source material, not a structure.

A thirty-page report usually becomes twelve to eighteen slides, and about a third
of the content does not survive. That is correct.

---

## After extracting

1. **Read all of it.** Not the headings. The whole digest.
2. **Find the argument.** What is this document claiming, and what supports it?
   Documents often bury the conclusion in the middle.
3. **Find the evidence worth showing.** Tables and figures usually become the best
   slides, because they are already the parts that carry weight.
4. **Find what to cut.** Methodology, caveats, background everyone knows,
   anything repeated. Some of it belongs in an appendix. Most of it goes.
5. **Rewrite everything.** Document prose does not belong on a slide. Apply
   `references/writing/voice.md` from scratch.

---

## Confirm before outlining

Show the user what you found, in one turn, before designing anything:

- What the document appears to be arguing
- The sections you plan to keep, and roughly what each becomes
- What you plan to cut, and why
- Tables and figures you want to turn into charts
- Anything that looked out of date or unsourced

Getting the cuts wrong is the expensive mistake. People are usually attached to
material you were planning to drop, and it is cheaper to find out now.

---

## Tables become charts

Extracted tables are the best raw material in most documents. A table of six rows
and three columns is usually a bar chart that takes two seconds to read instead of
twenty.

Keep it a table only when the individual values matter, when readers will compare
specific cells, or when the deck is a reference document.

See `references/components/data-viz.md`.

---

## Converting an existing PowerPoint

Extraction gives you slide text, tables, images and speaker notes.

Do not rebuild it slide for slide. The old deck's structure is usually the thing
the user wants improved, even when they only asked for a redesign. If the
headlines are topics rather than findings, say so and offer to rewrite them.

Ask whether they want a faithful port or a genuine rebuild, and ask it at intake
rather than after.

Images come out at their original resolution. Check them before reuse. Logos and
screenshots dragged into an old deck are often 400px wide and will look soft at
1920.

---

## Scanned PDFs

If a PDF returns almost no text, it is scanned images rather than text. The
script cannot read it.

Tell the user plainly and offer the options: run it through OCR first, send the
original file, or paste the content directly. Do not guess at content from
filenames.
