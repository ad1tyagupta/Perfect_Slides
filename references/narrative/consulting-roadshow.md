# Consulting: Roadshow Decks

Presented live to a room. Published research, market updates, conference
keynotes, partner briefings. The kind of deck a firm puts its name on and takes
on tour.

Measured from a Bain global private equity roadshow deck: **24 words a page**,
median. Chart-led, one finding per page, enormous white space.

**Density: 20 to 40 words a slide.** If a page needs a paragraph, it belongs in
the working deck instead.

---

## The shape

Not an argument with a recommendation at the end. A sequence of findings, each
standing alone, building a picture.

| Beat | Carries |
|---|---|
| **Title** | Report name, firm, year |
| **The headline finding** | The one thing people will quote |
| **Context** | Where the market was |
| **Findings** | One per page, six to twelve of them |
| **What it means** | Interpretation, briefly |
| **Outlook** | What happens next |
| **Method and sources** | At the back, thorough |

Twelve to twenty pages. Every page survives being screenshotted alone, because
that is what happens to these decks.

---

## One chart, one finding, one page

The discipline that makes these work.

The page holds an action title, one chart, and almost nothing else. No sidebar
of interpretation, no supporting bullets, no takeaway box. The title says what
the chart shows, and the chart proves it.

If a page needs two charts to make its point, it is two pages.

---

## The chart carries everything

Since there is no supporting text, the chart has to be self-sufficient.

**Grey everything, colour the point.** Every bar grey except the one the title
is about, which is the accent colour. This is the single most recognisable
consulting chart convention and it works because the eye lands on the finding
before the audience has read anything.

**Label directly, never with a legend.** Values sit on or beside their bars.
Series names sit at the end of their lines, in the series colour. Making someone
trace back to a legend is friction with no payoff.

**Say the units above the chart.** A small grey line under the title:
"Global buyout deal value, excluding add-ons". The title makes the claim, this
says what is being counted.

**Print the axis ceiling.** The top value stated top-left, so the scale is
readable at a glance without counting gridlines.

**Add a second data row when it helps.** A row of numbers beneath the axis,
labelled at the left, carrying a related series. Average deal size under a chart
of total value, for example. It doubles the information without adding a chart.

All of these are implemented in `components/data-viz.md`.

---

## The action title is the whole slide

> Global buyout value dropped by more than a third in 2022 to $654B

That title contains the direction, the magnitude, the period and the absolute
figure. Someone who reads only the titles has read the report.

Write every title so it works alone, out of order, with no chart beneath it.
Then check the titles in sequence tell the story.

---

## Design

Light background, near-black text, one accent. Serious, unfussy, and it survives
a bad projector, which matters because these get presented in rented rooms.

Generous margins. The Bain pages leave roughly a fifth of the width empty on
each side. That space is what makes a single chart look authoritative rather
than lonely.

`Signal Brief` or `Broadsheet` from the presets. Never a dark deck, because
these get printed and forwarded.

---

## Sources

One source line per page, small, at the bottom. Full methodology at the back,
not inline, because inline caveats break the rhythm of a roadshow.

If a figure is modelled or estimated, that word appears in the source line.

---

## Common failures

- **Adding an interpretation sidebar.** That is the working deck. Here it clutters.
- **Two charts on one page.**
- **A legend instead of direct labels.**
- **Colouring every series.** Then nothing is emphasised.
- **A topic title.** "Buyout market overview" wastes the most valuable line.
- **Dark backgrounds.** These decks get printed.
