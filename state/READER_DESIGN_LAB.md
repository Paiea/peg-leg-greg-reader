# PEG-LEG GREG — READER DESIGN LAB

Durable workshop and established direction for reader/UI/graphics work.

## Established reader model

Preserve one persistent project URL and the hierarchy:

**authoritative manuscript -> generated reader surfaces -> publishing output -> GitHub Pages**

Reader work must never create a competing prose authority.

Two intentional reading modes remain:

- **ILLUSTRATED** — book-like normal reader with chapter art when accepted art exists. A chapter may still publish here before art exists.
- **LIGHT** — fast text-first reader with no chapter illustrations.

Both are publishing derivatives. Exact manuscript authority outranks both.

Preferred presentation:

**CLEAN -> READABLE -> WARM -> BOOK-LIKE -> SLIGHTLY HANDMADE / STORYBOOK**

Avoid:

**FLASHY -> APP-LIKE -> ANIMATION-HEAVY -> DASHBOARD CHROME**

## Source authority

Reader generation follows the established exact-source split:

- existing illustrated Chapters 1–155 provide exact published prose for old-range Light extraction
- Chapters 156–219: `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`
- Chapters 220+: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`

Generated pages do not outrank those sources.

The Illustrated expansion generator deliberately supports a bounded range. Current approved static Illustrated expansion is Chapters **156–235**. It must not silently follow newer manuscript chapters beyond that bound unless the range is explicitly advanced.

Light `current` remains independent and follows whatever exact Chapter 220+ prose exists in the running manuscript.

This means the two modes can coexist safely when forward prose advances faster than Illustrated production.

## Book -> Act contents hierarchy

The reader now organizes chapters by **Book first, then content-based Acts**.

Act boundaries follow changes in Greg's lived state and story machinery rather than equal chapter counts.

The same logical Book/Act map is shared by Illustrated and Light so the two modes do not drift.

### BOOK I — Chapters 1–82

Book 1 is closed.

1. **ACT I — THE SECOND LIFE** — Chapters 1–20
   - the impossible morning becomes an actual second life
2. **ACT II — MAKING A PLACE** — Chapters 21–63
   - Carrow becomes work, people, obligations, and somewhere Greg can stand
3. **ACT III — THE NEW BASELINE** — Chapters 64–82
   - injury, changed body, recovery, and the terms of life becoming ordinary enough to live inside

### BOOK II — Chapter 83 onward

Book 2 remains active, so its final displayed range is dynamic.

1. **ACT I — A LIFE IN CARROW** — Chapters 83–111
   - recovery gives way to dating, errands, work, magic questions, and ordinary shared life
2. **ACT II — THE STAGE DOOR** — Chapters 112–137
   - theatre stops being peripheral and becomes a working social machine Greg begins entering
3. **ACT III — THE COMPANY ROAD** — Chapters 138–180
   - company work leaves familiar rooms; travel, performance, and accumulating roles become real work
4. **ACT IV — THE WORKING COMPANY** — Chapters 181–217
   - calling, backstage labor, performance, customers, debt work, and city routines deepen into a lived workplace network
5. **ACT V — THE PRICE OF ATTENTION** — Chapter 218 onward
   - ordinary life keeps accumulating while money, access, reputation, and outside attention begin carrying sharper consequences

Do not create a new Act because a chapter count becomes aesthetically inconvenient. Add or move an Act boundary only when later story progression establishes a genuinely new state.

## Contents presentation

- Book sections should read like divisions in a novel, not dashboard cards.
- Acts remain quiet expandable sections.
- Desktop chapter lists may use two columns; mobile collapses to one.
- Illustrated may open the first Act initially.
- Light uses the same Book/Act hierarchy without decorative imagery.
- Current endpoints are derived from available exact prose, not hard-coded reader claims.

## Book plates

The Illustrated contents page supports **one small high-resolution portrait bookplate per Book**.

Expected paths:

- `visual/homepage/Book01_Plate.jpg`
- `visual/homepage/Book02_Plate.jpg`

These are visual dividers, not hero banners.

Rules:

- one image per Book, not one per Act
- portrait orientation, preferably about 4:5 or 3:4
- source art should be high resolution even though display size stays small
- desktop display is approximately 260–340px wide and capped around 320px in the current implementation
- desktop places the plate beside the Book label/title/deck instead of spanning the page
- mobile stacks the plate above the Book heading at roughly 70–85% of the available content width with a sensible cap
- no text baked into generated art; Book labels and titles remain real HTML
- use a restrained border, small radius, soft shadow, and generous whitespace rather than glossy card chrome
- the image should summarize the Book's lived visual identity rather than depict one spoiler-heavy exact scene
- Book I should feel like finding a life: arrival, work, Carrow, roads, changed body, new baseline
- Book II should feel like living inside one: theatre, company work, roads, clothing, people, routines, and growing outside attention
- Greg need not dominate the frame; environment and movement matter
- if an asset is temporarily absent, the `<figure>` fails soft and disappears rather than showing broken-image UI
- Book I may load eagerly; lower-page Book plates should lazy-load
- explicit image dimensions / aspect ratio should prevent layout jump
- Light intentionally omits Book plates to preserve text-first speed and simplicity

The target feeling is **a nicely illustrated physical novel translated to the web**, not a promotional fantasy-franchise site.

Do not add full illustrations to every Act. Tiny Act vignettes or icons may be explored later, but typography alone is currently preferred to decorative clutter.

## Static Illustrated Chapters 156–235

`scripts/generate_illustrated.py` generates bounded exact-prose normal-reader derivatives.

Current approved range:

**156–235**

Behavior:

- 156–219 comes from recovered exact authority
- 220–235 comes from the permanent running manuscript
- Chapter 232's combined heading form is supported through shared parsing
- Chapter 155 links directly into 156
- 219 <-> 220 is a normal direct seam
- Chapter 235 has no forward Illustrated link until a later Illustrated range is explicitly approved
- each new Illustrated page links to its matching Light page
- pages may exist with zero art
- no manuscript prose is rewritten as part of generation

### Promoted-art preservation rule

Illustrated pages are derivatives, but accepted art can be layered onto them over time.

Regeneration therefore preserves existing promoted `<figure>` blocks by anchoring them to the following exact prose paragraph.

If a later prose edit invalidates an art anchor, generation must fail visibly so the art can be deliberately repositioned. It must never silently discard accepted art or guess a new paragraph location.

This keeps the useful long-term model:

**exact prose -> generated normal page -> selectively promoted art -> future exact regeneration without losing accepted figures**

## Mixed-fidelity image rhythm

Use illustrations as pacing weights rather than treating every image equally:

- **sketch beat** — small observation/pause
- **scene illustration** — substantial scene image
- **feature illustration** — occasional larger visual event

Do not force full bleed across mixed-resolution art.

### Desktop intrinsic-size rule

Desktop presentation must not enlarge weak/small raster art merely because the viewport is wide.

- default/scene art stays near intrinsic width with a moderate maximum
- sketch beats stay smaller
- feature illustrations may breathe larger only when the source supports it
- portrait features remain narrower
- use `width:auto` plus role-based `max-width` caps on desktop
- preserve responsive phone behavior

The goal is intentional page rhythm, not pixelated wall-sized images.

## Homepage / index direction

- make Illustrated / Light legible without turning the homepage into an app dashboard
- preserve clear book-first identity
- easy start / continue reading
- Book -> Act hierarchy for scanning a long serial
- gallery remains available but secondary to reading
- use the two Book plates sparingly
- avoid making the index feel like an admin interface

## Chapter-page direction

Useful principles:

- restrained chapter-title hierarchy
- comfortable reading measure
- breathing room through CSS only, never prose rewriting
- obvious but quiet previous / next / contents navigation
- mobile nav with generous touch targets
- image spacing based on role
- quiet caption treatment
- accessible focus states

## CSS debt finding

`assets/reader.css` contains multiple historical presentation passes and repeated mobile/image overrides.

Before another major visual layer:

**CONSOLIDATE -> PRESERVE GOOD BEHAVIOR -> POLISH**

Shared Book/Act styling, Book-plate styling, and desktop image caps should remain in the deterministic managed presentation block rather than becoming another uncontrolled override chain.

## Avoid

- universal full bleed
- stretching low-resolution art
- elaborate app framework for a static novel reader
- animation for its own sake
- UI redesign that competes with manuscript
- giant homepage banners or full-width cinematic Book art
- fake 3D book mockups
- generated text baked into Book art
- image backgrounds behind chapter links
- decorative images for every subdivision
- deleting old art before replacement coverage exists
- presentation edits that silently alter prose
- silently extending the bounded Illustrated range because the Manuscript Engine advanced
- fake Act breaks created only for numerical symmetry

## Promotion rule

When an experiment clearly works: implement and validate it on a branch, record the durable principle here or in the relevant visual/production file, then prune obsolete speculation.
