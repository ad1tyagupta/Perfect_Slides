# Style Presets

Read only the two or three entries shortlisted from `style-index.json`.

Each preset gives the palette, the fonts, one signature move, and what the
PowerPoint version becomes. A preset is a starting point, not a cage. Adapt the
palette when the user has a brand.

`safe` fonts are what the .pptx uses. They must be widely installed.

---

## Night Ride

Deep navy under an electric accent. Editorial serif carries the voice, geometric
sans carries the substance.

```css
--bg: #0E2635;  --bg2: #123448;  --stage-bg: #081B26;
--ink: #EAF4F8; --muted: #8FB2C0; --accent: #00A8D8;
--accent-soft: rgba(0,168,216,.16); --on-accent: #062130;
--panel: rgba(255,255,255,.05); --panel-line: rgba(255,255,255,.12);
--font-display: 'Fraunces', Georgia, serif;
--font-body: 'Satoshi', system-ui, sans-serif;
```
Fonts: Fraunces + Satoshi. Safe: Georgia + Calibri.

Satoshi comes from Fontshare, not Google Fonts, so a deck that only links
Google Fonts will silently fall back. Either add the Fontshare stylesheet, or
use Karla, which is what `examples/checkout-recovery.html` does.

**Signature move.** A dashed line drawn in the accent colour threads across every
slide at low opacity, in a different position each time. It reads as a route, a
timeline, a current. One idea repeated is what makes a deck feel authored.

Italic serif for emphasis inside headlines, always in the accent colour. Numbers
sit large in the display face with `tabular-nums`.

**PowerPoint.** Holds well. Flat navy fill, gold-free accent on rules and
figures. The dashed motif becomes a single freeform line on section dividers
only, since repeating it on every slide is fussy to edit around.

---

## Signal Brief

Warm paper against deep navy, joined by one antique gold. Reads as a serious
document rather than a slideshow.

```css
--bg: #F0ECE3;  --bg2: #E6E0D4;  --stage-bg: #DCD5C7;
--ink: #1A2030; --muted: #5A6478; --accent: #A8813C;
--accent-soft: rgba(168,129,60,.14); --on-accent: #FFFFFF;
--panel: #FFFFFF; --panel-line: rgba(26,32,48,.14);
--surface-dark: #1C2644;
--font-display: 'Source Serif 4', Georgia, serif;
--font-body: 'IBM Plex Sans', Calibri, sans-serif;
--font-mono: 'IBM Plex Mono', Consolas, monospace;
```
Fonts: Source Serif 4 + IBM Plex Sans + IBM Plex Mono. Safe: Georgia + Calibri.

**Signature move.** Two surfaces used deliberately: cream for evidence and
analysis, navy for section breaks and the recommendation. Never blended on one
slide. Mono for every kicker, source line and page number, so the chrome reads as
a different voice from the argument.

Hairline rules separate regions. No rounded cards, no shadows.

**PowerPoint.** The best of the eight in .pptx. Flat fills, hairline rules and
serif type all translate exactly. Use this when the format is PowerPoint and the
audience is senior.

---

## Broadsheet

White page, black type, one red mark. Newspaper structure at slide scale.

```css
--bg: #FFFFFF;  --bg2: #F4F2EE;  --stage-bg: #E4E1DA;
--ink: #111111; --muted: #6B6B6B; --accent: #D0021B;
--accent-soft: rgba(208,2,27,.10); --on-accent: #FFFFFF;
--panel: #F7F5F1; --panel-line: rgba(17,17,17,.14);
--font-display: 'Playfair Display', Georgia, serif;
--font-body: 'Work Sans', Calibri, sans-serif;
```
Fonts: Playfair Display + Work Sans. Safe: Georgia + Calibri.

**Signature move.** A heavy rule above every headline, the width of the column
below it. Headlines set large and tight, body in narrow measure. The red appears
perhaps four times in a whole deck, and each time it means look here.

Survives a bad projector better than anything else here.

**PowerPoint.** Translates almost exactly. Rules become thin rectangles.

---

## Blueprint

Cool grey under a fine technical grid. Built to hold dense information calmly.

```css
--bg: #EEF1F4;  --bg2: #E4E8ED;  --stage-bg: #D3D9E0;
--ink: #16202B; --muted: #5F6C7A; --accent: #0B5FCE;
--accent-soft: rgba(11,95,206,.10); --on-accent: #FFFFFF;
--panel: #FFFFFF; --panel-line: rgba(22,32,43,.16);
--grid-line: rgba(22,32,43,.06);
--font-display: 'Space Grotesk', Arial, sans-serif;
--font-body: 'Inter Tight', Calibri, sans-serif;
--font-mono: 'JetBrains Mono', Consolas, monospace;
```
Fonts: Space Grotesk + Inter Tight + JetBrains Mono. Safe: Arial + Calibri.

