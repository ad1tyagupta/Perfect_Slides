# Consulting: Working Decks

The deliverable. Diagnostics, strategy reviews, board papers, diligence,
recommendations someone will act on. Read as much as presented, and forwarded to
people who were never in the room.

Measured from a McKinsey-style financial impact assessment: **185 words a page**
median, 507 at its densest. Roughly eight times a roadshow deck, and correctly so.

**Density: 100 to 200 words a slide, 250 absolute ceiling.** Dense is not
cramped. Structure carries the density.

---

## Answer first

The instinct is to build to the conclusion: background, method, findings,
therefore the answer. That is the order you discovered it in and the wrong order
to present it in.

Lead with the answer, then support it. Senior readers read the first page and
the last. A recommendation that only appears at the end is a recommendation most
of the room never reaches.

Structure the whole deck, and every individual page, top down:

1. The answer
2. The two to four reasons it holds
3. The evidence under each reason

Nothing appears that does not support something above it. If a page holds up no
reason, cut it or move it to the appendix.

---

## Framing: situation, complication, answer

Two or three pages at the front.

- **Situation** — what everyone already agrees is true
- **Complication** — what changed, or what is not working
- **Answer** — the recommendation, stated plainly

The complication is the page people skip and the deck then fails. Without
tension there is no reason to keep reading. If you cannot name what broke or
what changed, there may be no deck to build.

---

## Groupings must not overlap or leak

When splitting anything into parts, the parts must not overlap, and together
they must cover the whole.

> ✗ Costs: staffing, technology, overheads, unexpected expenses
> ✓ Costs: fixed, variable

The first overlaps. Staffing is an overhead, anything could be unexpected. Test
every list of parts before it goes on a page. Overlapping categories are the
most common reason a sound analysis reads as muddled.

---

## Page sequence

| Page | Carries |
|---|---|
| **Executive summary** | The whole argument on one page. Written last |
| **Situation** | Agreed context, briefly |
| **Complication** | What changed or broke |
| **Approach** | What you examined. Only if the method is contestable |
| **Findings** | One per page, each headline a conclusion |
| **Options** | Real alternatives with honest trade-offs |
| **Recommendation** | The choice, and why it wins |
| **Implementation** | Who, what, by when |
| **Risks** | What could go wrong and the response |
| **Appendix** | Backup detail, referenced but not presented |

Fifteen to twenty-five pages plus appendix.

**Options pages must contain real options.** Two straw men and the answer is
transparent, and it costs trust. If there is genuinely one viable path, say so
and explain what you ruled out.

---

## Page anatomy

The dense consulting page, as the McKinsey deck builds it:

```
┌──────────────────────────────────────────────────────────┐
│ ①  Action title: the finding, in full                    │
│    Lighter second line elaborating it                    │
│ ─────────────────────────────────────────────────────────│
│  Lead-in: the left claim   │  Lead-in: the right claim   │
│  units, small and grey     │  units, small and grey      │
│                            │                             │
│      annotated chart       │      annotated chart        │
│                            │  (tinted panel background)  │
│ ─────────────────────────────────────────────────────────│
│  Source: publisher, document, date, sample            8  │
└──────────────────────────────────────────────────────────┘
```

Six techniques worth naming, all implemented in `components/`:

**Two-level headline.** A bold action title, then a lighter line beneath
elaborating it. The title makes the claim, the second line adds the nuance that
would otherwise bloat the title past readable length.

**Chained headlines.** Consecutive pages written to continue each other. A page
titled "Ridership fell 60% in the second week of March" followed by one titled
"...and has remained low since". Reading the titles in order gives a continuous
sentence. Use it for two or three pages in a row, never a whole deck.

**Numbered page badge.** A circled number top-left marking position within a
section, so someone can reference "the second page of section three".

**Tinted split panels.** Two halves with slightly different backgrounds, one
white and one light grey, so the eye reads them as separate evidence rather than
one continuous argument. Each half gets its own bold lead-in phrase.

**Chart annotations.** A vertical rule with a label marking an event on a time
axis. "President declares national emergency". This is what turns a line chart
into an explanation.

**Full source lines.** Multi-line at the bottom, naming every publisher used,
plus the measurement caveat. Not a URL.

---

## The "so what" test

Apply to every page. State the headline, then ask "so what?"

If there is no answer, the page describes rather than argues. Find the
implication and make it the headline, or move the page to the appendix.

> Headline: "Support tickets rose 30% in Q2"
> So what? "Because the Q2 release broke checkout on Safari"
> The second sentence is the headline. The first is evidence.

---

## Sourcing

Every claim a reasonable person would question carries a source.

- Data pages carry a source line at the bottom, always
- Quotes name the speaker and date
- Estimates are labelled as estimates, with the method stated
- Anything modelled says so, assumptions in the appendix

Never present a projection as a measurement. Being caught once costs the
credibility of the whole deck.

---

## Common failures

- **Building to the conclusion.** Answer first.
- **Topic headlines.** "Market analysis" instead of the finding.
- **Overlapping categories.**
- **Fake options.** The answer plus two obviously wrong alternatives.
- **Unsourced numbers.** One challenged figure discredits the rest.
- **Appendix material in the main deck.**
- **A recommendation with no owner or date.** Then it is an opinion.
- **Cramming rather than splitting.** Past 250 words, split the page.
