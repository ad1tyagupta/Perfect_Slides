# Consulting Page Techniques

Working code for the moves that make a dense consulting page readable. Taken
from real McKinsey-style and Bain decks.

Read this with `narrative/consulting-working.md` or `consulting-roadshow.md`.

These are what let a page carry 200 words without feeling crammed. Density is
survivable when structure is obvious, and unbearable when it is not.

---

## Two-level headline

A bold action title stating the finding, then a lighter line beneath adding the
nuance that would otherwise push the title past readable length.

```html
<header class="page-head">
  <span class="page-badge">1</span>
  <div>
    <h2 class="action-title">Ridership has remained low since the March drop</h2>
    <p class="title-sub">Initial declines led to persistently reduced demand</p>
  </div>
</header>
```

```css
.page-head { display: flex; gap: 26px; align-items: flex-start;
             border-bottom: 2px solid var(--ink); padding-bottom: 20px; }
.page-badge {
    flex: none; width: 52px; height: 52px; border-radius: 50%;
    background: var(--ink); color: var(--slide-bg);
    display: flex; align-items: center; justify-content: center;
    font: 700 26px var(--font-body);
}
.action-title { font: 700 52px/1.1 var(--font-display); color: var(--ink); }
.title-sub    { font: 400 30px/1.25 var(--font-body); color: var(--muted);
                margin-top: 10px; }
```

The badge marks position within a section, so someone can say "the second page
of section three". Drop it on decks under twelve pages.

---

## Chained headlines

Consecutive pages written to continue one sentence.

> Page 4: **Ridership fell 60% in the second week of March**
> Page 5: **...and has remained low since**

Reading the titles in order gives continuous prose. It signals that the pages
belong together and stops each one being read as a separate claim.

Two or three pages in a row, never a whole deck. Start the continuation with an
ellipsis so it is unmistakable. Every page must still work alone, because these
decks get screenshotted a page at a time.

---

## Tinted split panels

Two halves with slightly different grounds, so the eye reads them as separate
evidence rather than one argument running across.

```html
<div class="split-panels">
  <section class="panel-l">
    <p class="lead-in"><b>Initial decline:</b> ridership fell sharply from the
       week of 9 March</p>
    <p class="units">% decline in ridership, public reports</p>
    <!-- chart -->
  </section>
  <section class="panel-r">
    <p class="lead-in"><b>Sustained decline:</b> app data shows use flat
       through April</p>
    <p class="units">% change in transit demand, app measurement</p>
    <!-- chart -->
  </section>
</div>
```

```css
.split-panels { display: grid; grid-template-columns: 1fr 1fr; gap: 0;
                flex: 1; min-height: 0; }
.panel-l { background: var(--slide-bg); padding: 34px 44px 34px 0; }
.panel-r { background: var(--panel); padding: 34px 44px; }

.lead-in { font: 400 30px/1.3 var(--font-body); color: var(--ink); }
.lead-in b { font-weight: 700; }
.units   { font: 400 21px var(--font-body); color: var(--muted); margin-top: 14px; }
```

The **bolded lead-in** is the workhorse. Bold the two or three words that name
what the panel shows, then continue in regular weight. The reader can scan the
bold fragments alone and still get the argument.

The **units line** goes under the lead-in and above the chart. The title makes
the claim, this says what is being counted. Never skip it on a data page.

---

## Chart annotations

What turns a line chart into an explanation.

```html
<svg class="annotated" viewBox="0 0 900 460">
  <line class="event-rule" x1="360" y1="30" x2="360" y2="400"/>
  <text class="event-label" x="372" y="52">National emergency declared</text>

  <path class="series" d="M 40 90 L 200 105 L 360 140 L 540 330 L 720 356 L 860 362"/>
  <text class="series-end" x="868" y="366">-88</text>
</svg>
```

```css
.annotated .event-rule  { stroke: var(--muted); stroke-width: 2; }
.annotated .event-label { font: italic 400 20px var(--font-body); fill: var(--muted); }
.annotated .series      { fill: none; stroke: var(--chart-1); stroke-width: 4;
                          stroke-linecap: round; }
.annotated .series-end  { font: 700 22px var(--font-body); fill: var(--chart-1); }
```