**Signature move.** A 60px grid at very low opacity across every slide, with
content snapped to it visibly. Mono for all labels, axes, figures and callouts.
Measurement marks and thin leader lines annotate diagrams like a technical
drawing.

```css
.grid-bg {
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 60px 60px;
}
```

**PowerPoint.** Drop the grid rather than faking it, and keep the mono labels.
The precision reads through the type alone.

---

## Sunrise

Warm cream, terracotta and clay. Humanist and unhurried.

```css
--bg: #FBF6EF;  --bg2: #F5EBDD;  --stage-bg: #E8DCC9;
--ink: #2A211B; --muted: #7A6A5C; --accent: #C4623B;
--accent-soft: rgba(196,98,59,.13); --on-accent: #FFFFFF;
--panel: #FFFFFF; --panel-line: rgba(42,33,27,.12);
--accent-2: #6B8E6B;
--font-display: 'Fraunces', Georgia, serif;
--font-body: 'Karla', Calibri, sans-serif;
```
Fonts: Fraunces + Karla. Safe: Georgia + Calibri.

**Signature move.** Large soft organic shapes in clay and sage, bleeding off the
slide edge behind content at low opacity. Generous space, nothing crowded.
Photographs get rounded corners and a warm overlay so they sit inside the palette
rather than fighting it.

**PowerPoint.** The organic shapes become simple oval fills. Keep them few and
large.

---

## Graphite

Near-black, one hot accent, tight grotesque, ruthless hierarchy. Big numbers land
hard on this ground.

```css
--bg: #0C0C0E;  --bg2: #151519;  --stage-bg: #000000;
--ink: #F5F5F7; --muted: #8A8A93; --accent: #E8FF3A;
--accent-soft: rgba(232,255,58,.12); --on-accent: #0C0C0E;
--panel: rgba(255,255,255,.04); --panel-line: rgba(255,255,255,.10);
--font-display: 'Archivo', Impact, sans-serif;
--font-body: 'Archivo', Arial, sans-serif;
```
Fonts: Archivo, weights 400 through 900. Safe: Arial.

**Signature move.** One typeface across the whole deck, separated entirely by
weight. Headlines at 900 and very tight tracking, body at 400. The accent is
acidic and appears on perhaps one element per slide.

Statement slides carry a single sentence at 100px against near-black.

**PowerPoint.** Works well. Flat black fill, one bright accent, heavy type.
Avoid the panel transparencies and use a solid dark grey instead.

---

## Studio

Full-bleed colour blocks, oversized type, hard edges, no shadows anywhere.

```css
--bg: #1A1A1A;  --bg2: #262626;  --stage-bg: #0D0D0D;
--ink: #FFFFFF; --muted: rgba(255,255,255,.62); --accent: #FF5722;
--accent-2: #2E5BFF; --accent-3: #FFC400;
--accent-soft: rgba(255,87,34,.16); --on-accent: #1A1A1A;
--panel: #FF5722; --panel-line: transparent;
--font-display: 'Syne', Impact, sans-serif;
--font-body: 'Space Grotesk', Arial, sans-serif;
```
Fonts: Syne + Space Grotesk. Safe: Arial.

**Signature move.** Each slide is built from two or three flat colour panels
meeting at hard edges, with type crossing the boundary between them. Rotating
accent colours across the deck so no two consecutive slides share a scheme.
Section numbers set enormous, cropped by the slide edge.

Never a rounded corner, never a shadow.

**PowerPoint.** Translates almost perfectly, since flat colour blocks are what
PowerPoint does best. One of the strongest choices for .pptx.

---

## Clinic

White ground, restrained blue-grey, precise spacing, nothing decorative. Built so
the content is never upstaged.

```css
--bg: #FFFFFF;  --bg2: #F7F9FB;  --stage-bg: #E8ECF0;
--ink: #1B2733; --muted: #66788A; --accent: #2D6E8E;
--accent-soft: rgba(45,110,142,.10); --on-accent: #FFFFFF;
--panel: #F4F7F9; --panel-line: rgba(27,39,51,.12);
--font-display: 'Libre Franklin', Arial, sans-serif;
--font-body: 'Libre Franklin', Calibri, sans-serif;
```
Fonts: Libre Franklin. Safe: Arial or Calibri.

**Signature move.** Deliberately none. Hierarchy comes only from size, weight and
space. A single accent rule under each headline is the sole ornament.

Choose it when the material is serious enough that any styling would look like
spin, and when the deck will be printed, forwarded and annotated.

**PowerPoint.** Translates exactly. Nothing here is hard to reproduce.

---

## Adapting to a brand

When the user supplies brand colours, keep the preset's structure and swap the
palette:

- Their primary becomes `--accent`, used sparingly on what matters
- Their darkest neutral becomes `--ink`, their lightest becomes `--bg`
- Check contrast. Brand palettes are built for logos, not for body text at 22px.
- If the brand colour fails contrast against the background, use it for accents
  and rules only, and pick a readable near-black for text.

Never use all of a brand palette at once. Brands publish five colours and use two.
