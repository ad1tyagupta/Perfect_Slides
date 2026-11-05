---
name: perfect-slides
description: Build presentations as animated HTML decks or editable PowerPoint files. Use when the user wants to create a presentation, pitch deck, slide deck, consulting deck, or talk, convert a PDF/Word/PowerPoint document into slides, or improve an existing deck. Handles research, writing, design and export.
user-invocable: true
argument-hint: [what the deck is about]
---

# Perfect Slides

This skill is a thin pointer. Everything lives in plain files so the tool works
in any coding agent, not only this one.

**Read `${CLAUDE_PLUGIN_ROOT}/AGENTS.md` now**, then follow it. Every path it
names is relative to `${CLAUDE_PLUGIN_ROOT}`.

It routes to:

- `references/workflow/intake.md` — always first, before anything is built
- `references/narrative/` — structure per deck type
- `references/writing/voice.md` — how the words should sound
- `references/design/` — style selection and design rules
- `references/components/` — what can go on a slide
- `references/output/` — building HTML or PowerPoint
- `scripts/` — pptx builder, document ingest, deck checker

Scripts run from the plugin directory, with the deck written into the user's own
working directory:

```
python ${CLAUDE_PLUGIN_ROOT}/scripts/build_pptx.py deck.json out.pptx
python ${CLAUDE_PLUGIN_ROOT}/scripts/verify_deck.py deck.html --shots ./shots
```

## The rules that matter most

1. Never build before intake is finished.
2. Two checkpoints with the user, never three. Assume and flag instead of asking again.
3. Show data, do not describe it.
4. Headlines state the finding, not the topic.
5. Run `scripts/verify_deck.py` before saying it is done.
