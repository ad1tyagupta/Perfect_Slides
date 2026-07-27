# Perfect Slides

Build presentations people remember. HTML decks with real motion, PowerPoint
files anyone can edit, or both.

Works in any coding agent. Read this file, then load only the reference files
the current job needs.

---

## What this tool is for

Three jobs:

- **Build a deck from scratch**, researching the content if the user does not have it
- **Turn a document into a deck** from a PDF, Word file, spreadsheet or existing PowerPoint
- **Improve a deck** that already exists

---

## Non-negotiables

Break any of these and the output stops being worth using.

1. **Never start building before intake is finished.** Read
   `references/workflow/intake.md` first, every time.
2. **Two checkpoints with the user, no more.** Questions in one batch, then one
   consolidated review. Anything you forgot to ask becomes a stated assumption,
   not a third round of questions.
3. **Show data, do not describe it.** Before writing a sentence about a number,
   check `references/components/data-viz.md` for a way to show it.
4. **Headlines state the finding, not the topic.** "Revenue fell 12% in Q3",
   never "Q3 Revenue Overview".
5. **Every component needs a PowerPoint fallback.** Nothing goes on a slide that
   cannot degrade honestly. See `references/components/catalog.md`.
6. **Fixed 1920x1080 stage.** Slides scale as one unit and never reflow.
7. **Verify before delivering.** Run `scripts/verify_deck.py`. Do not tell the
   user it is done until it passes.
8. **Follow the writing rules.** `references/writing/voice.md` is not optional
   styling. No em dashes, no filler words, no repetition.

---

## The flow

```
Intake  ──►  Gather  ──►  Outline + style  ──►  Build  ──►  Verify  ──►  Deliver
  ▲                              ▲
  └── checkpoint 1               └── checkpoint 2
```

### 1. Intake
Read `references/workflow/intake.md`. Ask everything in one batch. Format first,
because it decides everything downstream.

### 2. Gather
- User has content → read all of it before outlining
- Document to convert → `references/workflow/ingest.md`
- Needs research → `references/workflow/research.md`, keeping `sources.json`

### 3. Outline and style
Read `references/narrative/index.md`, pick the deck type, then load only that
one framework. Check `scenarios.md` for a matching slide order. Outline
against it, at the density the framework states. Render three title-slide previews from `references/design/`.

Present findings, assumptions, outline and previews together. One reply approves
all four.

### 4. Build

**HTML** → `references/output/html.md`
Include `references/components/stage.css` and `references/components/deck.js`
in full. Pull markup from `data-viz.md` and `interactive.md`.

**PowerPoint** → `references/output/pptx.md`
Write `deck.json`, then run:
```
python scripts/build_pptx.py deck.json out.pptx
```

**Both** → write `deck.json` first as the shared content spine, then author the
HTML from it. Same content, two honest expressions.

### 5. Verify
```
python scripts/verify_deck.py deck.html --shots ./shots
```
Fix everything it reports, including any font reported as not available. Splitting a slide is almost always the right answer.
Shrinking type never is.

For PowerPoint, open the file and confirm charts are native and text is real.

If the user will present the HTML deck somewhere wifi is not guaranteed, run
`python scripts/embed_fonts.py deck.html` so the fonts travel with the file.

Before adding user images, run `python scripts/process_images.py assets/` to
catch anything oversized or too small to stay sharp at 1920x1080.

### 6. Deliver
Say where the file is, how to navigate it, and what you assumed. Mention that
pressing `E` lets them edit any text in the browser, so small wording fixes cost
them nothing. Offer `scripts/deploy.sh` if they want a link to share. If a font was
substituted in the .pptx, say so now rather than letting them find out in front
of a client.

---

## Reference map

Load only what the job needs.

| File | Read when |
|---|---|
| `workflow/intake.md` | Always, first |
| `workflow/research.md` | The user wants research |
| `workflow/ingest.md` | Converting a document |
| `narrative/index.md` | Always, to pick the deck type and its density |
| `narrative/<type>.md` | Only the one type you picked |
| `narrative/scenarios.md` | The request matches a specific situation, such as a QBR |
| `writing/voice.md` | Before writing any copy |
| `design/style-index.json` | Choosing a built-in style |
| `design/brand-index.json` | The user wants a deck styled after a company |
| `design/brands.md` | After a brand is chosen |
| `design/anti-slop.md` | Before designing anything |
| `components/catalog.md` | Choosing what goes on a slide |
| `components/data-viz.md` | Any number, chart or table |
| `components/diagrams.md` | Process, cycle, pyramid, funnel, hierarchy |
| `components/consulting-page.md` | Building a dense consulting page |
| `components/interactive.md` | HTML decks only |
| `output/html.md` | Building HTML |
| `output/pptx.md` | Building PowerPoint |
| `writing/languages.md` | Any deck not in English |
| `requirements.txt` | A script reports a missing dependency |

---

## Navigation built into every HTML deck

| Key | Does |
|---|---|
| Arrows, space, swipe, scroll | Move between slides |
| `F` | Fullscreen |
| `P` | Presenter view with notes, next slide and a timer |
| `Home` / `End` | First and last slide |

`deck.html#7` opens on slide 7.

---

## When the user asks for something that will look bad

Say so once, in a sentence. Offer the better option. If they repeat the request,
build it their way without further comment. It is their deck.
