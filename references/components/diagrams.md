# Diagrams

Structure made visible. Process, hierarchy, cycle, comparison.

The vocabulary here is the one professional decks actually use, measured by
frequency across a 247-slide diagram library: chevrons and pentagons for
process, trapezoids for funnels, triangles for hierarchy, arcs for cycles,
braces for grouping, diamonds for decisions.

**Use a diagram when the relationship is the point.** If the content is a list
that happens to have five items, a list is better. A diagram that adds shapes
without adding meaning is decoration, and it reads as filler.

---

## Chevron process

Sequential stages where each feeds the next. The most-used consulting diagram
there is.

```html
<div class="chevrons">
  <div class="chev reveal" style="--d:.1"><b>Discover</b><span>2 weeks</span></div>
  <div class="chev reveal" style="--d:.2"><b>Design</b><span>3 weeks</span></div>
  <div class="chev reveal" style="--d:.3"><b>Build</b><span>6 weeks</span></div>
  <div class="chev now reveal" style="--d:.4"><b>Launch</b><span>1 week</span></div>
</div>
```

```css
.chevrons { display: flex; gap: 6px; }
.chev {
    flex: 1; padding: 30px 34px 30px 54px; position: relative;
    background: var(--panel); color: var(--ink);
    clip-path: polygon(0 0, calc(100% - 34px) 0, 100% 50%, calc(100% - 34px) 100%, 0 100%, 34px 50%);
}
.chev:first-child { clip-path: polygon(0 0, calc(100% - 34px) 0, 100% 50%, calc(100% - 34px) 100%, 0 100%); }
.chev:last-child  { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 34px 50%); }
.chev.now { background: var(--accent); color: var(--on-accent); }
.chev b    { display: block; font: 600 30px var(--font-display); }
.chev span { display: block; font-size: 21px; opacity: .75; margin-top: 6px; }
```

Three to six stages. Mark the current one with the accent so the audience knows
where they are. Beyond six, the chevrons get too narrow to read and it becomes a
timeline instead.

---

## Cycle

A process with no end. Feedback loops, iteration, recurring reviews.

```html
<svg class="cycle" viewBox="0 0 520 520">
  <circle class="ring" cx="260" cy="260" r="180"/>
  <g class="arrow-head" transform="rotate(0 260 260)">
    <polygon points="260,68 274,96 246,96"/>
  </g>
  <g class="node" style="--d:.1"><circle cx="260" cy="80"  r="56"/><text x="260" y="88">Plan</text></g>
  <g class="node" style="--d:.2"><circle cx="440" cy="260" r="56"/><text x="440" y="268">Do</text></g>
  <g class="node" style="--d:.3"><circle cx="260" cy="440" r="56"/><text x="260" y="448">Check</text></g>
  <g class="node" style="--d:.4"><circle cx="80"  cy="260" r="56"/><text x="80"  y="268">Act</text></g>
</svg>
```

```css
.cycle .ring { fill: none; stroke: var(--panel-line); stroke-width: 3;
               stroke-dasharray: 10 12; }
.cycle .arrow-head polygon { fill: var(--accent); }
.cycle .node circle { fill: var(--panel); stroke: var(--accent); stroke-width: 3; }
.cycle .node text   { text-anchor: middle; font: 600 24px var(--font-body); fill: var(--ink); }
.cycle .node { opacity: 0; transform: scale(.85); transform-origin: center;
               transition: opacity .5s var(--ease), transform .5s var(--ease);
               transition-delay: calc(var(--d,0) * 1s); }
.slide.visible .cycle .node { opacity: 1; transform: scale(1); }
```

Four stages is the readable maximum. Three feels sparse, five crowds the ring.

---

## Pyramid

Hierarchy where each layer rests on the one below. Strategy stacks, needs
hierarchies, maturity models.

```html
<div class="pyramid">
  <div class="tier reveal" style="--d:.3;--w:34%">Vision</div>
  <div class="tier reveal" style="--d:.2;--w:62%">Strategy</div>
  <div class="tier reveal" style="--d:.1;--w:90%">Execution</div>
</div>
```

```css
.pyramid { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.pyramid .tier {
    width: var(--w); padding: 28px; text-align: center;
    background: var(--panel); color: var(--ink);
    font: 600 30px var(--font-display);
    clip-path: polygon(6% 0, 94% 0, 100% 100%, 0 100%);
}
.pyramid .tier:first-child { background: var(--accent); color: var(--on-accent);
    clip-path: polygon(50% 0, 100% 100%, 0 100%); }
```

**Reveal bottom to top**, which is why the delays run backwards. The foundation
appears first because that is the argument: this rests on that.

Three or four tiers. Accent the tier the slide is about, which is usually the top.

---

## Funnel

Sequential drop-off. Label the loss between stages, not only the stages, because
the loss is the finding.

```html
<div class="funnel">
  <div class="stage reveal" style="--d:.1;--w:100%"><b>12,400</b><span>Reached</span></div>
  <div class="drop">-32%</div>
  <div class="stage reveal" style="--d:.2;--w:68%"><b>8,400</b><span>Clicked</span></div>
  <div class="drop">-54%</div>
  <div class="stage end reveal" style="--d:.3;--w:31%"><b>3,900</b><span>Installed</span></div>
</div>
```

