# Intake

The questioning phase. Runs before any slide is designed or written.

## The rule: two checkpoints, never more

Every turn costs the user a full replay of the conversation. Questions are not
free, and a tool that drips them one at a time is an expensive tool.

So the entire intake is **two** interaction points:

| | What happens |
|---|---|
| **Checkpoint 1** | Every question that can be asked without knowing another answer. One turn. |
| *(work)* | Ingest, research, outline, and render style previews — no user contact |
| **Checkpoint 2** | One consolidated approval: findings + outline + style options together |
| *(build)* | Generate the deck |

Anything you failed to ask at Checkpoint 1 does **not** become a third
checkpoint. Make a sensible assumption, build, and state the assumption in the
delivery note. A flagged assumption the user can correct afterwards costs one
turn; stopping mid-build to ask costs one turn *and* stalls the work.

---

## Rule 0: never ask what the user already told you

Read the opening request and extract every answer it already contains. Ask only
for what is genuinely missing.

If someone opens with *"build me a 12-slide HTML pitch deck for seed investors
about our logistics API, here's my data"* — that answers format, length, deck
type, audience, topic and content source. Ask nothing. Confirm your reading in
one line and go straight to the work.

If only two or three answers are missing, ask only those. Checkpoint 1 is a
maximum, not a script.

---

## Checkpoint 1 — everything, at once

Ask as one batch: six questions plus a catch-all.

### Working within a question-UI cap

Most structured-question pickers cap out, commonly at four questions. Claude
Code does. **The cap limits the picker, not the turn.** Splitting across two
turns to fit the widget breaks the rule that matters.

Put the multiple-choice questions in the picker and the free-text ones in the
same message:

| Picker (fixed options) | Message body (free text) |
|---|---|
| Q1 Output format | Q2 Topic |
| Q3 Deck type | Q4 Audience and occasion |
| Q5 Content source | Q6 Research scope |
| Q7 Style source | Q8 Anything else |

That is four in the picker, which fits the common cap exactly, and four written
out. One turn.

If the host has no picker at all, send everything as one numbered list. If the
cap is smaller than three, move Q3 and Q5 into the body too. The order of
preference is always: keep it to one turn first, use the widget second.

### Q1. Output format

**Ask this first — it gates every downstream decision.** Available style
presets, component vocabulary and charting approach all branch on the answer.

Do not just list options. Show the tradeoff in the message body, because most
people have not thought about it and will otherwise pick from habit:

> **HTML** — a single self-contained file that opens in any browser.
>
> - Full motion: staggered reveals, drawing lines, counting numbers, animated charts
> - Genuinely interactive: clickable tabs, flip cards, charts that respond to hover
> - Pixel-identical on every machine — no font substitution, nothing shifts
> - Shareable as a link that works on phones
> - You present from a browser, and the recipient can't edit it without touching code
>
> **PowerPoint** — a real .pptx of native, editable shapes.
>
> - Anyone can open and edit it in PowerPoint, Keynote or Google Slides
> - Fits institutional workflows — clients, professors and review cycles expect it
> - Runs offline on any conference-room machine, and merges into a bigger deck
> - Motion is limited to PowerPoint's own entrance effects, and nothing is interactive
> - Fonts substitute if the viewer doesn't have them installed
>
> **Both** — the HTML deck to present from, the .pptx to hand over afterwards.

Options: `HTML` / `PowerPoint (.pptx)` / `Both`

**When the user is unsure, ask what happens after they present.** Presenting
live and sharing a link → HTML. Someone else needs to edit it, or it enters a
client or academic review cycle → PowerPoint. Both → Both.

If they pick PowerPoint or Both, state once — here, not at delivery — that the
PowerPoint version trades motion and interactivity for editability, and that
interactive components appear in their resolved state.

### Q2. Topic

Free text. Push for one specific sentence, not a subject area. *"Q3 retention
fell and here's the recovery plan"* produces a far better deck than
*"retention."* The first has an argument; the second is a category.

### Q3. Deck type

Selects the narrative framework from `references/narrative/`. Decides structure,
argument shape and citation convention — not decoration.

Options: `Pitch deck` / `Consulting` / `Marketing plan` / `Campaign` /
`Research findings` / `Talk, teaching or internal update`

Two of these split again once you know how the deck gets used, and
`narrative/index.md` decides which side. Consulting splits into roadshow,
presented live and chart-led, and working deck, circulated and dense: the
densities differ eightfold. The last option covers three frameworks, picked from
the audience answer in Q4.

