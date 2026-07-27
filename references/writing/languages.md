# Languages

Decks can be built in any language. Read this whenever the deck is not in
English, or mixes languages.

Ask which language at intake if it is not obvious. Never assume English because
the request arrived in English. People routinely brief in one language and
present in another.

---

## What carries across, and what does not

From `voice.md`, these hold in every language:

- Headlines state the finding, not the topic
- Nothing is said twice
- Numbers beat adjectives
- No filler vocabulary
- Read it aloud

These are Latin-script specific and need translating, not copying:

- The em dash ban. Other scripts have their own fussy punctuation. Chinese has
  the full-width dash `——` and the enumeration comma `、`. The principle is the
  same: plain marks, short sentences.
- The filler word list. Every language has its own corporate mush. German has
  *ganzheitlich* and *nachhaltig* used as noise. Spanish has *sinergia* and
  *apostar por*. Build the equivalent list for the target language and apply the
  same test: does this word carry meaning, or does it only sound like it does?

---

## Type by script

| Script | Display and body | Notes |
|---|---|---|
| Latin | Wide choice | Default rules apply |
| Cyrillic | Most quality Latin faces cover it | Check the font actually ships Cyrillic before committing |
| Greek | Many Latin faces cover it | Same check |
| Chinese (Simplified) | Noto Sans SC, Noto Serif SC | |
| Chinese (Traditional) | Noto Sans TC, Noto Serif TC | Do not substitute Simplified |
| Japanese | Noto Sans JP, Noto Serif JP | |
| Korean | Noto Sans KR, Noto Serif KR | |
| Arabic | Noto Sans Arabic, Cairo, Tajawal | Right to left |
| Hebrew | Noto Sans Hebrew, Heebo, Rubik | Right to left |
| Devanagari | Noto Sans Devanagari, Mukta | Needs extra line height |
| Thai | Noto Sans Thai, Sarabun | Needs extra line height |

Pick the font before designing the slide. A layout built for a compact Latin face
will break when the text becomes Devanagari and every line grows taller.

---

## CJK adjustments

Chinese, Japanese and Korean text breaks under Latin typographic habits:

- **Letter spacing stays at zero.** Tracking CJK looks broken. Never apply the
  wide-tracked uppercase label treatment to CJK text.
- **Line height goes up**, roughly 1.6 to 1.8 against 1.3 to 1.4 for Latin.
  Dense characters need vertical room.
- **No uppercase transform.** There is no uppercase. The rule silently does
  nothing, which means any design leaning on it loses that layer entirely.
- **No italics.** Synthetic slanting of CJK looks like a rendering fault. Use
  weight or colour for emphasis instead.
- **Avoid the lightest weights.** Thin CJK strokes disappear on a projector.
- **Count characters, not words.** A CJK headline of 20 characters is roughly a
  12 word English headline.

---

## Right to left

For Arabic and Hebrew, the whole layout mirrors, not only the text:

- Set text direction to RTL at the container level
- Reading order flows right to left, so the eye enters top right
- Entrance animations come from the right
- Timelines, funnels and process flows run right to left
- Charts keep their axes conventional, but legends and labels mirror
- Numbers and Latin brand names stay left to right inside RTL text

Mirroring the text but leaving the layout untouched is worse than not mirroring
at all. It reads as a translation someone pasted in.

---

## Mixed language decks

Common and legitimate. An English deck presenting Spanish campaign copy, a
Japanese deck quoting an English research paper.

The rule: **material stays in its original language.** Do not translate:

- Direct quotes
- Advertising and campaign copy
- Product names and brand terms
- Anything the audience will encounter in the real world

Put the translation in smaller type underneath, or in the speaker notes. Both the
original and the meaning survive that way.

Translating campaign copy into the deck language destroys the thing you are
showing. The audience needs to judge the actual words.

---

## Length shifts

Text expands and contracts when translated. Budget for it before the layout is fixed.

| Language | Against English |
|---|---|
| German | 20 to 35% longer |
| Spanish, French, Portuguese | 15 to 25% longer |
| Russian | 10 to 20% longer |
| Arabic | Similar count, wider glyphs |
| Chinese, Japanese, Korean | 30 to 50% shorter |

Design the layout against the longest language it will hold. A headline box sized
to English will overflow in German, and shrinking the type to compensate is not
a fix.

---

## PowerPoint output

Non-Latin fonts are the weak point. If the viewer lacks the font, PowerPoint
substitutes, and non-Latin substitution is far uglier than Latin.

Safest widely installed choices when the deck must open anywhere:

| Script | Windows | macOS |
|---|---|---|
| Chinese (Simplified) | Microsoft YaHei | PingFang SC |
| Chinese (Traditional) | Microsoft JhengHei | PingFang TC |
| Japanese | Yu Gothic | Hiragino Sans |
| Korean | Malgun Gothic | Apple SD Gothic Neo |
| Arabic | Segoe UI, Arial | Geeza Pro |

Tell the user which font the deck uses and that installing it keeps the design
intact. Better to say it once at delivery than to have them open a broken deck
in front of a client.
