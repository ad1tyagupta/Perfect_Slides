# Research

When the user does not have the content. Use your agent's own web search.

The output of research is not slides. It is a digest the user approves before
anything gets built.

---

## Scope first

Research that goes wide and returns forty facts for a ten-slide deck wastes
everyone's time and buries the argument.

The scope was asked at intake. If the user left it blank, set it yourself from
the topic and deck type, and state what you scoped at the review.

Work out what the deck actually needs before searching:

| Deck type | Needs |
|---|---|
| Pitch | Market size bottom up, competitors, comparable funding, the timing argument |
| Consulting | Base rates, benchmarks, precedents, primary sources for every claim |
| Marketing | Audience behaviour, channel costs, competitor campaigns, seasonality |
| Conference | One or two surprising facts, a memorable example, current context |
| Internal | Usually little. Do not research what the team already knows |
| Teaching | Authoritative definitions, worked examples, common misconceptions |

Ten to fifteen solid facts is enough for most decks. Depth on the load-bearing
claims beats breadth.

---

## Track every source

Maintain `sources.json` from the first search:

```json
{
  "sources": [
    {
      "id": "s1",
      "claim": "Bike share trips in Spanish cities grew 34% in 2025",
      "value": "34%",
      "publisher": "Spanish Ministry of Transport",
      "title": "Urban Mobility Annual Report 2025",
      "url": "https://…",
      "date": "2026-02",
      "accessed": "2026-07-25",
      "type": "primary",
      "confidence": "high"
    }
  ]
}
```

`type` is `primary` for original data, `secondary` for reporting on it, and
`estimate` for anything modelled. `confidence` is your own honest read.

**Never put a number on a slide that is not in this file.** If it cannot be
traced, it cannot be presented.

---

## What counts as a good source

Ranked:

1. The original data. Statistical offices, regulators, company filings, published research.
2. The organisation being discussed. Their own reports and releases.
3. Established outlets reporting on the above, when the original is paywalled.
4. Industry analysts, noting they usually sell something related.

Avoid: content marketing dressed as research, statistics with no named origin,
numbers that circulate widely with no traceable source, and anything you cannot
date.

**Chase numbers to their origin.** A figure quoted in three articles usually
traces back to one report, and often to a different number than the one being
quoted. Cite the report.

**Check the date.** Market data older than two years is usually wrong now. Say
the date on the slide when it matters.

---

## Conflicts

Two credible sources disagreeing is information, not a problem.

Do not average them and do not quietly pick the convenient one. Present the range
and say who says what. "Estimates run from 12% to 19%, depending on whether
in-app purchases are counted" is a stronger slide than either figure alone.

---

## Citation on the slide

Where it goes depends on the deck type:

| Deck type | Convention |
|---|---|
| Consulting | Source line at the bottom of every data slide. Non-negotiable |
| Pitch | Market size and competitive claims cited. Product claims need none |
| Marketing | Cite benchmarks and audience data. Creative needs no citation |
| Conference | Cite surprising facts on the slide. The audience will ask |
| Internal | Link to the dashboard or the query. No formal citation |
| Teaching | Cite, and add a further reading slide |

Format:

> Source: Spanish Ministry of Transport, Urban Mobility Annual Report 2025, Feb 2026.

Name the publisher, the document, and the date. A bare URL is not a citation.

---

## Labelling honestly

- **Estimates** say so, with the method in a note or the appendix
- **Projections** say so, with the assumption stated
- **Your own analysis** says so
- **A single case** is never presented as a pattern

Never present a projection as a measurement. Being caught once costs the
credibility of the whole deck.

---

## The digest

Present findings before outlining. Never go from research straight to slides.

Keep it short:

1. **What I found** — the load-bearing facts, each with its source
2. **What surprised me** — anything that changes the likely argument
3. **What I could not confirm** — gaps, and what you would need to close them
4. **Where sources disagree** — the ranges

Then the outline, the assumptions and the style previews, all in the same turn.
See `references/workflow/intake.md`.

Make rejection cheap. If the premise is wrong, the user should be able to say so
in one line without reading the rest.
