# Data Visuals

Working code for every chart the tool can draw. Pure SVG and CSS, no libraries.

All coordinates are in 1920x1080 stage space. Charts animate when their slide
becomes visible, driven by `.slide.visible`.

**Reach for a chart before a sentence.** The reason decks turn text-heavy is that
writing about a number is easier than showing it. These exist to make showing it
the easier path.

---

## Colour

Use one accent for the value that matters and a muted tone for everything else.
Charts where every series is a different bright colour are harder to read, not
easier.

```css
:root {
    --chart-1: var(--accent);              /* the point of the chart */
    --chart-2: rgba(255,255,255,.40);
    --chart-3: rgba(255,255,255,.26);
    --chart-4: rgba(255,255,255,.16);
    --chart-grid: rgba(255,255,255,.10);
    --chart-label: var(--muted);
}
```

If a chart needs more than four colours it is probably two charts.

---

## Stat block

One to three figures carrying a slide. The most under-used layout in decks and
usually the strongest.

```html
<div class="stats">
  <div class="stat reveal" style="--d:.1">
    <div class="stat-value"><span data-count="53.6" data-dec="1">0</span></div>
    <div class="stat-label">Median age in the target city</div>
  </div>
  <div class="stat reveal" style="--d:.2">
    <div class="stat-value"><small>&euro;</small><span data-count="500" data-sep="1">0</span></div>
    <div class="stat-label">Total paid budget</div>
  </div>
</div>
```

```css
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(0,1fr)); gap: 60px; }
.stat { border-left: 3px solid var(--accent); padding-left: 34px; }
.stat-value {
    font: 600 132px/1 var(--font-display);
    color: var(--ink);
    font-variant-numeric: tabular-nums;   /* stops digits jittering while counting */
}
.stat-value small { font-size: 64px; color: var(--accent); }
.stat-label { font-size: 24px; color: var(--muted); margin-top: 12px; max-width: 22ch; }
```

`tabular-nums` matters. Without it the number visibly shivers as it counts.

---

## Bar chart

```html
<svg class="bars" viewBox="0 0 900 460">
  <line class="axis" x1="0" y1="400" x2="900" y2="400"/>
  <g class="bar" style="--d:.1">
    <rect x="40"  y="120" width="120" height="280" rx="6"/>
    <text class="bar-value" x="100" y="100">1,240</text>
    <text class="bar-label" x="100" y="432">Q1</text>
  </g>
  <g class="bar" style="--d:.2">
    <rect x="220" y="200" width="120" height="200" rx="6"/>
    <text class="bar-value" x="280" y="180">890</text>
    <text class="bar-label" x="280" y="432">Q2</text>
  </g>
</svg>
```

```css
.bars .axis { stroke: var(--chart-grid); stroke-width: 2; }
.bars rect  { fill: var(--chart-2); transform-origin: center bottom; transform: scaleY(0); }
.bars .bar:last-child rect { fill: var(--chart-1); }   /* the bar that matters */

.slide.visible .bars rect {
    transform: scaleY(1);
    transition: transform .8s var(--ease);
    transition-delay: calc(var(--d,0) * 1s);
}

.bars text        { text-anchor: middle; font-family: var(--font-body); }
.bars .bar-value  { font-size: 26px; font-weight: 700; fill: var(--ink); }
.bars .bar-label  { font-size: 22px; fill: var(--chart-label); }
```

Bars grow from the baseline, which is why `transform-origin` is `center bottom`.
Growing from the centre reads as a glitch.

**Label the bars directly and drop the y-axis.** Making someone trace a bar back
to an axis is friction with no payoff.

---

## Line chart

Draws itself using stroke dash offset. Same technique as the route motif.

```html
<svg class="line-chart" viewBox="0 0 900 440">
  <line class="grid" x1="0" y1="110" x2="900" y2="110"/>
  <line class="grid" x1="0" y1="250" x2="900" y2="250"/>
  <path class="trend" d="M 40 340 L 220 300 L 400 190 L 580 210 L 760 90" pathLength="1000"/>
  <circle class="node" cx="760" cy="90" r="9"/>
  <text class="peak" x="760" y="58">1,900</text>
</svg>
```

