# PEG-LEG GREG — READER / VISUAL STATE

## Reader authority

The static reader is a derived publishing surface. It does not outrank manuscript prose.

Current mismatch at this checkpoint:

- story authority: Chapter 219
- public reader: Chapter 155

Do not fabricate reader Chapters 156–219 from summaries. Synchronize only when authoritative prose is materialized/available.

## Current presentation identity

Preserve:

- warm book-like static reader
- restrained typography
- strong chapter-title hierarchy
- mixed-fidelity illustration roles
- intrinsic-resolution image sizing
- mobile intrinsic-height behavior
- art/gallery as a secondary surface rather than the main reading experience

Avoid:

- forced full bleed for small raster art
- stretching images above sensible native size
- app-like chrome
- animation for its own sake
- giant framework migration for a static reader

## Existing illustration roles

- `sketch-beat`: small vignette / observation / quick physical beat
- `scene-illustration`: normal reader scene image
- `feature-illustration`: occasional visual peak
- `feature-portrait`: portrait-constrained feature art

## Current CSS observation

`assets/reader.css` contains several historical presentation passes layered sequentially. Later rules override earlier ones, so behavior can be correct while the stylesheet is harder than necessary to reason about.

A future cleanup should consolidate duplicate chapter-title, illustration-role, and mobile intrinsic-height rules without changing rendered behavior first. Treat that as refactoring before additional visual invention.

## Visual-production north star

Fill the illustrated reader first. Upgrade later.

Target roughly 1–3 useful illustrations per chapter, ideally three when the chapter supports it. Most art may be fast storybook coverage; stronger feature art can create peaks.

Reject/retry primarily for:

- wrong skin tone / ethnicity
- badly wrong recurring-character identity
- Greg's disability contradicted
- severe anatomy/body failure
- direct scene/equipment/location contradiction

Do not delete acceptable existing art merely to create uniformity.

## Movement composition

Assume movement unless deliberate stillness is the point.

Ask:

1. Where does the eye enter?
2. Where does motion carry it?
3. Where does the eye land?

Movement may come from posture, crutches, fabric, props, weather, crew, background work, eyelines, perspective, doors, carts, smoke, or stage action.

## Next reader sequence

1. consolidate reader CSS without changing behavior
2. materialize authoritative 156–219 prose
3. synchronize reader pages/navigation/index through the real endpoint
4. recalculate actual image coverage from chapter HTML
5. resume 5x5 coverage waves against real gaps
6. validate mobile/desktop, links, chapter ordering, and image references