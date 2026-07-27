# Examples

The same nine-slide deck in both formats, so you can see exactly what the two
outputs give you.

| File | What it is |
|---|---|
| `checkout-recovery.html` | Open it in a browser. Arrows to move, `F` fullscreen, `P` presenter view |
| `checkout-recovery.pptx` | Open in PowerPoint. Click a chart and edit the data |
| `checkout-recovery.deck.json` | The spec the .pptx was built from |

A consulting deck: a finding, the evidence, the options, the recommendation, the ask.

---

## Worth looking at

**Every headline is a finding.** Read them in order and you get the whole
argument without opening a single slide:

> Checkout is where the revenue leaks · We lose 8% of carts to a bug we have
> known about since March · Abandonment rose every month since March · Safari
> carries almost all of the loss · Three fixes, in shipping order · Three weeks,
> one engineer

**Numbers are shown, not described.** Nine slides carry one line chart, one bar
chart, one donut, three counting statistics and a timeline. Almost no prose.

**One interaction, on the slide that matters.** The flip cards on slide 7. Not
on every slide, because then it stops being remarkable.

**One repeating motif.** The dashed route line appears on the title and the
timeline in different positions. One idea repeated is what makes a deck look
authored rather than assembled.

**Every data slide names its source.** Bottom left, small, always there.

---

## Rebuild them

```bash
python scripts/build_pptx.py examples/checkout-recovery.deck.json out.pptx
python scripts/verify_deck.py examples/checkout-recovery.html --shots ./shots
```

The checker reports nine slides, both webfonts loaded, no problems.

---

## The difference between the two

The HTML has the drawing line chart, the growing bars, the counting numbers, the
hoverable donut and the flip cards.

The .pptx has native editable charts with their data inside the file, real
selectable text, and speaker notes in the notes pane. The flip cards are flat
panels and nothing animates.

Neither is worse. They are for different moments.

Note the font warning the builder prints: the design calls for Fraunces and
Satoshi, and the .pptx uses Georgia and Calibri so it opens correctly on any
machine. That is the trade PowerPoint asks for, and the tool says so out loud
rather than letting you find out in front of a client.
