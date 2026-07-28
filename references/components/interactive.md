# Interactive Components

HTML only. Behaviour is already wired in `deck.js`; this file is the markup and
styling.

Aim for **one interactive moment per deck**, placed on the slide that carries the
most weight. Interaction on every slide stops being remarkable and starts being
work. Interaction on the one slide that matters is what people remember.

When the output format is PowerPoint, do not design around these at all. Design
the flat slide from the start. See `references/output/pptx.md`.

---

## Flip card

Click to reveal the reverse. Best for pairing a claim with its evidence, a
creative with its rationale, or a question with its answer.

```html
<div class="flip">
  <div class="flip-inner">
    <div class="face front" style="background-image:url('assets/creative-01.jpg')">
      <div class="scrim"></div>
      <div class="face-title">Free first hour, every Tuesday</div>
      <div class="flag">Instagram</div>
    </div>
    <div class="face back">
      <div class="back-label">Why it worked</div>
      <div class="back-copy">Tuesday was the weakest ride day. Removing price
        on the weakest day cost the least and moved the most.</div>
    </div>
  </div>
</div>
```

```css
.flip { perspective: 1400px; cursor: pointer; }
.flip-inner {
    position: relative; width: 100%; height: 100%;
    transform-style: preserve-3d; transition: transform .7s var(--ease);
}
.flip.flipped .flip-inner { transform: rotateY(180deg); }
.flip:focus-visible { outline: 3px solid var(--accent); outline-offset: 4px; }

.face {
    position: absolute; inset: 0;
    backface-visibility: hidden; -webkit-backface-visibility: hidden;
    border-radius: 18px; overflow: hidden;
}
.face.front { background-size: cover; background-position: center 28%; }
.face.back  { background: var(--panel-strong); transform: rotateY(180deg);
              padding: 30px 32px; display: flex; flex-direction: column; justify-content: center; }

.scrim { position: absolute; inset: 0;
         background: linear-gradient(180deg, transparent 30%, rgba(0,0,0,.88) 100%); }
.face-title { position: absolute; left: 24px; right: 24px; bottom: 20px;
              font: 600 30px/1.12 var(--font-display); color: #fff; }
.flag { position: absolute; top: 16px; right: 16px;
        background: var(--accent); color: var(--on-accent);
        font: 900 18px var(--font-body); letter-spacing: .06em;
        padding: 7px 13px; border-radius: 999px; }
.back-label { font: 700 18px var(--font-body); letter-spacing: .16em;
              text-transform: uppercase; opacity: .75; margin-bottom: 14px; }
.back-copy  { font: italic 400 25px/1.4 var(--font-display); color: #fff; }
```

The `-webkit-` prefix on `backface-visibility` is still required. Without it
Safari shows both faces at once, which looks like a rendering fault.

**Signal that it flips.** A small hint, a corner fold, a cursor change. An
interaction nobody discovers is wasted work.

---

## Tab switcher

Comparing two or three profiles that share a structure. Personas, plans,
scenarios, before and after.

```html
<div class="tab-group">
  <div class="tabs">
    <button class="tab on" data-tab="a" aria-selected="true">
      Lucía<span>18-27 · Student</span>
    </button>
    <button class="tab" data-tab="b" aria-selected="false">
      Carlos<span>28-40 · Professional</span>
    </button>
  </div>

  <div class="panel on" data-panel="a">
    <div class="panel-photo" style="background-image:url('assets/lucia.jpg')"></div>
    <div class="panel-body">
      <div class="role">Weekend rider</div>
      <blockquote>The bus takes twenty minutes to go two kilometres.</blockquote>
      <ul><li>Rides socially, rarely commutes</li><li>Price sensitive</li></ul>
    </div>
  </div>

  <div class="panel" data-panel="b">…</div>
</div>
```

```css
.tabs { display: flex; gap: 16px; margin-bottom: 26px; }
.tab {
    flex: 1; text-align: left; cursor: pointer;
    padding: 18px 22px; border-radius: 14px;
    border: 2px solid var(--panel-line); background: var(--panel);
    color: var(--muted); font: 700 26px var(--font-body);
    transition: all .3s var(--ease);
}
.tab span { display: block; font: 500 19px var(--font-body); margin-top: 3px; opacity: .8; }
.tab.on {
    border-color: var(--accent); background: var(--accent-soft); color: var(--ink);
    box-shadow: 0 12px 34px var(--accent-soft);
}

/* Panels use visibility, not display, so the grid layout below survives. */
.panel { display: grid; grid-template-columns: 380px 1fr;
         height: 520px; border-radius: 20px; overflow: hidden;
         background: var(--panel); border: 1px solid var(--panel-line);
         position: absolute; visibility: hidden; opacity: 0; }
.panel.on { position: relative; visibility: visible; opacity: 1; }

.panel-photo { background-size: cover; background-position: center; }
.panel-body  { padding: 38px 44px; display: flex; flex-direction: column; }
.panel-body .role { font: 700 22px var(--font-body); letter-spacing: .12em;
                    text-transform: uppercase; color: var(--accent); }
.panel-body blockquote { font: italic 400 37px/1.25 var(--font-display);
                         color: var(--ink); margin: 20px 0 26px; }
.panel-body li { display: flex; gap: 14px; font-size: 23px; line-height: 1.35;
                 color: var(--ink); list-style: none; margin-bottom: 14px; }
.panel-body li::before { content: "—"; color: var(--accent); font-weight: 900; }
```

