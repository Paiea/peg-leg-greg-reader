# PEG-LEG GREG — READER DESIGN LAB

A durable workshop for reader/UI/graphics ideas that are worth preserving but are not yet project law.

This file may contain experiments and rejected ideas. Successful durable principles should graduate into production instructions or the visual bible.

## Established design direction

Preserve a single persistent mobile-friendly reader URL and the hierarchy:

**authoritative manuscript -> illustrated reader build -> publishing output -> GitHub Pages**

Hosting/presentation work must not create a competing prose branch.

## Reader personality

Prefer:

CLEAN -> READABLE -> WARM -> BOOK-LIKE -> SLIGHTLY HANDMADE / STORYBOOK

Avoid:

FLASHY -> APP-LIKE -> ANIMATION-HEAVY -> DASHBOARD CHROME

## Mixed-fidelity image rhythm

Promoted idea worth preserving:

Use illustrations as pacing weights rather than treating every image equally.

- **sketch beat** — small observation/pause
- **scene illustration** — substantial scene image
- **feature illustration** — occasional larger visual event

Do not force full bleed across mixed-resolution art.

## Homepage / index ideas

Useful experiments:
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
- intentional paragraph breathing room through CSS only, never prose rewriting
- obvious but quiet previous / next / contents navigation
- mobile nav that does not require precision tapping
- image spacing based on role
- captions quiet and optional-feeling
- accessible focus states

## CSS debt finding

`assets/reader.css` has accumulated multiple historical presentation passes and repeated mobile/image overrides.

Before adding another major visual layer:

**CONSOLIDATE -> PRESERVE GOOD BEHAVIOR -> POLISH**

Do not merely append another giant override block.

## Graphics / illustration integration ideas

- Let art provide texture and personality instead of adding decorative UI elements.
- Keep small raster art near intrinsic size.
- Let stronger feature art breathe when resolution supports it.
- Use movement and camera variety so scrolling through chapters does not feel visually repetitive.
- Consider chapter-opening feature art selectively rather than universally.
- Preserve whitespace around strong images rather than filling every gap.

## Act / section grouping

Possible, not mandatory.

Use collapsible or lightweight Act grouping only when story structure genuinely supports it. Do not invent Acts merely to organize a long table of contents.

## Development experiments

Future workers may test on branches:
- CSS consolidation
- typography/measure adjustments
- chapter-nav variations
- index grouping
- image-role sizing
- subtle section/act treatment
- improved gallery hierarchy
- chapter coverage indicators for production surfaces only, not necessarily public reader

## Rejected / avoid

- universal full bleed
- stretching low-resolution art
- elaborate app framework for a static novel reader
- animation for its own sake
- UI redesign that competes with manuscript
- deleting old art before replacement coverage exists
- presentation edits that silently alter prose

## Promotion rule

When an experiment clearly works:
1. implement/validate it on a branch
2. record the durable principle in the appropriate production/visual file
3. prune obsolete speculation here

The lab should remain useful, not become a graveyard of every thought anyone ever had.