# Component Catalogue

Every visual element the tool may use. Read this before designing a slide.

**The rule that governs this file:** nothing enters the catalogue without a
declared PowerPoint fallback. If a component cannot degrade honestly into native
editable shapes, it does not exist here — because a user who picked "Both" would
otherwise get a beautiful HTML deck and a broken .pptx.

Fallbacks are not apologies. A flip card that becomes two side-by-side panels is
still a good slide. Design the fallback deliberately, not as an afterthought.

---

## Motion

| Component | What it does | PowerPoint fallback |
|---|---|---|
| **Staggered reveal** | Elements fade and rise in sequence as the slide opens | Native entrance animations, same order and delays |
| **Count-up number** | A figure counts from zero to its value | Final value, styled identically |
| **Path draw** | A line draws itself across the slide | Freeform shape with a wipe animation |
| **Hover lift** | A card raises and brightens under the cursor | Static resting state |
| **Particle burst** | Celebratory scatter, closing slides only | Omitted — no honest equivalent, and it carries no information |

Staggered reveal is the workhorse. One well-paced entrance does more for a slide
than five scattered micro-animations. Reach for it first and stop there unless
the content genuinely needs more.

Motion carries meaning or it goes. A number counting up earns its animation
because the count *is* the point. A subtitle sliding in from the left does not.

---

## Data

The reason most decks are text-heavy is that showing the number is harder than
writing a sentence about it. These exist so the tool always has an easier path
to a chart than to a paragraph.

| Component | Use when | PowerPoint fallback |
|---|---|---|
| **Stat block** | One to three figures carry the whole slide | Text shapes — near-identical |
| **Bar chart** | Comparing quantities across categories | Native PowerPoint chart, data editable |
| **Line chart** | Change over time | Native PowerPoint chart, data editable |
| **Donut / pie** | Parts of one whole, five slices maximum | Native PowerPoint chart, data editable |
| **Waterfall** | Explaining how a total was reached | Native chart, or stacked shapes |
| **Funnel** | Sequential drop-off through stages | Trapezoid shapes with labels |
| **2×2 matrix** | Positioning options against two axes | Grouped shapes with a real axis |
| **Timeline** | Sequence of dated events | Line, markers and text shapes |
| **Comparison table** | Structured like-for-like detail | Native table |

Native charts matter more than they look. A PowerPoint chart carries its data
inside it, so the client can correct a number without rebuilding the slide.
A picture of a chart cannot. Always prefer the native chart.

**Five slices is the donut limit.** Past that nobody can read it, and the honest
move is a bar chart.

---

## Interaction — HTML only

These are the components that made the reference deck memorable, and they are
also the ones PowerPoint cannot hold. Each degrades to something that still
works, but the user should know what they are trading.

| Component | What it does | PowerPoint fallback |
|---|---|---|
| **Flip card** | Click to reveal the reverse | Both faces, side by side |
| **Tab switcher** | Toggle between comparable profiles | All panels shown, or one per slide |
| **Interactive chart** | Hover a segment for its detail | Static chart with all labels visible |
| **Device mockup** | Content shown inside a phone frame | Vector phone, one state |
| **Carousel** | Cycle through a set of items | One slide per item, or a grid |

**When the format is PowerPoint, do not design around these at all.** Do not
build a flip-card slide and then flatten it — design the flattened slide from the
start. Reduced versions of interactive ideas read as compromises, because they
are.

---

## Structure

| Component | Use when |
|---|---|
| **Section divider** | Marking a shift in the argument, every four to six slides |
| **Statement slide** | One sentence, full bleed — the line you want remembered |
| **Quote slide** | Customer voice, expert testimony, source material |
| **Split layout** | Image against text, or claim against evidence |
| **Card grid** | Three to six parallel items of equal weight |
| **Callout** | A single figure or warning pulled out of surrounding text |

Card grids are the most overused layout in existence. Before using one, check
that the items are genuinely parallel and genuinely equal in weight. If one
matters more than the others, the grid is hiding your argument.

---

## Choosing

Work down this list. Stop at the first that fits:

1. Is it **one number**? → stat block
2. Is it a **comparison**? → bar chart, or a table if the detail matters
3. Is it **change over time**? → line chart
4. Is it a **sequence**? → timeline or funnel
5. Is it a **single idea**? → statement slide
6. Is it **parallel items**? → card grid, three to six
7. None of these → it is probably two slides, not one

If a slide needs a paragraph to explain its own chart, the chart is wrong.
