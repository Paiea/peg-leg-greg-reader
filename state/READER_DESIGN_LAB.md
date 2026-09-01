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
- show the CURRENT manuscript group first so the live endpoint cannot be mistaken for the illustrated edge
- show Chapters 156–219 immediately below Current
- place the shared story Acts for Chapters 1–155 below those current/recovered groups
- keep a direct newest/current reading shortcut near the top
- preserve compatibility routing for ranges that have not yet been statically backfilled

Prefer:

CLEAN -> READABLE -> WARM -> BOOK-LIKE -> SLIGHTLY HANDMADE / STORYBOOK

Avoid:

FLASHY -> APP-LIKE -> ANIMATION-HEAVY -> DASHBOARD CHROME

## Shared story Acts

The Illustrated and Light contents surfaces share one content-based Act map for Chapters 1–155. These are story transitions, not equal numeric buckets:

1. **ACT I — THE SECOND LIFE** — Chapters 1–20
2. **ACT II — MAKING A PLACE** — Chapters 21–63
3. **ACT III — THE NEW BASELINE** — Chapters 64–82
4. **ACT IV — A LIFE IN CARROW** — Chapters 83–137
5. **ACT V — THE COMPANY ROAD** — Chapters 138–155

The Act definition belongs in shared reader tooling so Illustrated and Light cannot silently drift into different boundaries or labels.

Presentation rule:
- use quiet expandable book-like sections, not dashboard cards
- Illustrated may open Act I initially while later Acts remain collapsed
- Light keeps Current and recovered prose above the Acts
- desktop chapter lists may use two columns; mobile should collapse to one
- do not invent later Acts merely to organize chapter counts; future Act boundaries must be justified by story movement

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
- use the shared story Acts for cleaner chapter scanning
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

Shared Act styling and desktop image caps should remain a deterministic managed presentation block rather than becoming another uncontrolled chain of overrides.

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

## Avoid

- universal full bleed
- stretching low-resolution art
- elaborate app framework for a static novel reader
- animation for its own sake
- UI redesign that competes with manuscript
- deleting old art before replacement coverage exists
- presentation edits that silently alter prose

## Promotion rule

When an experiment clearly works: implement/validate it on a branch, record the durable principle in the appropriate production/visual file, then prune obsolete speculation here.
