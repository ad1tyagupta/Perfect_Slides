# Building HTML

One self-contained file. All CSS and JavaScript inline, no build step, no
dependencies. Opens by double-clicking it.

---

## Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deck title</title>

<!-- Real fonts, never system fonts. Google Fonts or Fontshare. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..700&display=swap" rel="stylesheet">

<style>
/* === THEME ===============================================================
   Every colour and font in one place. Changing the deck means changing here.
   ========================================================================= */
:root {
    --bg: #0E2635;
    --bg2: #123448;
    --stage-bg: #081B26;        /* the letterbox around the stage */
    --slide-bg: #0E2635;
    --ink: #EAF4F8;
    --muted: #8FB2C0;
    --accent: #00A8D8;
    --accent-soft: rgba(0,168,216,.16);
    --on-accent: #062130;
    --panel: rgba(255,255,255,.05);
    --panel-line: rgba(255,255,255,.12);

    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'Satoshi', system-ui, sans-serif;

    --ease: cubic-bezier(.16, 1, .3, 1);
    --dur: .7s;
}

/* === STAGE ===============================================================
   Paste references/components/stage.css here, complete and unedited.
   ========================================================================= */

/* === SLIDES ==============================================================
   One clearly commented block per slide. Someone editing this later needs
   to find slide 6 without reading the whole file.
   ========================================================================= */
</style>
</head>
<body>

<div class="deck-progress"></div>

<div class="deck-viewport">
  <main class="deck-stage" id="deckStage">

    <!-- ===== 1 · TITLE ===== -->
    <section class="slide active">
      <div class="slide-inner">
        <div class="kicker reveal" style="--d:.05">Quarterly review</div>
        <h1 class="reveal" style="--d:.15">Checkout is where the revenue leaks</h1>
        <p class="reveal" style="--d:.3">Three fixes recover more than a quarter
           of acquisition spend.</p>
      </div>
      <div class="speaker-notes">Open with the number, not the background.</div>
    </section>

    <!-- ===== 2 · THE PROBLEM ===== -->
    <section class="slide">…</section>

  </main>
</div>

<div class="edit-hotzone"></div>
<button class="edit-toggle" id="editToggle" title="Edit text (E)">&#9998;</button>

<nav class="deck-controls" aria-label="Slide navigation">
  <button data-nav="prev" aria-label="Previous slide">‹</button>
  <span class="count">1 / 12</span>
  <button data-nav="next" aria-label="Next slide">›</button>
  <button data-nav="fullscreen" aria-label="Fullscreen">⛶</button>
</nav>