If none fit, take the free-text answer, pick the closest framework, and say
which one you chose and why. `narrative/scenarios.md` carries ready slide orders
for around twenty specific situations, such as a quarterly business review or a
competitor analysis.

### Q4. Audience and occasion

Free text. Who is in the room, and what is the setting? Drives tone, density and
how much context to assume. *"Seed investors, 20-minute slot, they've seen 40
decks this week"* and *"internal engineering team, weekly sync"* produce
different decks from the same topic.

### Q5. Content source

- **I have the content** — notes, a doc, or a rough outline
- **I have a document to convert** — PDF, DOCX, PPTX, MD or spreadsheet
- **Research it for me** — the agent gathers and cites the material
- **Mix** — some material exists, gaps need research

### Q6. Research scope *(only if Q5 involves research)*

Ask it now rather than after Q5 comes back — it is the one dependent question
worth pre-empting, because asking it later costs a whole turn.

Phrase it as: *"If I'm researching, what should I focus on, and is anything
off-limits or already settled?"* If they leave it blank, scope it yourself from
the topic and deck type, and state your scope at Checkpoint 2.

### Q7. Style source

Multiple choice, so it belongs in the picker.

> Do you want a built-in style, or should the deck be styled after a company
> whose design you like?

Options: `Built-in style` / `Match a company` / `You choose`

`Built-in style` and `You choose` go to `design/style-index.json`. `Match a
company` goes to `design/brand-index.json`, then `design/brands.md` for the
translation rules. If they name a company unprompted anywhere in their answers,
treat that as `Match a company` and do not ask.

Either way the user never describes an aesthetic in words. They pick from three
rendered title slides at Checkpoint 2.

### Q8. Anything else — the catch-all

One optional free-text field. This exists specifically to pre-empt follow-ups,
so name the things that would otherwise become one:

> Anything else I should know? For example: brand colours, a logo or fonts to
> match · the language it should be in · specific numbers or claims that must
> appear · images or assets you have · whether you need speaker notes · how long
> the talk is · where you're presenting it (a washed-out projector rules out
> some palettes) · anything to avoid.

Blank is a fine answer. Every item here has a defensible default, and defaults
get applied silently and flagged at delivery rather than chased with a question.

---

## Between the checkpoints — no user contact

Do all of it before speaking again:

1. **Ingest** any supplied document → `references/workflow/ingest.md`
2. **Research** to the confirmed scope → `references/workflow/research.md`, maintaining `sources.json`
3. **Infer** slide count and density from Q3 + Q4 — do not ask, the table below is the starting point
4. **Outline** the deck against its narrative framework
5. **Render** three title-slide style previews, from `design/style-index.json`
   or `design/brand-index.json` depending on the Q7 answer

If the format is PowerPoint or Both, only offer presets whose PPTX reduction
holds up. Never show a style in HTML that the .pptx cannot honour — the user
picks based on what they saw.

### Inferred length and density

| Deck type | Slides | Density |
|---|---|---|
| Pitch deck | 10–15 | Low — one idea per slide |
| Consulting / analysis | 15–25 | High — self-contained, sourced |
| Marketing / campaign | 8–15 | Medium |
| Conference talk | 15–30 | Low — big type, fast pacing |
| Internal update | 5–12 | Medium-high |
| Teaching / tutorial | 15–25 | Medium — built to be revisited |

A live audience pushes density down; async circulation pushes it up. If the deck
is both presented *and* circulated, design for the room and let speaker notes
carry the rest. Do not split the difference and serve neither.

Talk length beats slide count when the user gave it: roughly a minute a slide
for low density, two for high.

---

## Checkpoint 2 — one consolidated approval

Everything in a single turn, in this order:

1. **What I found** — the research digest with sources, or a summary of the
   ingested document. Lead with this: it carries the premise, and a wrong
   premise invalidates everything below it.
2. **Assumptions I made** — anything defaulted from a blank Q7, stated plainly
   so it can be corrected in the same reply.
3. **The outline** — numbered slide titles, a phrase each on what they carry.
4. **Three style previews** — rendered title slides, opened for the user.

Ask for one reply covering all four. Make it easy to reject cheaply: *"If the
premise is off, say so and ignore the rest — I'll redo the outline."*

Then build.

---

## When breaking the two-checkpoint rule is correct

Rare, and only when proceeding under any assumption would waste the whole deck:

- Research contradicts the premise outright — the product launched, the deal
  closed, the number is off by an order of magnitude
- A supplied document is unreadable, or is about something else entirely
- The request needs information only the user has, with no defensible default —
  unshared financials, an internal decision, a name you cannot verify

Everything else: assume, build, flag.
