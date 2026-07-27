# Building PowerPoint

Write a `deck.json`, run the builder, get a .pptx of real editable shapes.

```bash
pip install python-pptx
python scripts/build_pptx.py deck.json out.pptx
```

Nothing in the output is a screenshot. Charts carry their data inside the file,
so a client can correct a number without rebuilding the slide. Text is real text,
so it is searchable, translatable and readable by a screen reader.

---

## Design for PowerPoint from the start

The most common failure is designing a beautiful HTML slide and then flattening
it. Reduced versions of interactive ideas read as compromises, because they are.

If the format is PowerPoint, do not put a flip card in the outline at all. Design
the two-panel slide directly. It will be better than a flattened flip card.

What survives, and what does not:

| Works well | Avoid |
|---|---|
| Bold type, strong colour blocks | Blur, glass, backdrop filters |
| Native charts and tables | Custom SVG illustration |
| Simple entrance animations | Anything hover or click driven |
| Solid and linear gradient fills | Layered radial gradient meshes |
| Photos and vector shapes | 3D transforms |
| Generous spacing | Fine hairline detail under 1pt |

---

## deck.json

```json
{
  "meta": {
    "title": "Checkout recovery",
    "author": "Aditya Gupta",
    "date": "July 2026",
    "language": "en",
    "deck_type": "consulting"
  },
  "theme": {
    "colors": {
      "bg": "#0E2635", "ink": "#EAF4F8", "accent": "#00A8D8",
      "muted": "#8FB2C0", "panel": "#173B4F", "on_accent": "#062130"
    },
    "fonts": {
      "display": "Fraunces", "display_safe": "Georgia",
      "body": "Satoshi", "body_safe": "Calibri"
    }
  },
  "slides": [ … ]
}
```

**`display_safe` and `body_safe` are what the .pptx actually uses.** Name
something the recipient is likely to have installed. A gorgeous font the viewer
lacks becomes whatever PowerPoint picks, and that is usually worse than choosing
a good common font yourself.

For non-Latin scripts see the safe-font table in
`references/writing/languages.md`. Substitution is far uglier outside Latin.

---

## Slide types

Every slide takes `headline`, and optionally `kicker`, `subhead`, `source` and
`notes`. `notes` becomes real PowerPoint speaker notes.

### title
```json
{ "layout": "title", "kicker": "Quarterly review",
  "headline": "Checkout is where the revenue leaks",
  "subhead": "Three fixes recover more than a quarter of acquisition spend." }
```

### section
Divider between parts of the argument. Fills the slide with the accent colour.
```json
{ "layout": "section", "headline": "Recommendation",
  "subhead": "Ship the fix before the autumn campaign." }
```

### statement
One sentence, full slide. The line you want remembered.
```json
{ "layout": "statement",
  "headline": "We lose 8% of carts to a bug we have known about since March.",
  "source": "Source: checkout logs, Mar to Jun 2026. n = 4,812." }
```

### stats
Up to three figures. More than three and none of them land.
```json
{ "layout": "stats", "headline": "Three numbers frame the problem",
  "body": { "items": [
    { "value": "8%", "label": "of carts abandoned at payment" },
    { "value": "€142k", "label": "annualised revenue at risk" }
  ] } }
```

### chart
Native PowerPoint chart with editable data.
```json
{ "layout": "chart", "headline": "Abandonment rose every month since March",
  "body": {
    "chart": "line",
    "categories": ["Jan", "Feb", "Mar", "Apr"],
    "series": [{ "name": "Abandonment rate", "values": [3.1, 3.0, 4.8, 6.2] }]
  },
  "source": "Source: checkout logs." }
```

`chart` accepts `bar`, `hbar`, `line`, `pie`, `donut`, `area`.

One series gets no legend, because the headline already says what it is. Pie and
donut take five slices maximum. Past that use `bar`.

### table
```json
{ "layout": "table", "headline": "Fixing checkout beats raising spend",
  "body": {
    "headers": ["Option", "Cost", "Recovered", "Time"],
    "rows": [["Fix checkout", "€12k", "€142k", "3 weeks"]]
  } }
```
Eight rows and four columns is the readable ceiling.

### bullets
```json
{ "layout": "bullets", "headline": "What we need from you today",
  "body": { "points": ["Approve three weeks of engineering time"] } }
```
Six points maximum. Ten words each. If it needs more, it is two slides.

### cards
Two to six parallel items of equal weight.
```json
{ "layout": "cards", "headline": "Three fixes, in shipping order",
  "body": { "cards": [
    { "title": "Payment iframe", "detail": "Replace the deprecated handler." }
  ] } }
```

### timeline
```json
{ "layout": "timeline", "headline": "Three weeks to full recovery",
  "body": { "events": [{ "when": "Week 1", "what": "Payment iframe" }] } }
```
Three to six events. More becomes unreadable across the slide.

### quote
```json
{ "layout": "quote",
  "body": { "quote": "I tried three times and bought it somewhere else.",
            "attribution": "Customer interview, 14 June 2026" } }
```

### image
```json
{ "layout": "image", "headline": "The error customers actually see",
  "body": { "path": "assets/error.png", "full_bleed": false },
  "subhead": "No message, no retry, no way back to the cart." }
```
`full_bleed: true` fills the slide and lays the headline over a band at the
bottom.

---

## After building

1. **Open the file.** Confirm the charts are charts and the text is selectable.
2. **Check the fonts.** The builder prints any substitution it made. Pass that on.
3. **Check the notes.** Speaker notes should be in the notes pane, not on slides.

If the user also asked for HTML, build both from this same `deck.json`. It is the
content spine, and using it for both is what keeps them from drifting apart.

---

## Known limits

Say these plainly rather than letting the user discover them.

- **No hover or click behaviour.** PowerPoint has no equivalent.
- **Entrance animations only.** The builder does not yet write PowerPoint
  animation timing, so slides arrive fully composed.
- **Funnels, matrices and process diagrams are grouped shapes**, not charts.
  Editable, but not data-driven.
- **Gradients are flat fills.** Layered gradient backgrounds do not translate.