Two or three tabs. Four means the comparison belongs in a table.

---

## Device mockup

Content shown inside a phone. Strong for anything the audience would really see
on a phone: notifications, app screens, messages, social posts.

The version in the reference deck was one of the two things people named. It
works because it shows the real artefact rather than describing it.

```html
<div class="phone">
  <div class="notch"></div>
  <div class="screen">
    <div class="lock-time">09:00</div>
    <div class="lock-date">Tuesday, 23 June</div>

    <div class="notif" data-replay>
      <div class="notif-head">
        <span class="app-icon">n</span>
        <span class="app-name">nextbike</span>
        <span class="notif-time">now</span>
      </div>
      <div class="notif-body">¡Felices fiestas de San Juan! Deja tu bici en casa.</div>
    </div>
  </div>
</div>
```

```css
.phone {
    width: 352px; height: 664px; padding: 16px; position: relative;
    background: #040d14; border-radius: 52px;
    border: 3px solid rgba(255,255,255,.16);
    box-shadow: 0 40px 90px rgba(0,0,0,.55);
}
.notch { position: absolute; top: 16px; left: 50%; transform: translateX(-50%);
         width: 120px; height: 30px; background: #040d14;
         border-radius: 0 0 18px 18px; z-index: 3; }
.screen { width: 100%; height: 100%; border-radius: 38px; overflow: hidden;
          background: linear-gradient(165deg, #14425c, #071722); position: relative; }

.lock-time { text-align: center; margin-top: 84px;
             font: 500 76px var(--font-body); color: #fff; }
.lock-date { text-align: center; font-size: 21px; color: rgba(255,255,255,.75); }

.notif { margin: 36px 16px 0; padding: 16px 18px; border-radius: 22px;
         background: rgba(255,255,255,.14); backdrop-filter: blur(10px);
         animation: notif-in .5s var(--ease); }
@keyframes notif-in {
    from { opacity: 0; transform: translateY(-18px) scale(.96); }
    to   { opacity: 1; transform: none; }
}
.notif-head { display: flex; align-items: center; gap: 10px; }
.app-icon { width: 30px; height: 30px; border-radius: 8px;
            background: var(--accent); color: var(--on-accent);
            display: flex; align-items: center; justify-content: center;
            font: 900 15px var(--font-body); }
.app-name { font: 700 16px var(--font-body); color: #fff; flex: 1; }
.notif-time { font-size: 14px; color: rgba(255,255,255,.65); }
.notif-body { font-size: 17.5px; line-height: 1.4; color: #fff; margin-top: 9px; }
```

**Type inside a device mockup is exempt from the 18px floor.** A phone is 352px
wide on a 1920 stage, so its interface text scales like real phone text and
14 to 18px is correct there. `verify_deck.py` skips anything inside `.phone`,
`.device` or `[data-device]`. Everywhere else the floor applies.

`data-replay` makes the notification animate again each time the slide is
revisited. Without it the animation only ever plays once and the slide looks dead
on a second pass.

Combine with the carousel wiring in `deck.js` to cycle several notifications from
one phone.

---

## Path draw

A line that draws itself across a slide. Use it as a motif that recurs through
the deck, threading the story together, rather than as decoration on one slide.

```html
<svg class="path-motif" viewBox="0 0 1920 1080" preserveAspectRatio="none">
  <path d="M -40 880 C 300 780, 520 1010, 860 930 S 1500 700, 1980 820" pathLength="900"/>
  <circle cx="300" cy="843" r="9"/>
  <circle cx="860" cy="930" r="9"/>
</svg>
```

```css
.path-motif { position: absolute; inset: 0; pointer-events: none; opacity: .35; }
.path-motif path { fill: none; stroke: var(--accent); stroke-width: 3;
                   stroke-dasharray: 14 16; stroke-dashoffset: 900; }
.path-motif circle { fill: var(--accent); }
.slide.visible .path-motif path { animation: draw-path 2.4s var(--ease) forwards; }
@keyframes draw-path { to { stroke-dashoffset: 0; } }
```

Behind content, low opacity, always. A motif that competes with the words is
a mistake.

---

## Hover-lift cards

The cheapest interaction that still adds life. Good for a grid of parallel items.

```css
.lift {
    background: var(--panel); border: 1px solid var(--panel-line);
    border-radius: 20px; padding: 36px 38px; position: relative; overflow: hidden;
    transition: transform .35s var(--ease), border-color .35s, box-shadow .35s;
}
.lift:hover {
    transform: translateY(-10px);
    border-color: var(--accent);
    box-shadow: 0 26px 60px var(--accent-soft);
}
.lift .index {
    position: absolute; top: 18px; right: 28px;
    font: italic 400 88px/1 var(--font-display);
    color: var(--accent-soft); transition: color .35s;
}
.lift:hover .index { color: var(--accent); }
```

---

## Accessibility

`deck.js` gives flip cards a tab index and keyboard activation, and keeps
`aria-selected` current on tabs. Two rules to hold when authoring:

- Never put information **only** behind an interaction. Anyone reading the PDF or
  the PowerPoint version has to get the same content.
- Any colour used to carry meaning needs a second signal: a label, an icon, or
  a position.
