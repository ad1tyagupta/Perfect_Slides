# Deck Types

Pick one framework and read only that file. The framework decides structure,
argument shape, density and citation habits. It does not decide design.

| Deck type | File | Use when |
|---|---|---|
| Pitch | `pitch-deck.md` | Raising money, or selling to a decision maker |
| Consulting, roadshow | `consulting-roadshow.md` | Presented live. Chart-led, sparse, one finding per slide |
| Consulting, working | `consulting-working.md` | Read and forwarded. Dense, sourced, self-contained |
| Marketing plan | `marketing-plan.md` | The quarterly or annual strategy. Internal planning |
| Campaign | `campaign.md` | One creative idea, pitched. Show the work |
| Research | `research.md` | Presenting findings. Method matters as much as the answer |
| Conference talk | `conference.md` | A stage, a room, a speaker |
| Internal update | `internal.md` | Team status, weekly or monthly |
| Teaching | `teaching.md` | Lessons, workshops, onboarding |

Short proven slide orders for around twenty more specific situations, such as a
quarterly business review or a competitor analysis, are in `scenarios.md`.

---

## Two pairs people confuse

**Consulting roadshow against consulting working deck.** Same discipline,
opposite densities. Measured from real decks, a Bain roadshow runs 24 words a
page and a McKinsey-style assessment runs 185, with its worst page at 507. That
is an eight-fold gap. Ask whether the deck is *presented* or *circulated*. If
both, build the roadshow and let the appendix carry the detail.

**Marketing plan against campaign.** A plan is the whole function over a quarter:
objectives, audiences, channels, budget, measurement. A campaign is one idea,
shown large, with the creative on screen. A plan that tries to be a campaign
feels thin. A campaign that tries to be a plan buries the idea.

---

## Density, measured

These are real numbers taken from professional templates, not estimates. Words
per slide, counting everything visible.

| Register | Words per slide | Looks like |
|---|---|---|
| Keynote, pitch | 20 to 40 | One idea, large type, heavy white space |
| General business | 40 to 70 | A headline, a chart, a short interpretation |
| Consulting deliverable | 100 to 200 | Two panels, annotated charts, source lines |
| Dense working deck | up to 250 | The ceiling. Past this, split the slide |

Anything over 250 words is two slides. No exceptions, and shrinking the type is
never the fix.

Live audience pushes density down. Circulation pushes it up.

---

## What every framework shares

These hold regardless of deck type:

1. **Headlines state the finding, not the topic.** See `writing/voice.md`.
2. **Show the number, do not describe it.** See `components/data-viz.md`.
3. **Nothing appears twice.**
4. **Every questionable claim carries a source.** How visibly, the framework decides.
5. **One interactive moment per HTML deck**, on the slide that carries most weight.

---

## Choosing when the user is vague

Ask what happens after the presentation. It resolves almost every case.

| They say | Build |
|---|---|
| "Investors are in the room" | Pitch |
| "I present it, then it gets forwarded" | Consulting roadshow, with an appendix |
| "The client reads it without me" | Consulting working |
| "We plan next quarter's marketing" | Marketing plan |
| "We sell this idea to the client" | Campaign |
| "I ran a study and I'm presenting results" | Research |
| "It's a talk at a conference" | Conference |
| "Weekly team sync" | Internal |
| "People are learning something" | Teaching |
