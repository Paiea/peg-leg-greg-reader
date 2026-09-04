# PEG-LEG GREG — READER DESIGN LAB

Durable workshop for reader/UI/graphics ideas worth preserving but not yet project law.

## Established direction

Preserve a single persistent mobile-friendly project URL and the hierarchy:

**authoritative manuscript -> reader surfaces -> publishing output -> GitHub Pages**

Hosting/presentation work must not create a competing prose branch.

Two reader surfaces are intentional:

- **LIGHT = CURRENT** — fast text-first reading, no chapter illustrations, driven from exact GitHub prose sources.
- **ILLUSTRATED = BEAUTIFUL** — book-like illustrated edition that may lag while exact prose is synchronized and art coverage catches up.

The Light Reader does not replace the illustrated edition. It removes art/layout production from the critical path for making exact manuscript prose readable online.

Current source behavior:
- exact published Chapters 1–155 are available from their existing illustrated chapter pages and can be rendered as Light derivatives with figures removed
- exact Chapters 156–219 live in `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`
- Chapters 220+ are driven from `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`
- generated Light chapter pages are publishing derivatives, not prose authority
- as the permanent running manuscript advances, Current Light generation follows exact prose authority

Current Light UX rule:
- keep a direct newest/current reading shortcut near the top
- use the same Book -> Act -> Chapter hierarchy as Illustrated
- Light remains intentionally image-free at Book and chapter level
- preserve compatibility routing for ranges that have not yet been statically backfilled

Prefer:

CLEAN -> READABLE -> WARM -> BOOK-LIKE -> SLIGHTLY HANDMADE / STORYBOOK

Avoid:

FLASHY -> APP-LIKE -> ANIMATION-HEAVY -> DASHBOARD CHROME

## Shared Book / Act hierarchy

The Illustrated and Light contents surfaces share one content-based Book/Act map. These are story transitions, not equal numeric buckets.

### BOOK I — Chapters 1–82

1. **ACT I — THE SECOND LIFE** — Chapters 1–20
2. **ACT II — MAKING A PLACE** — Chapters 21–63
3. **ACT III — THE NEW BASELINE** — Chapters 64–82

### BOOK II — Chapters 83–180

1. **ACT I — A LIFE IN CARROW** — Chapters 83–99
2. **ACT II — THE STAGE DOOR** — Chapters 100–137
3. **ACT III — THE COMPANY ROAD** — Chapters 138–180

### BOOK III — Chapters 181–current

1. **ACT I — THE WORKING COMPANY** — Chapters 181–219
2. **ACT II — THE PRICE OF ATTENTION** — Chapters 220–current

Chapter 181 is the Book III boundary. Chapter 220 remains an internal Act boundary, not a Book boundary; its repository manuscript-file transition is a production detail and must not define story architecture.

The definition belongs in shared reader tooling so Illustrated and Light cannot silently drift into different boundaries or labels. `current` must resolve from actual chapter authority rather than a manually baked endpoint.

Presentation rule:
- hierarchy is **BOOK -> ACT -> CHAPTERS**
- Book label stays small and quiet
- Act title is the prominent navigational unit
- chapter range stays quiet
- Acts remain expandable
- Illustrated may open the first Act initially while later Acts remain collapsed
- desktop chapter lists may use two columns; mobile should collapse to one
- do not invent later Acts merely to organize chapter counts; future Act boundaries must be justified by story movement

## Book role cards

Illustrated gets one representative **chapter role card** per Book. Light gets none.

This replaces the earlier fake-cover / generic-frontispiece direction. The card is an illustrated artifact from inside the novel, not a product mockup and not a literal cover for the Book.

Current representatives:
- **Book I -> Chapter 05 — THE WARRIOR**
- **Book II -> Chapter 177 — THE STAGEHAND**
- **Book III -> Chapter 234 — THE MAGISTRATE**

Selection rule:
- use an actual chapter role Greg inhabits, not merely an event or environment label
- the representative should say something useful about the state of Greg's life during that Book
- the card uses **ROLE -> ILLUSTRATION -> SHORT VERBATIM CHAPTER LINE -> CHAPTER NUMBER**
- a small peg-leg emblem may echo the project identity, but it is decorative branding rather than a claim about Greg's body state in that chapter
- the surrounding HTML owns **BOOK I / II / III** and the Book chapter range; the card does not pretend to be the Book itself
- because the title, quote, and number belong to the card artifact, baked-in card typography is intentional here even though generated Book-cover titles are not

