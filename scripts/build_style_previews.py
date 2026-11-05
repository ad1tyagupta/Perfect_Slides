#!/usr/bin/env python3
"""
Rebuild examples/style-previews.html.

One title slide per preset in references/design/presets.md, each carrying that
preset's own palette, fonts and signature move. The file is composed from the
repository's own parts rather than written by hand: the stage is
references/components/stage.css verbatim, the behaviour is
references/components/deck.js verbatim, and every palette below is copied out
of presets.md.

Run it after changing a preset, or the preview starts lying about the preset.

Usage:
    python build_style_previews.py

Requires:
    nothing
"""
import io
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
stage_css = io.open(REPO / "references/components/stage.css", encoding="utf-8").read()
deck_js = io.open(REPO / "references/components/deck.js", encoding="utf-8").read()

FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600"
    "&family=Karla:wght@400;500;700"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600"
    "&family=IBM+Plex+Sans:wght@400;500;600"
    "&family=IBM+Plex+Mono:wght@400;500"
    "&family=Playfair+Display:ital,wght@0,500..900;1,500..700"
    "&family=Work+Sans:wght@400;500;600"
    "&family=Space+Grotesk:wght@400;500;700"
    "&family=Inter+Tight:wght@400;500;600"
    "&family=JetBrains+Mono:wght@400;500"
    "&family=Archivo:wght@400;600;800;900"
    "&family=Syne:wght@700;800"
    "&family=Libre+Franklin:wght@300;400;500;600"
    "&display=swap"
)

THEMES = """
/* Each preview carries its own tokens, scoped to the slide. Nothing leaks.
   The values are copied verbatim from references/design/presets.md, so what
   you see here is what the preset actually renders. */

.slide[data-style="night-ride"] {
    --slide-bg: #0E2635; --bg2: #123448;
    --ink: #EAF4F8; --muted: #8FB2C0; --accent: #00A8D8;
    --accent-soft: rgba(0,168,216,.16); --on-accent: #062130;
    --panel: rgba(255,255,255,.05); --panel-line: rgba(255,255,255,.12);
    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'Karla', system-ui, sans-serif;
}
.slide[data-style="signal-brief"] {
    --slide-bg: #F0ECE3; --bg2: #E6E0D4;
    --ink: #1A2030; --muted: #5A6478; --accent: #A8813C;
    --accent-soft: rgba(168,129,60,.14); --on-accent: #FFFFFF;
    --panel: #FFFFFF; --panel-line: rgba(26,32,48,.14);
    --surface-dark: #1C2644;
    --font-display: 'Source Serif 4', Georgia, serif;
    --font-body: 'IBM Plex Sans', Calibri, sans-serif;
    --font-mono: 'IBM Plex Mono', Consolas, monospace;
}
.slide[data-style="broadsheet"] {
    --slide-bg: #FFFFFF; --bg2: #F4F2EE;
    --ink: #111111; --muted: #6B6B6B; --accent: #D0021B;
    --accent-soft: rgba(208,2,27,.10); --on-accent: #FFFFFF;
    --panel: #F7F5F1; --panel-line: rgba(17,17,17,.14);
    --font-display: 'Playfair Display', Georgia, serif;
    --font-body: 'Work Sans', Calibri, sans-serif;
}
.slide[data-style="blueprint"] {
    --slide-bg: #EEF1F4; --bg2: #E4E8ED;
    --ink: #16202B; --muted: #5F6C7A; --accent: #0B5FCE;
    --accent-soft: rgba(11,95,206,.10); --on-accent: #FFFFFF;
    --panel: #FFFFFF; --panel-line: rgba(22,32,43,.16);
    --grid-line: rgba(22,32,43,.06);
    --font-display: 'Space Grotesk', Arial, sans-serif;
    --font-body: 'Inter Tight', Calibri, sans-serif;
    --font-mono: 'JetBrains Mono', Consolas, monospace;
}
.slide[data-style="sunrise"] {
    --slide-bg: #FBF6EF; --bg2: #F5EBDD;
    --ink: #2A211B; --muted: #7A6A5C; --accent: #C4623B;
    --accent-soft: rgba(196,98,59,.13); --on-accent: #FFFFFF;
    --panel: #FFFFFF; --panel-line: rgba(42,33,27,.12);
    --accent-2: #6B8E6B;
    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'Karla', Calibri, sans-serif;
}
.slide[data-style="graphite"] {
    --slide-bg: #0C0C0E; --bg2: #151519;
    --ink: #F5F5F7; --muted: #8A8A93; --accent: #E8FF3A;
    --accent-soft: rgba(232,255,58,.12); --on-accent: #0C0C0E;
    --panel: rgba(255,255,255,.04); --panel-line: rgba(255,255,255,.10);
    --font-display: 'Archivo', Impact, sans-serif;
    --font-body: 'Archivo', Arial, sans-serif;
}
.slide[data-style="studio"] {
    --slide-bg: #1A1A1A; --bg2: #262626;
    --ink: #FFFFFF; --muted: rgba(255,255,255,.62); --accent: #FF5722;
    --accent-2: #2E5BFF; --accent-3: #FFC400;
    --accent-soft: rgba(255,87,34,.16); --on-accent: #1A1A1A;
    --panel: #FF5722; --panel-line: transparent;
    --font-display: 'Syne', Impact, sans-serif;
    --font-body: 'Space Grotesk', Arial, sans-serif;
}
.slide[data-style="clinic"] {
    --slide-bg: #FFFFFF; --bg2: #F7F9FB;
    --ink: #1B2733; --muted: #66788A; --accent: #2D6E8E;
    --accent-soft: rgba(45,110,142,.10); --on-accent: #FFFFFF;
    --panel: #F4F7F9; --panel-line: rgba(27,39,51,.12);
    --font-display: 'Libre Franklin', Arial, sans-serif;
    --font-body: 'Libre Franklin', Calibri, sans-serif;
}
"""