```css
.funnel { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.funnel .stage {
    width: var(--w); padding: 26px 34px; text-align: center;
    background: var(--panel); display: flex; gap: 20px;
    align-items: baseline; justify-content: center;
    clip-path: polygon(0 0, 100% 0, 94% 100%, 6% 100%);
}
.funnel .end  { background: var(--accent); color: var(--on-accent); }
.funnel b     { font: 600 42px var(--font-display); font-variant-numeric: tabular-nums; }
.funnel span  { font-size: 22px; opacity: .8; }
.funnel .drop { font: 700 20px var(--font-body); color: var(--accent);
                letter-spacing: .06em; }
```

---

## Brace grouping

A curly brace gathering several items into one conclusion. The cheapest way to
show "all of these lead to that", and badly underused.

```html
<div class="braced">
  <ul class="brace-items">
    <li>Payment handler deprecated</li>
    <li>Session token expires early</li>
    <li>No error shown on failure</li>
  </ul>
  <svg class="brace" viewBox="0 0 40 300" preserveAspectRatio="none">
    <path d="M 4 0 Q 30 0 30 40 L 30 130 Q 30 150 38 150 Q 30 150 30 170 L 30 260 Q 30 300 4 300"/>
  </svg>
  <div class="brace-result">8% of carts lost</div>
</div>
```

```css
.braced { display: grid; grid-template-columns: 1fr 40px auto;
          gap: 30px; align-items: center; }
.brace path { fill: none; stroke: var(--accent); stroke-width: 3;
              vector-effect: non-scaling-stroke; }
.brace-items li { list-style: none; font-size: 27px; color: var(--ink);
                  padding: 14px 0; border-bottom: 1px solid var(--panel-line); }
.brace-result { font: 600 44px var(--font-display); color: var(--accent); max-width: 12ch; }
```

`vector-effect: non-scaling-stroke` keeps the brace stroke even after the
non-uniform scaling. Without it the curve thickens on one axis.

---

## Decision tree

Branching choices. Diamonds for decisions, rectangles for outcomes.

```html
<div class="tree">
  <div class="q">Is the cart recoverable?</div>
  <div class="branches">
    <div class="branch"><span class="edge">Yes</span>
      <div class="outcome ok">Restore and retry</div></div>
    <div class="branch"><span class="edge">No</span>
      <div class="outcome">Show the error, offer to rebuild</div></div>
  </div>
</div>
```

```css
.tree .q {
    margin: 0 auto; width: 380px; aspect-ratio: 1.6; display: grid;
    place-content: center; text-align: center; padding: 0 40px;
    background: var(--accent); color: var(--on-accent);
    font: 600 26px var(--font-body);
    clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%);
}
.tree .branches { display: flex; gap: 80px; justify-content: center; margin-top: 30px; }
.tree .edge { display: block; text-align: center; font: 700 20px var(--font-body);
              color: var(--accent); margin-bottom: 12px; }
.tree .outcome { padding: 26px 32px; border-radius: 10px;
                 background: var(--panel); border: 1px solid var(--panel-line);
                 font-size: 25px; color: var(--ink); max-width: 340px; }
.tree .outcome.ok { border-color: var(--accent); }
```

Two levels maximum on a slide. Three levels is a document, not a diagram.

---

## Arrow flow

When the relationship is directional but not a fixed sequence. Inputs feeding an
output, causes producing an effect.

```css
.flow { display: flex; align-items: center; gap: 24px; }
.flow .box { flex: 1; padding: 30px; border-radius: 12px;
             background: var(--panel); border: 1px solid var(--panel-line);
             font-size: 26px; color: var(--ink); }
.flow .arrow { flex: none; width: 46px; height: 46px; }
.flow .arrow svg { fill: var(--accent); }
```

```html
<div class="arrow"><svg viewBox="0 0 24 24"><path d="M2 11h14l-5-5 1.5-1.5L21 12l-8.5 7.5L11 18l5-5H2z"/></svg></div>
```

Use one arrow style throughout a deck. Mixing arrow shapes reads as clip art.

---

## Choosing

| The relationship is | Use |
|---|---|
| Ordered stages, each feeding the next | Chevron process |
| A loop with no end | Cycle |
| Layers resting on each other | Pyramid |
| Sequential loss | Funnel |
| Many things producing one thing | Brace |
| A branching choice | Decision tree |
| Directional but unordered | Arrow flow |
| Two independent axes | 2x2 matrix, in `data-viz.md` |
| Events over time | Timeline, in `data-viz.md` |
| None of these | It is a list. Use a list. |

---

## PowerPoint

All of these translate, because they are flat vector shapes and PowerPoint has
native geometry for every one.

| Diagram | Built from |
|---|---|
| Chevron process | `MSO_SHAPE.CHEVRON` in a row |
| Cycle | Ovals on a circle, plus `BLOCK_ARC` and a triangle head |
| Pyramid | Stacked `TRAPEZOID`, with `ISOSCELES_TRIANGLE` on top |
| Funnel | Stacked `TRAPEZOID`, narrowing |
| Brace | `LEFT_BRACE` |
| Decision tree | `DIAMOND` plus `ROUNDED_RECTANGLE` |
| Arrow flow | `RIGHT_ARROW` between rectangles |

Entrance animations survive. Nothing here needs hover or click, which makes
diagrams the safest content in a PowerPoint deck.