<script>
/* Paste references/components/deck.js here, complete and unedited. */
</script>
</body>
</html>
```

---

## Rules

**Include `stage.css` and `deck.js` in full.** Not summarised, not trimmed. They
carry fixes for problems that are painful to rediscover, including the
`display: none` trap that shows every slide at once and the print rules that stop
PDF export producing blank pages.

**Author at 1920x1080 in real pixels.** No `vw`, no `vh`, no `clamp()` inside a
slide. The stage handles every screen by scaling as one unit. Responsive units
inside a slide fight the scaling and produce layouts that drift between machines.

**Never switch slides with `display`.** Use the `.active` and `.visible` classes.
A later rule like `.slide-content { display: flex }` overrides `display: none`
and reveals every slide at once. This is the single most common way a deck breaks.

**Always write slide variants as `.slide.divider`, never `.divider`.**

```css
.slide.divider { background: var(--ink); }     /* correct */
.divider       { background: var(--ink); }     /* silently fails */
```

`stage.css` sets `.slide { background: var(--slide-bg) }` at specificity (0,1,0).
A bare `.divider` has the same specificity, so it only wins if it appears later
in the stylesheet. Group your variants with the theme, as most people naturally
do, and `.slide` wins instead: the background snaps back to the theme colour
while your dark-slide text colour stays.

The result is a section divider with white text on a white background. It looks
completely blank and nothing in the markup is wrong. `.slide.divider` is (0,2,0)
and wins regardless of order, so use it every time.

`verify_deck.py` now catches this and reports it as invisible text.

**Never negate a CSS function.** `-clamp(...)` and `-min(...)` are silently
ignored. Write `calc(-1 * clamp(...))`.

**Comment every slide.** `<!-- ===== 4 · BUDGET ===== -->`. Someone editing this
in six months needs to find things.

---

## Three layout traps

All three were hit building the example deck. They share a habit of failing
silently, so the deck looks finished and is not.

**Set the font on `.slide`, not only on `.slide-inner`.**

```css
.slide { font-family: var(--font-body); color: var(--ink); }
```

Anything placed directly on the slide, such as a source line, a footer or a
full-bleed layout, sits outside `.slide-inner`. Without this it inherits the
browser default and quietly renders in Times. It is easy to miss because the
main content looks right.

**Make the content region fill the slide.**

```css
.slide-inner { display: flex; flex-direction: column; }
.slide-inner > .s-head { flex: none; }
.slide-inner > *:not(.s-head) { flex: 1; min-height: 0; align-content: center; }
```

Without this, content stacks from the top and leaves a dead band across the
bottom half. The slide is not broken, it just looks unfinished, which is harder
to notice and just as bad.

**Anything with absolutely positioned children needs its row stretched.**

Flip cards, device mockups and layered panels put their content in
`position: absolute` layers, which contribute no height. Inside a grid whose rows
size to content, the card collapses to nothing.

```css
.flip-grid {
    display: grid;
    align-content: stretch;          /* not center */
    grid-auto-rows: minmax(0, 1fr);
}
```

---

## Reveals

Stagger with the `--d` custom property, in seconds:

```html
<h2 class="reveal" style="--d:.1">The finding</h2>
<p  class="reveal" style="--d:.25">The evidence</p>
<div class="reveal" style="--d:.4">The chart</div>
```

Delays land between `.05` and `.6`. Past that the audience is waiting for the
slide instead of listening to you.

Variants: `.reveal-scale`, `.reveal-left`, `.reveal-blur`. Pick one per deck and
hold it. Mixing entrance directions looks unplanned.

**One well-paced entrance beats five scattered micro-animations.** Motion carries
meaning or it goes. A number counting up earns it because the count is the point.
A subtitle sliding in does not.

---

## Inline editing

Included by default. The user presses `E`, or hovers the top-left corner, and
can then click any text in the deck to change it. Edits save to their browser
automatically, and "Save a copy" downloads an HTML file with the changes baked in.

Two lines of markup, already in the skeleton above:

```html
<div class="edit-hotzone"></div>
<button class="edit-toggle" id="editToggle" title="Edit text (E)">&#9998;</button>
```

Everything else is in `deck.js`. Counters, speaker notes and the nav are
excluded from editing on purpose.

Leave it in unless the user asks for a locked or export-only file. Fixing a typo
should not cost them a message.

---

## Speaker notes

```html
<div class="speaker-notes">Point at March. That is the release date.</div>
```

Hidden in the deck. Shown in presenter view, which opens with `P` and gives the
notes, the next slide and a running timer in a second window. Put that window on
the laptop and the deck on the projector.

---

## Images

Relative paths, kept in `assets/` beside the HTML.

```html
<img src="assets/error-state.png" alt="Checkout error with no message">
```

Never absolute filesystem paths. They break the moment the file moves, and they
break PDF export.

Real `alt` text. "Checkout error with no message" tells someone something.
"Image" does not.

---

## Fonts and the network

Decks load fonts from a CDN, so a deck opened offline or behind a firewall that
blocks Google Fonts renders in a fallback and does not look the way it was
designed.

For anything you will present, bake the fonts in:

```bash
python scripts/embed_fonts.py deck.html
```

That writes `deck.offline.html` with every font inlined. It adds a few hundred
KB and needs no network at all. Do this before any talk where you cannot count
on wifi, which is most of them.

`verify_deck.py` reports any font that is declared but not actually rendering.

---

## Type sizes

**Nothing below 18px at stage scale.** `verify_deck.py` fails the deck otherwise.
That is roughly 9pt on a real slide, which is unreadable past the third row.

Source lines and captions belong at 19-20px. Body text 22-30px. Headlines 48-64px.
Full table in `references/writing/voice.md`.

---

## Before delivering

```bash
python scripts/verify_deck.py deck.html --shots ./shots
```

Then look at the screenshots. The checker catches overflow, overlap, unreadable
type and fonts that are not really loading. It cannot tell you whether the slide
is any good.

---

## PDF

Print to PDF from the browser at 1920x1080 landscape, background graphics on.
The print rules in `stage.css` put one slide per page and resolve every reveal,
so nothing prints blank.

Animation and interactivity do not survive. Say so when handing it over.