LAYOUT = """
/* Shared ------------------------------------------------------------------ */
.slide {
    color: var(--ink);
    font-family: var(--font-body);
    --dur: .7s;
    --ease: cubic-bezier(.16, 1, .3, 1);
}
.pad { position: absolute; inset: 0; padding: 110px 130px; display: flex;
       flex-direction: column; justify-content: center; }
.kick { font-size: 24px; letter-spacing: .20em; text-transform: uppercase;
        color: var(--accent); font-weight: 600; }
.sub  { font-size: 32px; line-height: 1.5; color: var(--muted);
        max-width: 1020px; margin-top: 38px; }
.foot { position: absolute; left: 130px; bottom: 74px; font-size: 22px;
        color: var(--muted); }
.tag  { position: absolute; right: 130px; bottom: 74px; font-size: 20px;
        letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }

/* 1 · Night Ride — a dashed route threading the slide --------------------- */
[data-style="night-ride"] .route { position: absolute; inset: 0; width: 1920px;
    height: 1080px; fill: none; }
[data-style="night-ride"] .route path { stroke: var(--accent); stroke-width: 3;
    stroke-dasharray: 16 20; opacity: .42; }
[data-style="night-ride"] .route circle { fill: var(--accent); opacity: .75; }
[data-style="night-ride"] h1 { font-family: var(--font-display); font-size: 128px;
    line-height: 1.02; font-weight: 600; letter-spacing: -.02em; margin-top: 34px; }
[data-style="night-ride"] h1 em { display: block; font-style: italic;
    color: var(--accent); font-weight: 500; }

/* 2 · Signal Brief — two surfaces, mono chrome, hairline rules ------------ */
[data-style="signal-brief"] .band { position: absolute; right: 0; top: 0;
    width: 560px; height: 1080px; background: var(--surface-dark); }
[data-style="signal-brief"] .band span { position: absolute; left: 70px;
    bottom: 96px; width: 420px; font-family: var(--font-mono); font-size: 21px;
    line-height: 1.75; color: rgba(255,255,255,.72); }
[data-style="signal-brief"] .band i { display: block; width: 64px; height: 3px;
    background: var(--accent); margin-bottom: 30px; }
[data-style="signal-brief"] .pad { padding-right: 700px; }
[data-style="signal-brief"] .kick { font-family: var(--font-mono);
    font-size: 21px; letter-spacing: .16em; color: var(--muted); font-weight: 400; }
[data-style="signal-brief"] .rule { width: 100%; height: 1px;
    background: var(--panel-line); margin: 30px 0 34px; }
[data-style="signal-brief"] h1 { font-family: var(--font-display); font-size: 92px;
    line-height: 1.1; font-weight: 600; letter-spacing: -.015em; }
[data-style="signal-brief"] h1 b { color: var(--accent); font-weight: 600; }

/* 3 · Broadsheet — a heavy rule, then the headline ------------------------ */
[data-style="broadsheet"] .masthead { display: flex; justify-content: space-between;
    align-items: baseline; font-family: var(--font-body); font-size: 22px;
    letter-spacing: .18em; text-transform: uppercase; color: var(--muted); }
[data-style="broadsheet"] .heavy { height: 10px; background: var(--ink);
    margin: 26px 0 46px; }
[data-style="broadsheet"] h1 { font-family: var(--font-display); font-size: 118px;
    line-height: .99; font-weight: 800; letter-spacing: -.025em; max-width: 1480px; }
[data-style="broadsheet"] h1 mark { background: none; color: var(--accent); }
[data-style="broadsheet"] .cols { display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 54px; margin-top: 56px; max-width: 1460px; }
[data-style="broadsheet"] .cols p { font-size: 25px; line-height: 1.55;
    color: var(--muted); }
[data-style="broadsheet"] .cols p:first-child { color: var(--ink); }

/* 4 · Blueprint — a 60px grid, mono labels, a leader line ----------------- */
[data-style="blueprint"] .grid-bg { position: absolute; inset: 0;
    background-image: linear-gradient(var(--grid-line) 1px, transparent 1px),
                      linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 60px 60px; }
[data-style="blueprint"] .kick { font-family: var(--font-mono); font-size: 21px;
    letter-spacing: .14em; color: var(--muted); font-weight: 400; }
[data-style="blueprint"] h1 { font-family: var(--font-display); font-size: 104px;
    line-height: 1.06; font-weight: 500; letter-spacing: -.03em; margin-top: 30px;
    max-width: 1280px; }
[data-style="blueprint"] h1 u { text-decoration: none; color: var(--accent);
    box-shadow: inset 0 -14px 0 var(--accent-soft); }
[data-style="blueprint"] .callout { position: absolute; right: 130px; top: 300px;
    width: 420px; font-family: var(--font-mono); font-size: 20px; line-height: 1.7;
    color: var(--muted); border-left: 2px solid var(--accent); padding-left: 26px; }
[data-style="blueprint"] .callout b { display: block; color: var(--ink);
    font-size: 54px; font-weight: 500; margin-bottom: 10px; }

/* 5 · Sunrise — organic shapes bleeding off the edge ---------------------- */
[data-style="sunrise"] .bleed { position: absolute; inset: 0; overflow: hidden; }
[data-style="sunrise"] .blob { position: absolute; border-radius: 50%;
    filter: blur(.4px); }
[data-style="sunrise"] .b1 { width: 860px; height: 860px; right: -230px;
    top: -210px; background: var(--accent); opacity: .14; }
[data-style="sunrise"] .b2 { width: 620px; height: 620px; right: 180px;
    bottom: -300px; background: var(--accent-2); opacity: .16; }
[data-style="sunrise"] .b3 { width: 300px; height: 300px; left: -120px;
    bottom: 120px; background: var(--accent); opacity: .10; }
[data-style="sunrise"] .pad { padding-right: 760px; }
[data-style="sunrise"] h1 { font-family: var(--font-display); font-size: 110px;
    line-height: 1.06; font-weight: 500; letter-spacing: -.02em; margin-top: 32px; }
[data-style="sunrise"] h1 em { font-style: italic; color: var(--accent); }

/* 6 · Graphite — one weight apart, one acid accent ------------------------ */
[data-style="graphite"] .pad { justify-content: flex-end; padding-bottom: 180px; }
[data-style="graphite"] .kick { color: var(--accent); font-size: 22px;
    letter-spacing: .26em; font-weight: 600; }
[data-style="graphite"] h1 { font-family: var(--font-display); font-size: 136px;
    line-height: .98; font-weight: 900; letter-spacing: -.045em; margin-top: 40px;
    max-width: 1520px; }
[data-style="graphite"] h1 span { color: var(--accent); }
[data-style="graphite"] .meta { display: flex; gap: 90px; margin-top: 70px; }
[data-style="graphite"] .meta div { font-size: 22px; color: var(--muted);
    font-weight: 400; }
[data-style="graphite"] .meta b { display: block; color: var(--ink);
    font-size: 46px; font-weight: 800; letter-spacing: -.02em; margin-bottom: 6px; }

/* 7 · Studio — flat blocks, hard edges, a cropped number ------------------ */
[data-style="studio"] .blk { position: absolute; }
[data-style="studio"] .k1 { left: 0; top: 0; width: 760px; height: 1080px;
    background: var(--accent); }
[data-style="studio"] .k2 { right: 0; top: 0; width: 1160px; height: 404px;
    background: var(--accent-2); }
[data-style="studio"] .num { position: absolute; left: 52px; bottom: 0;
    width: 700px; height: 430px; overflow: hidden;
    font-family: var(--font-display); font-size: 440px; font-weight: 800;
    line-height: 1.02; letter-spacing: -.05em;
    color: var(--on-accent); opacity: .26; }
[data-style="studio"] .pad { padding-left: 860px; padding-top: 140px;
    justify-content: flex-start; }
[data-style="studio"] .kick { color: var(--ink); opacity: .9; }
[data-style="studio"] h1 { font-family: var(--font-display); font-size: 108px;
    line-height: 1.0; font-weight: 800; letter-spacing: -.03em; margin-top: 150px;
    max-width: 900px; }
[data-style="studio"] .sub { color: rgba(255,255,255,.76); max-width: 820px; }

/* 8 · Clinic — no ornament but one rule ----------------------------------- */
[data-style="clinic"] .kick { color: var(--muted); font-weight: 500;
    font-size: 22px; letter-spacing: .18em; }
[data-style="clinic"] h1 { font-family: var(--font-display); font-size: 96px;
    line-height: 1.12; font-weight: 600; letter-spacing: -.028em; margin-top: 30px;
    max-width: 1420px; }
[data-style="clinic"] .accent-rule { width: 180px; height: 5px;
    background: var(--accent); margin-top: 48px; }
[data-style="clinic"] .facts { display: grid; grid-template-columns: repeat(3, 320px);
    gap: 64px; margin-top: 64px; }
[data-style="clinic"] .facts b { display: block; font-size: 58px; font-weight: 600;
    letter-spacing: -.02em; color: var(--accent); }
[data-style="clinic"] .facts span { display: block; font-size: 23px; line-height: 1.5;
    color: var(--muted); margin-top: 10px; }
"""

