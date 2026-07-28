# Intake

The questioning phase. Runs before any slide is designed or written.

## The rule: two checkpoints, never more

Every turn costs the user a full replay of the conversation. Questions are not
free, and a tool that drips them one at a time is an expensive tool.

| | What happens |
|---|---|
| **Checkpoint 1** | Every question that can be asked without knowing another answer. One turn. |
| *(work)* | Ingest, research, outline, render style previews. No user contact |
| **Checkpoint 2** | One consolidated approval: findings, assumptions, outline, style options |
| *(build)* | Generate the deck |

Anything you failed to ask at Checkpoint 1 does **not** become a third
checkpoint. Make a sensible assumption, build, and state it in the delivery
note. A flagged assumption the user corrects afterwards costs one turn. Stopping
mid-build to ask costs a turn *and* stalls the work.

---

## Rule 0: never ask what the user already told you

Read the opening request and extract every answer it already contains.

If someone opens with *"build me a 12-slide HTML pitch deck for seed investors
about our logistics API, here's my data"* that answers format, length, deck type,
audience, topic and content source. Ask nothing. Confirm your reading in one line
and go straight to the work.

**Mine the request hardest for the topic.** It is the one answer that cannot be
defaulted, and it is almost always already in the first message even when
nothing else is. If you can state the topic in a sentence from what the user
wrote, do not ask for it.

If only two or three answers are missing, ask only those. Checkpoint 1 is a
maximum, not a script.

---

## Checkpoint 1 — everything, at once

Four questions in the picker, four written out. **Both halves must be
answerable without a follow-up**, which drives every rule below.

### Two failure modes to design against

**People answer the picker and skim the prose.** When a structured widget
appears, the surrounding text reads as preamble. That is predictable, not a user
error. So:

- Open the message with the written questions, **before** describing the picker
- Number them, and mark the topic as required
- State in bold that there are questions in both places

**A picker option that needs a follow-up guarantees a third turn.** "Match a
company" with no company named is a dead end. Every option must be phrased so
the reply carries what it needs:

> ✗ Match a company
> ✓ Match a company (name it in your reply)

---

### The written half — put these first

Send these above the picker, numbered:

> **1. What is the presentation about?** One specific sentence, not a subject.
> *Required.* "Q3 retention fell and here is the recovery plan" produces a far
> better deck than "retention". The first has an argument, the second is a category.
>
> **2. Who is the audience, and what is the occasion?** Drives tone, density and
> how much context to assume.
>
> **3. What language?** English unless you say otherwise. Any language works,
> including right to left and Chinese, Japanese or Korean.
>
> **4. Anything else?** Optional. A logo or images you have, numbers or claims
> that must appear, how long the talk is, where you are presenting it, anything
> to avoid.
>
> **If you chose "research it" below, also tell me what to focus on and anything
> that is off-limits or already settled.**

Then, in bold, immediately before the picker:

> **There are four more questions in the picker below. Please answer both parts.**

### Q1. Format and sharing

Ask this first. It gates the available styles, the component vocabulary and the
charting approach. Sharing is folded in here rather than raised at delivery,
because a shareable link needs a one-time signup and the end of the conversation
is the worst moment to discover that.

Show the tradeoff in the message body. Most people have not thought about it and
will otherwise pick from habit.

> **HTML** — one self-contained file that opens in any browser.
>
> - Full motion: staggered reveals, drawing lines, counting numbers
> - Genuinely interactive: flip cards, tabs, charts that respond to hover
> - Presenter view with your notes, the next slide and a timer
> - You can edit any text in the browser afterwards
> - You present from a browser, and nobody can edit it without touching code
>
> **PowerPoint** — a real .pptx of native, editable shapes.
>
> - Anyone can edit it in PowerPoint, Keynote or Google Slides
> - Charts keep their data inside the file, so a client can correct a number
> - Runs offline anywhere and merges into a bigger deck
> - Motion is limited to entrance effects, and nothing is interactive
> - Fonts substitute if the viewer does not have them installed

Options:

- `HTML`
- `HTML plus a shareable link` (free Vercel account, one signup during the build)
- `PowerPoint (.pptx)`
- `Both HTML and PowerPoint`

**When the user is unsure, ask what happens after they present.** Presenting live
and sharing a link → HTML. Someone else must edit it, or it enters a client or
academic review → PowerPoint. Both → Both.

