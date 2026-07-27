# Voice

How the words on the slide should sound. Read this before writing any copy.

The test for every line: **would a competent person say this out loud to a room
without feeling embarrassed?** If not, rewrite it.

---

## Four bans

### 1. Punctuation

- **No em dashes.** Not one. Use a full stop and start a new sentence, or
  restructure. Substituting an en dash is the same offence wearing a hat.
- **No semicolons.** If two clauses are related enough to need one, they are two
  sentences.
- **No colons in headlines.** `Retention: A Deep Dive` is a filing label, not a
  headline. Write the finding instead.
- **No exclamation marks.** The content carries the emphasis.

Slide copy lives in short declarative sentences. If a line needs a comma to hold
itself together, it is too long for a slide.

### 2. Filler vocabulary

Never use these, or anything in their family:

> leverage · seamless · robust · cutting-edge · delve · landscape · realm ·
> unlock · empower · elevate · harness · navigate (figuratively) · journey ·
> ecosystem · synergy · holistic · game-changing · transformative ·
> best-in-class · world-class · state-of-the-art · paradigm · pivotal ·
> testament to · at the forefront · in the realm of

Every one of these is a word that sounds like meaning without carrying any. The
fix is always the same: say the specific thing.

> ✗ We leverage cutting-edge analytics to unlock growth
> ✓ We read the checkout logs. Three fixes recovered 8% of abandoned carts.

### 3. AI sentence shapes

- **No "it's not just X, it's Y."** Also banned: "this isn't about X. It's about
  Y." The construction announces profundity instead of delivering it.
- **No rule of three by default.** Three adjectives, three clauses, three bullets
  because three feels complete. Use the number of items that exist. If there are
  two, write two.
- **No scene-setting openers.** "In today's fast-paced world", "As we all know",
  "Now more than ever", "Imagine a world where". Delete and start at the point.
- **No rhetorical questions as headlines.** "So what does this mean?" means the
  headline is missing.
- **No throat-clearing.** The first sentence of a draft is usually warm-up.
  Delete it and check whether anything was lost.

### 4. Repetition

- The body never restates the title. If the headline says revenue fell 12%, the
  body explains why, not that it fell.
- No point appears twice in the deck. If it needs saying again, the first slide
  was in the wrong place.
- No word appears twice in one headline.
- Do not summarise a slide on the slide. That is what the headline is for.

---

## Headlines carry the argument

The single largest improvement available to any deck.

**Write the finding, not the topic.** A headline that names a subject makes the
audience read the whole slide to learn what it says. A headline that states the
conclusion lets them read the slide as evidence.

> ✗ Q3 Revenue Overview
> ✓ Revenue fell 12% in Q3, driven entirely by churn

> ✗ Market Analysis
> ✓ Three competitors entered our price band this year

> ✗ Our Solution
> ✓ Fixing checkout recovers more revenue than new acquisition

**Then check the sequence.** Read every headline in order, ignoring the slides.
They should form the argument end to end. If they read as a table of contents,
they are topics. Rewrite them as findings.

This is how consulting decks work and it is why they survive being forwarded.

---

## Word budgets

| Element | Limit |
|---|---|
| Headline | 12 words, one line |
| Statement slide | 15 words |
| Bullet | 10 words, no full stop |
| Body sentence | 20 words |
| Caption | 8 words |
| Stat label | 6 words |

Budgets are ceilings, not targets. Half is usually better.

If content will not fit, split the slide. Never shrink type to make text fit.
A slide that needs 9pt is two slides wearing a trench coat.

---

## Type sizes

Sizes are in stage pixels, on the 1920x1080 canvas. Halve them for the
equivalent in points on a real slide.

| Element | Size | Never below |
|---|---|---|
| Statement slide | 76-140px | 60px |
| Slide headline | 48-64px | 40px |
| Subhead, lead-in | 28-34px | 24px |
| Body, bullets | 24-32px | 20px |
| Stat figure | 90-140px | 64px |
| Stat label, caption | 20-24px | 18px |
| Source line, fine print | 19-20px | **18px** |

**18px is the hard floor and `verify_deck.py` fails anything under it.** At
stage scale that is roughly 9pt, which nobody reads past the third row and which
disappears entirely on a projector.

Source lines and captions sit right on the floor by design. They are meant to be
quiet, not invisible. If something genuinely cannot fit at 18px, it does not
belong on the slide.

---

## Numbers

- A number beats an adjective every time. Not "significant growth" but "growth
  from 400 to 1,900 users".
- Round for speech. Say 1.9k or "about 2,000", not 1,873, unless the exact figure
  is the point.
- Every number a reasonable person would question needs a source. See the deck
  type for where the citation goes.
- Never write a percentage without its base. "Up 40%" from what?

---

## Tone by deck type

The bans hold everywhere. Register moves.

| Deck type | Sounds like |
|---|---|
| Pitch | Confident, specific, short. No hedging. State the ask plainly. |
| Consulting, roadshow | Declarative. The title states the finding and stops. |
| Consulting, working | Measured and sourced. Findings before recommendations. |
| Marketing plan | Businesslike. Owners, numbers, dates. |
| Campaign | Closer to speech. Contractions fine. Still no filler. |
| Research | Precise. Hedge where hedging is honest, unique to this type. |
| Conference talk | Spoken register. Fragments allowed. Slides support the voice. |
| Internal update | Direct and unceremonious. Say what changed and what you need. |
| Teaching | Patient and plain. Define terms once, then use them. |

Research is the one exception to the no-hedging rule. "Suggests" and "is
consistent with" are correct when that is what the data supports. Everywhere
else, hedging is padding.

---

## Before finishing

Check every one:

1. No em dashes, semicolons, headline colons or exclamation marks
2. No word from the filler list
3. No banned sentence shape
4. Headlines read in sequence as the argument
5. Nothing said twice
6. Every number has a base and, where it matters, a source
7. Read aloud without wincing