SLIDES = """
  <!-- 1 ====================================================== Night Ride -->
  <section class="slide active" data-style="night-ride">
    <svg class="route" viewBox="0 0 1920 1080" preserveAspectRatio="none">
      <path d="M -40 840 C 320 740, 560 980, 900 900 S 1520 660, 1980 790"/>
      <circle cx="320" cy="805" r="9"/><circle cx="900" cy="900" r="9"/>
    </svg>
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Brand campaign &middot; Q1 2027</div>
      <h1 class="reveal" style="--d:.15">Nobody remembers<em>the second message</em></h1>
      <p class="sub reveal" style="--d:.3">One idea, four channels, measured in
         recall rather than reach.</p>
    </div>
    <div class="foot reveal" style="--d:.45">Northwind &middot; Brand team</div>
    <div class="speaker-notes">Preset: night-ride. Signature move: a dashed route
      threading every slide at low opacity, in a different position each time.</div>
  </section>

  <!-- 2 ==================================================== Signal Brief -->
  <section class="slide" data-style="signal-brief">
    <div class="band">
      <span><i></i>Prepared for the board<br>Circulated 14 February<br>
        Commercially confidential</span>
    </div>
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Board paper &middot; 14 February 2027</div>
      <div class="rule reveal" style="--d:.1"></div>
      <h1 class="reveal" style="--d:.18">The merger pays for itself in the
         <b>third year</b>, not the first</h1>
      <p class="sub reveal" style="--d:.32">Integration cost lands early and the
         revenue synergy lands late. The plan should say so.</p>
    </div>
    <div class="foot reveal" style="--d:.45">Lindgren Partners</div>
    <div class="speaker-notes">Preset: signal-brief. Signature move: two surfaces
      used deliberately, cream for analysis and navy for the break. Mono chrome.</div>
  </section>

  <!-- 3 ====================================================== Broadsheet -->
  <section class="slide" data-style="broadsheet">
    <div class="pad">
      <div class="masthead reveal" style="--d:.05">
        <span>Housing Review 2027</span><span>Section one &middot; Affordability</span>
      </div>
      <div class="heavy reveal" style="--d:.12"></div>
      <h1 class="reveal" style="--d:.2">Rents outran wages in <mark>nineteen</mark>
         of twenty cities</h1>
      <div class="cols reveal" style="--d:.34">
        <p>The gap widened fastest where construction had already stalled, which
           rules out supply as the whole story.</p>
        <p>Only one city closed the gap. It did so by changing what counts as
           permitted density, not by building faster.</p>
        <p>Every figure here comes from the same registry, so the cities can be
           compared without adjustment.</p>
      </div>
    </div>
    <div class="speaker-notes">Preset: broadsheet. Signature move: a heavy rule the
      width of the column, and red used perhaps four times in a whole deck.</div>
  </section>

  <!-- 4 ======================================================= Blueprint -->
  <section class="slide" data-style="blueprint">
    <div class="grid-bg"></div>
    <div class="pad">
      <div class="kick reveal" style="--d:.05">System review / 2026-11</div>
      <h1 class="reveal" style="--d:.16">Ninety percent of our latency
         is <u>one queue</u></h1>
      <p class="sub reveal" style="--d:.3">Everything downstream of it is already
         fast enough. We have been optimising the wrong half.</p>
    </div>
    <div class="callout reveal" style="--d:.4">
      <b>412 ms</b>median time a request spends waiting in the ingest queue,
      against 44 ms for all remaining work
    </div>
    <div class="foot reveal" style="--d:.5">Platform group</div>
    <div class="speaker-notes">Preset: blueprint. Signature move: a 60px grid with
      content snapped to it visibly, and mono for every label and figure.</div>
  </section>

  <!-- 5 ========================================================= Sunrise -->
  <section class="slide" data-style="sunrise">
    <div class="bleed">
      <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
    </div>
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Retention study &middot; Spring</div>
      <h1 class="reveal" style="--d:.16">Growth came from the customers
         we <em>almost dropped</em></h1>
      <p class="sub reveal" style="--d:.3">The accounts we scored lowest renewed
         at the highest rate once someone called them.</p>
    </div>
    <div class="foot reveal" style="--d:.45">Customer research</div>
    <div class="speaker-notes">Preset: sunrise. Signature move: large soft organic
      shapes in clay and sage bleeding off the slide edge behind the content.</div>
  </section>

  <!-- 6 ======================================================== Graphite -->
  <section class="slide" data-style="graphite">
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Series A &middot; Confidential</div>
      <h1 class="reveal" style="--d:.15">We are three weeks from
         <span>running out of road.</span></h1>
      <div class="meta reveal" style="--d:.32">
        <div><b>11</b>weeks of runway</div>
        <div><b>&euro;2.4m</b>asked</div>
        <div><b>18&times;</b>pipeline cover</div>
      </div>
    </div>
    <div class="speaker-notes">Preset: graphite. Signature move: one typeface across
      the deck separated only by weight, and an acid accent on one element.</div>
  </section>

  <!-- 7 ========================================================== Studio -->
  <section class="slide" data-style="studio">
    <div class="blk k1"><div class="num">04</div></div>
    <div class="blk k2"></div>
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Chapter four</div>
      <h1 class="reveal" style="--d:.16">Interfaces that argue back</h1>
      <p class="sub reveal" style="--d:.3">What happens to a product when the
         cheapest thing in it is an opinion.</p>
    </div>
    <div class="speaker-notes">Preset: studio. Signature move: two or three flat
      colour panels meeting at hard edges, section numbers cropped by the edge.</div>
  </section>

  <!-- 8 ========================================================== Clinic -->
  <section class="slide" data-style="clinic">
    <div class="pad">
      <div class="kick reveal" style="--d:.05">Phase II results</div>
      <h1 class="reveal" style="--d:.15">The treatment works, and only for the
         group we did not target</h1>
      <div class="accent-rule reveal" style="--d:.26"></div>
      <div class="facts reveal" style="--d:.36">
        <div><b>+31%</b><span>response in the over-sixties</span></div>
        <div><b>No effect</b><span>in the enrolled primary cohort</span></div>
        <div><b>n = 1,204</b><span>across nine sites, two countries</span></div>
      </div>
    </div>
    <div class="foot reveal" style="--d:.5">Nine-site collaborative trial</div>
    <div class="speaker-notes">Preset: clinic. Signature move: deliberately none.
      Hierarchy from size, weight and space, with one accent rule as the ornament.</div>
  </section>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Perfect Slides &middot; style previews</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">

<style>
/* ===========================================================================
   STYLE PREVIEWS

   One title slide per built-in preset, each carrying that preset's own palette,
   fonts and signature move. Arrow keys or swipe to compare them.

   This file is generated from the repo's own parts: the stage below is
   references/components/stage.css verbatim, the behaviour is
   references/components/deck.js verbatim, and every palette is copied from
   references/design/presets.md. Nothing here is a mock-up.
   =========================================================================== */

:root {{ --stage-bg: #15181C; --slide-bg: #FFFFFF; }}

{stage_css}

{THEMES}

{LAYOUT}

.speaker-notes {{ display: none; }}
</style>
</head>
<body>

<div class="deck-progress"></div>

<div class="deck-viewport">
  <main class="deck-stage" id="deckStage">
{SLIDES}
  </main>
</div>

<script>
{deck_js}
</script>
</body>
</html>
"""

out = REPO / "examples/style-previews.html"
io.open(out, "w", encoding="utf-8").write(html)
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