If they pick PowerPoint or Both, say once, here rather than at delivery, that the
PowerPoint version trades motion and interactivity for editability.

If they pick the shareable link, run `scripts/deploy.sh` during the build phase
so the signup happens while they are waiting, not after handover.

### Q2. Deck type

Four broad options, because pickers commonly cap at four choices per question as
well as four questions. `narrative/index.md` narrows to the exact framework using
the audience answer.

- `Pitch or sales`
- `Consulting, analysis or research`
- `Marketing plan or campaign`
- `Talk, teaching or internal update`

Narrowing, once you have the audience:

| They picked | Splits into |
|---|---|
| Pitch or sales | `pitch-deck.md`, plus `scenarios.md` for a sales deck or proposal |
| Consulting, analysis or research | `consulting-roadshow.md` if presented live, `consulting-working.md` if circulated, `research.md` if the method matters as much as the answer |
| Marketing plan or campaign | `marketing-plan.md` for a quarter of strategy, `campaign.md` for one creative idea |
| Talk, teaching or internal update | `conference.md`, `teaching.md` or `internal.md` |

Say which framework you chose and why, in one line at Checkpoint 2.
`scenarios.md` has ready slide orders for twenty more specific situations.

### Q3. Content source

Every option carries what it needs.

- `I have the content, in my reply` — pasted, or a path
- `Research it for me`
- `A document to convert, path in my reply` — PDF, DOCX, PPTX, XLSX, MD
- `Some of each, I will explain in my reply`

### Q4. Style

Options:

- `Choose for me`
- `A built-in style, named in my reply`
- `Match a company, named in my reply`
- `My own brand colours, in my reply`

**Show the options in the message body.** Nobody can choose from a library they
cannot see, and every option except the first is otherwise a dead end. List them
compactly:

> **Built-in styles.** Night Ride (deep navy, electric accent) · Signal Brief
> (warm paper and navy, institutional) · Broadsheet (white, black, one red mark)
> · Blueprint (technical grid, precise) · Sunrise (warm cream and terracotta) ·
> Graphite (near-black, one hot accent) · Studio (bold colour blocks) · Clinic
> (white, restrained, nothing decorative)
>
> **Or styled after a company.** Linear · Vercel · Stripe · Notion · Claude ·
> Apple · IBM · Figma · Airbnb · Wise · Revolut · Slack · Shopify · WIRED ·
> MongoDB · Raycast · Nike · Uber · Mastercard · BMW
>
> Forty-five more are available by name. **Any other company also works** —
> name it and the palette gets built from their public brand colours.

Never render a style name on a preview slide. Style names belong in the message.

---

## Between the checkpoints — no user contact

1. **Ingest** any supplied document → `workflow/ingest.md`
2. **Research** to the confirmed scope → `workflow/research.md`, keeping `sources.json`
3. **Infer** slide count and density from the framework. Do not ask
4. **Outline** against the framework
5. **Render** three title-slide previews, from `design/style-index.json`,
   `design/brand-index.json`, or built from brand colours per `design/brands.md`
6. **Deploy** if they asked for a link, so the signup happens now

If the format is PowerPoint or Both, only offer styles whose .pptx reduction
holds up. Never show a style in HTML that the .pptx cannot honour.

---

## Checkpoint 2 — one consolidated approval

One turn, in this order:

1. **What I found** — research digest with sources, or a summary of the ingested
   document. Lead with this. It carries the premise, and a wrong premise
   invalidates everything below
2. **Assumptions I made** — anything defaulted, stated plainly
3. **The outline** — numbered slide titles, a phrase each
4. **Three style previews** — rendered title slides, opened for the user

Ask for one reply covering all four, and make rejection cheap: *"If the premise
is off, say so and ignore the rest. I will redo the outline."*

Then build.

---

## When a third turn is unavoidable

Rare. Only when proceeding under any assumption would waste the whole deck:

- **The topic is still unknown** after Checkpoint 1 and cannot be inferred from
  anything the user has written. Everything else has a defensible default. This
  one does not
- Research contradicts the premise outright
- A supplied document is unreadable, or is about something else entirely
- The request needs information only the user has, such as unshared financials

If it happens, ask everything still missing in one message, not just the one
thing that blocked you.

Everything else: assume, build, flag at delivery.
