# Styling a Deck After a Brand

Read after the user picks a company from `brand-index.json`.

**These are website design systems, not slide templates.** Copying one wholesale
produces a deck that looks like a landing page, which is a specific and
recognisable kind of wrong. What follows is the translation.

---

## What transfers, and what does not

| Transfers | Does not |
|---|---|
| Palette, and the role each colour plays | Buttons, nav bars, form fields |
| Type pairing, and the ratio between sizes | Absolute pixel sizes |
| Corner radius language | Hover, focus and active states |
| Spacing rhythm, the underlying unit | Breakpoints and responsive rules |
| Elevation language, flat or shadowed | Cards as a default container |
| The feel, from Overview and Do's and Don'ts | Product UI screenshots |

The palette and the type pairing carry almost all of the recognition. Someone
looking at a Linear-styled deck knows it from the near-black ground, the violet
and the tight grotesque, not from anything structural.

---

## Rescaling type

A website sets body text around 16px on a roughly 1440px canvas. A deck is
1920px wide and read from across a room. Copying the pixel values gives text
nobody can read.

**Keep the ratios, discard the absolute sizes.**

1. Take the brand's type scale and work out the ratio between steps. A display
   size of 64 against a body of 16 is a 4:1 relationship.
2. Set deck body text at 24 to 32px, from `writing/voice.md`.
3. Rebuild the scale upward at the brand's ratio, then clamp to the deck limits.

A brand with a dramatic scale keeps its drama. A brand with a tight, even scale
keeps its evenness. That relationship is what reads as the brand, not the numbers.

Never go below the 18px floor whatever the brand does.

---

## Resolving fonts

Three steps, in order. `brand-index.json` gives the chain for each curated brand.

1. **The real font**, if it is open and on Google Fonts. IBM Plex, Inter, Lora
   and Space Grotesk are all free. Use them directly.
2. **The closest open substitute.** Most brand faces are licensed and cannot be
   loaded. Claude's Copernicus becomes Cormorant Garamond. Stripe's Sohne
   becomes Inter. Match the skeleton: serif against sans, the width, the
   contrast between thick and thin, the x-height.
3. **A PowerPoint-safe fallback**, for .pptx output. Georgia, Calibri, Arial.
   See `output/pptx.md`.

Say which substitution you made at delivery. "Styled after Stripe, using Inter
because Sohne is licensed" is honest and takes one line.

---

## Using the palette

Brands publish five to twenty colours and use two. Do the same.

- The brand's **primary becomes `--accent`**, used sparingly on what matters
- Its **darkest neutral becomes `--ink`**, its lightest becomes `--bg`
- Secondary brand colours become chart colours, not slide furniture

**Check contrast before committing.** Brand palettes are tuned for logos and
buttons, not for 24px body text across a room. If the brand colour fails against
the background, keep it for accents and rules and pick a readable near-black for
text. Do not dim the text to make the palette work.

Wise's acid green is a good example. It is superb as an accent and unreadable as
body text.

---

## Adapting the layout

Take the brand's spacing unit, usually 4 or 8px, and scale it to the deck. An
8px web unit becomes roughly a 12 to 16px deck unit. Every margin and gap
becomes a multiple.

Take the radius language as a category, not a number. Sharp, slightly softened,
or fully rounded. A web radius of 8px on a 300px card becomes 12 to 16px on a
600px slide panel, because radius should stay proportional to the shape.

Take the elevation language as a decision. Some brands are flat with hairline
borders, others use soft shadows. Pick one and hold it for the whole deck.

**Do not import their layouts.** A hero section, a three-column feature grid and
a pricing table are web page furniture. Slides need slide layouts, which come
from `components/catalog.md`.

---

## The honesty rules

Not optional, and they cost nothing.

- Describe the result as **"in the spirit of Linear"**, never as official, and
  never implying the deck is from that company
- **Never reproduce their logo or wordmark.** The user's own logo goes on the
  deck. Nobody else's
- Do not copy their marketing copy, taglines or product screenshots
- If the deck is for a client, say the styling is inspired by a public design
  system so nobody is surprised later

Using a public design language as a reference is ordinary design practice.
Passing a deck off as another company's is not, and the difference is entirely
in how it is presented.

---

## Building it

1. Read the brand's entry in `brand-index.json`
2. If the user named a brand from `also_available_by_name`, fetch its DESIGN.md
   from the source repo, then apply everything above
3. Fill the theme block in `output/html.md` with the translated values
4. Render the title-slide preview. Ask yourself whether it looks like a deck
   styled after the brand, or like their website with slides glued on. If the
   second, you imported layout rather than language
5. Run `verify_deck.py`. Brand palettes fail contrast more often than the
   built-in presets, because they were never designed for this

---

## When a brand does not translate

Some do not, and saying so is better than shipping something weak.

Ferrari, PlayStation and Nintendo lean almost entirely on photography, licensed
type and product imagery. Strip those and little remains but a colour.

If the chosen brand comes out thin, say which parts did not translate, show the
preview anyway, and offer the nearest built-in preset alongside it. The user
picks by looking, which is the whole point of showing three previews.