Mark the event, not just the data. A vertical rule at the date something
happened, with a short label, does more explaining than a paragraph beside the
chart.

---

## Direct series labels

Never a legend box. Put the series name at the end of its line, in the line's
colour.

```css
.series-label { font: 700 22px var(--font-body); dominant-baseline: middle; }
```

```html
<text class="series-label" x="870" y="120" fill="var(--chart-1)">NJ Transit</text>
<text class="series-label" x="870" y="188" fill="var(--chart-2)">MBTA Boston</text>
```

Where lines end close together, stagger the labels vertically and add a short
leader line. Still better than a legend, which makes the reader hold a
colour in memory while looking somewhere else.

---

## Axis ceiling and secondary data row

Two Bain conventions that add information without adding a chart.

**Axis ceiling.** The top value printed at the top left of the plot, so the
scale reads at a glance.

```html
<text class="axis-ceiling" x="40" y="46">$1,200B</text>
```
```css
.axis-ceiling { font: 400 22px var(--font-body); fill: var(--ink); }
```

**Secondary data row.** A labelled row of figures beneath the category axis,
carrying a related series. Average deal size under total deal value, headcount
under revenue, sample size under percentages.

```html
<div class="data-row">
  <span class="data-row-label">Avg. deal size<br>$M</span>
  <span>256</span><span>494</span><span>476</span><span>165</span>
</div>
```
```css
.data-row { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr;
            align-items: start; margin-top: 18px; padding-left: 190px; }
.data-row span { text-align: center; font: 400 22px var(--font-body); color: var(--ink);
                 font-variant-numeric: tabular-nums; }
.data-row-label { position: absolute; left: 0; width: 180px; text-align: left;
                  font: 400 20px/1.25 var(--font-body); color: var(--muted); }
```

Align the columns to the chart's categories exactly. Misaligned by a few pixels
and it reads as a mistake.

---

## Source lines

Multi-line, at the bottom, naming every publisher plus the measurement caveat.

```html
<footer class="page-foot">
  <p class="sources">Source: The New York Times, Bloomberg, The Boston Herald,
     TransitApp data measuring frequency of app opens against projected use,
     adjusted for annual growth</p>
  <span class="page-no">8</span>
</footer>
```

```css
.page-foot { display: flex; justify-content: space-between; align-items: flex-end;
             gap: 40px; border-top: 1px solid var(--panel-line); padding-top: 16px; }
.sources   { font: 400 19px/1.35 var(--font-body); color: var(--muted); max-width: 1400px; }
.page-no   { font: 400 20px var(--font-body); color: var(--muted); flex: none; }
```

Name the publisher, the document and the date. A bare URL is not a citation.
Where the measurement needs explaining, explain it here rather than on the chart.

---

## Disclaimer box

For scenario work, projections, or anything a lawyer would want marked.

```css
.disclaimer { border: 1px solid var(--ink); padding: 18px 22px;
              font: 400 19px/1.35 var(--font-body); color: var(--ink);
              max-width: 620px; }
```

Boxed, top right, small. Being explicit that these are scenarios rather than
forecasts protects the credibility of everything else on the page.

---

## PowerPoint

| Technique | Fallback |
|---|---|
| Two-level headline | Two text boxes, same sizes |
| Page badge | Oval with centred text |
| Chained headlines | Identical, it is only copy |
| Tinted split panels | Two rectangles with different fills |
| Bolded lead-in | Rich text run with bold, identical |
| Units line | Text box |
| Event annotation | Line shape plus text box |
| Direct series labels | Chart data labels, or text boxes |
| Axis ceiling | Text box |
| Secondary data row | Text boxes on a grid, or a borderless table |
| Source line, page number | Text boxes |

All of it survives, because none of it depends on motion or interaction. Dense
consulting pages are the deck type PowerPoint handles best.