```css
.line-chart .grid  { stroke: var(--chart-grid); stroke-width: 1; }
.line-chart .trend {
    fill: none; stroke: var(--chart-1); stroke-width: 4;
    stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 1000; stroke-dashoffset: 1000;
}
.slide.visible .line-chart .trend { animation: draw 1.6s var(--ease) .2s forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }

.line-chart .node { fill: var(--chart-1); opacity: 0; }
.slide.visible .line-chart .node { animation: pop .4s var(--ease) 1.6s forwards; }
@keyframes pop { from { opacity:0; r:0 } to { opacity:1; r:9 } }

.line-chart .peak { text-anchor: middle; font: 700 26px var(--font-body); fill: var(--ink); }
```

`pathLength="1000"` normalises the path so the dash values work regardless of the
real geometry. Without it every new line needs its length measured by hand.

---

## Donut

Five slices maximum. Past that, use a bar chart.

```html
<div class="donut" data-chart-hover>
  <svg viewBox="0 0 200 200">
    <!-- r=80, circumference = 502.4. dasharray = slice, remainder -->
    <circle class="seg" data-value="45%" data-label="Paid social"
            cx="100" cy="100" r="80" stroke-dasharray="226 276" stroke-dashoffset="0"/>
    <circle class="seg" data-value="30%" data-label="Creative"
            cx="100" cy="100" r="80" stroke-dasharray="151 351" stroke-dashoffset="-226"/>
    <circle class="seg" data-value="25%" data-label="Contingency"
            cx="100" cy="100" r="80" stroke-dasharray="125 377" stroke-dashoffset="-377"/>
  </svg>
  <div class="donut-centre">
    <div class="big" data-readout-value>&euro;500</div>
    <div class="sub" data-readout-label>Total budget</div>
  </div>
</div>
```

```css
.donut { position: relative; width: 400px; height: 400px; }
.donut svg { transform: rotate(-90deg); overflow: visible; }  /* start at 12 o'clock */

.donut .seg {
    fill: none; stroke-width: 44; cursor: pointer;
    pointer-events: visibleStroke;
    transition: stroke-width .25s var(--ease), opacity .25s;
}
.donut .seg:nth-of-type(1) { stroke: var(--chart-1); }
.donut .seg:nth-of-type(2) { stroke: var(--chart-2); }
.donut .seg:nth-of-type(3) { stroke: var(--chart-3); }

/* Hovering one slice dims the rest, so the readout is unambiguous. */
.donut.hovering .seg        { opacity: .32; }
.donut.hovering .seg:hover  { opacity: 1; stroke-width: 58; }

.donut-centre {
    position: absolute; inset: 0; pointer-events: none;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.donut-centre .big { font: 600 62px/1 var(--font-display); color: var(--ink); }
.donut-centre .sub { font-size: 22px; color: var(--muted); margin-top: 8px; }
```

**Working out the dash arrays:** circumference is `2 * PI * r`. For r=80 that is
502.4. A slice of N percent has `stroke-dasharray: (N/100 * 502.4) (502.4 - that)`.
Each slice offsets by the negative sum of everything before it.

`pointer-events: visibleStroke` makes only the drawn ring hoverable, not the
transparent middle.

---

## Funnel

Stages with drop-off. Label the drop, not only the stage.

```html
<div class="funnel">
  <div class="stage reveal" style="--d:.1;--w:100%"><b>12,400</b><span>Reached</span></div>
  <div class="stage reveal" style="--d:.2;--w:68%"><b>8,400</b><span>Clicked</span></div>
  <div class="stage reveal" style="--d:.3;--w:31%"><b>3,900</b><span>Installed</span></div>
  <div class="stage reveal end" style="--d:.4;--w:14%"><b>1,700</b><span>Subscribed</span></div>
</div>
```

```css
.funnel { display: flex; flex-direction: column; gap: 14px; align-items: center; }
.funnel .stage {
    width: var(--w); padding: 26px 34px; border-radius: 10px;
    background: var(--chart-3); display: flex; align-items: baseline; gap: 20px;
    justify-content: center;
}
.funnel .end { background: var(--chart-1); color: var(--on-accent); }
.funnel b    { font: 600 42px var(--font-display); font-variant-numeric: tabular-nums; }
.funnel span { font-size: 22px; opacity: .8; }
```

---

## Timeline

```html
<div class="timeline">
  <div class="event reveal" style="--d:.1">
    <div class="when">Week 1</div>
    <div class="what">Creative testing</div>
    <div class="detail">12 variants across two audiences</div>
  </div>
  <div class="event reveal end" style="--d:.3">
    <div class="when">Week 4</div>
    <div class="what">Scale the winner</div>
  </div>
</div>
```

