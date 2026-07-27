# Reference Templates

Drop real decks here to teach the tool. Consulting templates, pitch decks you
admire, anything with layouts worth learning from.

```
templates/
  consulting/     structured evidence, action titles, dense grids
  pitch/
  marketing/
  <your-own>/
```

Any format: `.pptx`, `.pdf`, `.key` exported to PDF, or screenshots.

---

## Reading a template into the tool

Do not copy a template slide for slide. Extract what makes it work, then write it
down where the tool will find it.

1. **Extract it.**
   ```bash
   python scripts/ingest.py templates/consulting/deck.pptx out/
   ```

2. **Look at the layouts, not the content.** How much fits on a page before it
   feels crowded. Where the source line sits. How the action title relates to the
   evidence below it. What the margins are. How charts are labelled.

3. **Write the findings into the right file:**

   | What you learned | Where it goes |
   |---|---|
   | A recurring slide layout | `references/components/catalog.md` |
   | Argument structure or slide order | `references/narrative/<type>.md` |
   | Palette, type scale, spacing rhythm | `references/design/presets.md` + `style-index.json` |
   | Chart conventions | `references/components/data-viz.md` |
   | Headline patterns | `references/writing/voice.md` |

4. **Add a preset** if the template has a coherent visual system worth reusing.
   Give it a `pptx_safe` flag and a PowerPoint reduction, like every other preset.

---

## What to look for in consulting decks

The things that are hard to work out without seeing real examples:

- **Density.** How many supporting points fit before a slide feels heavy. This is
  the hardest thing to judge from principles alone.
- **The action title.** How long it runs, where it sits, how it relates to the
  chart underneath.
- **Source lines.** Wording, placement, size.
- **Chart restraint.** How few colours, how labels are placed, when a legend is
  dropped.
- **The takeaway box.** Whether they use one, and when.
- **Appendix handling.** What gets pushed back and how it is referenced.

---

## Licensing

Keep templates out of the public repository unless you have the right to publish
them. Firm templates are usually confidential.

Add `templates/` to `.gitignore` if that applies, and keep the extracted design
rules in `references/` instead. The rules are what the tool needs. The original
files are only the source you read them from.