Body/canon rule:
- Greg remains recognizably a young man across all three representatives; visual progression comes from wear, grooming, work, and context rather than aging him decades
- early Greg may have beard shadow / scruff rather than a pristine clean shave
- Chapter 177 Greg can carry a short unkempt beard
- **The Stagehand card must keep the lower body and mobility aid out of frame** so the index does not accidentally spoil or contradict his body state
- when a representative changes later, verify the chapter's actual body/grooming state before art promotion

Presentation rule:
- desktop: card sits to the left of the Book's Act contents, roughly **380–420px wide**
- mobile: presentation stacks **Book heading -> centered card -> Acts**, with the card at roughly **min(85vw, 340px)**
- cards preserve the approved **3:4 portrait** proportions and should not become banners
- restrained border/radius/shadow only; no giant glossy container
- each card is clickable and opens its representative chapter
- the card should be visually substantial enough to enjoy while the Book/Act hierarchy remains clear beside or below it

Current implementation uses three individual high-resolution WebP assets, one per representative. Illustrated renders them as normal image elements. Light remains image-free. Do not recombine them into an embedded sprite.

Use the project visual language: dark divination-card framing with **SKETCH + INK + PAINT** color illustration, weathered physical texture, restrained ornament, and a recognizable small peg-leg emblem. The influence may nod toward old game divination cards without cloning a specific commercial card frame.

Act-level art remains deliberately deferred. Tiny 32–56px vignettes may be explored later, but typography alone is currently preferred over flooding the contents page with separate Act illustrations.

## Mixed-fidelity image rhythm

Use illustrations as pacing weights rather than treating every image equally:
- **sketch beat** — small observation/pause
- **scene illustration** — substantial scene image
- **feature illustration** — occasional larger visual event

Do not force full bleed across mixed-resolution art.

### Desktop intrinsic-size rule

Desktop presentation must not enlarge weak/small raster art merely because the viewport is wide.

- default/scene art should remain near intrinsic width and use a moderate maximum
- sketch beats stay smaller
- feature illustrations may breathe larger only when the source can support it
- portrait features remain narrower
- use `width:auto` plus role-based `max-width` caps on desktop rather than forcing every image to the cap width
- preserve the existing responsive phone behavior; small screens already constrain art naturally

The goal is intentional page rhythm, not pixelated wall-sized images.

## Homepage / index direction

- make Illustrated / Light reading modes legible without turning the homepage into an app dashboard
- preserve clear book-first identity
- easy start / continue reading
- use the shared Book/Act hierarchy for cleaner chapter scanning
- Illustrated contents should continue through the actual current manuscript endpoint; chapters beyond the current illustrated-page edge may route to Light rather than disappearing
- gallery remains available but secondary to reading
- avoid making the index feel like an admin interface

## Chapter-page ideas

Useful experiments:
- restrained chapter-title hierarchy
- comfortable reading measure
- intentional breathing room through CSS only, never prose rewriting
- obvious but quiet previous / next / contents navigation
- mobile nav with generous touch targets
- image spacing based on role
- quiet caption treatment
- accessible focus states

## CSS debt finding

`assets/reader.css` has accumulated multiple historical presentation passes and repeated mobile/image overrides.

Before adding another major visual layer:

**CONSOLIDATE -> PRESERVE GOOD BEHAVIOR -> POLISH**

Do not merely append another giant override block.

Shared Act styling and desktop image caps should remain deterministic managed presentation. Small self-contained components may use a focused stylesheet when that is safer than replacing the entire historical reader stylesheet for a narrow feature.

## Graphics / illustration integration

- Let art provide texture and personality instead of decorative UI clutter.
- Keep small raster art near intrinsic size.
- Let stronger feature art breathe when resolution supports it.
- Use movement and camera variety so long scrolling does not feel visually repetitive.
- Consider chapter-opening feature art selectively rather than universally.
- Preserve whitespace around strong images rather than filling every gap.

## Future branch experiments

- decide later whether recovered Chapters 156–219 should be consolidated into a different permanent manuscript path; do not rewrite or reconstruct them
- broader CSS consolidation
- typography/measure adjustments
- chapter-nav variations
- improved gallery hierarchy
- production-only coverage indicators
- tiny Act vignettes only if they materially improve recognition without adding clutter

## Avoid

- universal full bleed
- stretching low-resolution art
- elaborate app framework for a static novel reader
- animation for its own sake
- UI redesign that competes with manuscript
- deleting old art before replacement coverage exists
- presentation edits that silently alter prose
- giant Book banners, fake 3D covers, progress meters, status badges, statistics, glowing UI, streaming-service framing, or image backgrounds behind chapter links

## Promotion rule

When an experiment clearly works: implement/validate it on a branch, record the durable principle in the appropriate production/visual file, then prune obsolete speculation here.