```css
.timeline { position: relative; padding-left: 44px; }
.timeline::before {
    content: ""; position: absolute; left: 11px; top: 14px; bottom: 14px;
    border-left: 4px dashed var(--chart-grid);
}
.timeline .event { position: relative; padding-bottom: 34px; }
.timeline .event::before {
    content: ""; position: absolute; left: -44px; top: 4px;
    width: 20px; height: 20px; border-radius: 50%;
    background: var(--slide-bg); border: 5px solid var(--accent);
}
.timeline .end::before { background: var(--accent); box-shadow: 0 0 18px var(--accent); }
.timeline .when   { font: 700 20px var(--font-body); color: var(--accent); letter-spacing: .06em; }
.timeline .what   { font: 600 31px var(--font-display); color: var(--ink); margin-top: 2px; }
.timeline .detail { font-size: 20px; color: var(--muted); margin-top: 6px; }
```

Set `flex-direction: row` and swap the pseudo-element geometry for a horizontal
version. The vertical form fits more events; the horizontal reads as a journey.

---

## 2x2 matrix

Consulting staple. Only honest when both axes are real and the placements are
defensible.

```html
<div class="matrix">
  <span class="axis-y">Impact</span>
  <span class="axis-x">Effort</span>
  <div class="quadrant"></div><div class="quadrant"></div>
  <div class="quadrant"></div><div class="quadrant"></div>
  <div class="plot reveal" style="--d:.2;--x:22%;--y:18%">Checkout fix</div>
  <div class="plot reveal" style="--d:.3;--x:74%;--y:66%">Rebrand</div>
</div>
```

```css
.matrix { position: relative; display: grid; grid-template: 1fr 1fr / 1fr 1fr;
          width: 760px; height: 620px; }
.matrix .quadrant { border: 1px solid var(--chart-grid); }
.matrix .plot {
    position: absolute; left: var(--x); top: var(--y); transform: translate(-50%,-50%);
    background: var(--accent); color: var(--on-accent);
    padding: 12px 22px; border-radius: 999px; font: 600 21px var(--font-body);
    white-space: nowrap;
}
.matrix .axis-y { position: absolute; left: -46px; top: 50%;
                  transform: rotate(-90deg) translateX(50%); }
.matrix .axis-x { position: absolute; bottom: -40px; left: 50%; transform: translateX(-50%); }
.matrix .axis-x, .matrix .axis-y {
    font: 700 18px var(--font-body); letter-spacing: .14em;
    text-transform: uppercase; color: var(--muted);
}
```

Never label quadrants with jargon like "Stars" or "Question marks". Say what the
quadrant means for this decision.

---

## Comparison table

When the detail genuinely matters and a chart would hide it.

```css
.cmp { width: 100%; border-collapse: collapse; font-size: 23px; }
.cmp th {
    text-align: left; padding: 18px 24px;
    font: 700 18px var(--font-body); letter-spacing: .14em;
    text-transform: uppercase; color: var(--accent);
    border-bottom: 2px solid var(--accent);
}
.cmp td { padding: 20px 24px; border-bottom: 1px solid var(--chart-grid); color: var(--ink); }
.cmp tr:last-child td { border-bottom: none; }
.cmp .highlight { background: var(--accent-soft); }   /* the recommended row */
```

No vertical rules, no zebra striping. Horizontal lines and spacing do the work.
Highlight the row you are recommending so the eye lands there first.

Eight rows and four columns is the readable ceiling at 1920x1080. Beyond that,
split the table or move it to an appendix.

---

## Source lines

Any chart carrying real data needs one.

```css
.source {
    position: absolute; left: 92px; bottom: 44px;
    font-size: 19px; color: var(--muted); opacity: .75;
}
```

> Source: internal checkout logs, Jan to Mar 2026. n = 4,812.

19px is the smallest a source line may be. The floor is 18px and
`verify_deck.py` fails anything below it. See `writing/voice.md`.

Name the origin, the period, and the sample size when there is one. Estimates say
so. Projections say so.

---

## PowerPoint

Every chart here becomes a **native PowerPoint chart** in .pptx output, not a
picture. The data stays editable inside the file, so a client can fix a number
without rebuilding the slide.

Funnels, matrices and timelines have no native chart type and become grouped
shapes. Still editable, just not data-driven.

See `references/output/pptx.md`.
