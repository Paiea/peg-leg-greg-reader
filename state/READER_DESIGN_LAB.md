# PEG-LEG GREG — READER DESIGN LAB

Durable workshop for reader/UI/graphics ideas worth preserving but not yet project law.

## Established direction

Preserve a single persistent mobile-friendly project URL and the hierarchy:

**authoritative manuscript -> reader surfaces -> publishing output -> GitHub Pages**

Hosting/presentation work must not create a competing prose branch.

Two reader surfaces are now intentional:

- **LIGHT = CURRENT** — fast text-first reading, no chapter illustrations, driven from exact GitHub prose sources.
- **ILLUSTRATED = BEAUTIFUL** — book-like illustrated edition that may lag while exact prose is synchronized and art coverage catches up.

The Light Reader does not replace the illustrated edition. It removes art/layout production from the critical path for making exact manuscript prose readable online.

Current source behavior:
- exact published Chapters 1–155 are rendered text-only from their existing chapter pages, with figures removed in the browser
- Chapters 220+ are discovered/rendered directly from `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`
- Chapters 156–219 remain unavailable until exact-text synchronization; never reconstruct them from summaries
- as new chapters are appended to the permanent running manuscript, the Light Reader should discover them without requiring one new static HTML page per chapter

Prefer:

CLEAN -> READABLE -> WARM -> BOOK-LIKE -> SLIGHTLY HANDMADE / STORYBOOK

Avoid:

FLASHY -> APP-LIKE -> ANIMATION-HEAVY -> DASHBOARD CHROME

## Mixed-fidelity image rhythm

Use illustrations as pacing weights rather than treating every image equally:
- **sketch beat** — small observation/pause
- **scene illustration** — substantial scene image
- **feature illustration** — occasional larger visual event

Do not force full bleed across mixed-resolution art.

## Homepage / index ideas

Useful experiments:
- make Illustrated / Light reading modes legible without turning the homepage into an app dashboard
- clearer book-first identity
- easy start / continue reading
- cleaner chapter scanning
- gallery available but secondary to reading
- lightweight Act grouping only where real story transitions support it
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

## Graphics / illustration integration

- Let art provide texture and personality instead of decorative UI clutter.
- Keep small raster art near intrinsic size.
- Let stronger feature art breathe when resolution supports it.
- Use movement and camera variety so long scrolling does not feel visually repetitive.
- Consider chapter-opening feature art selectively rather than universally.
- Preserve whitespace around strong images rather than filling every gap.

## Act / section grouping

Possible, not mandatory. Use only when story structure genuinely supports it. Do not invent Acts merely to organize a long table of contents.

## Future branch experiments

- recover/synchronize exact Chapters 156–219 so Light becomes continuous
- add a restrained Light Reader entry point to the main homepage when safe to edit the large generated index
- CSS consolidation
- typography/measure adjustments
- chapter-nav variations
- index grouping
- image-role sizing
- subtle section/act treatment
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