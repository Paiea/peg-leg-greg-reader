# SHOWCASE CANON

## Purpose

Peg-Leg Greg preserves a complete canonical chronology while publishing a shorter reader-facing sequence.

**Full Canon** is the story.

**Showcase** is the selected telling of that story.

A chapter hidden from Showcase remains fully canonical. Its events still happened. Characters remember them. Money, objects, relationships, injuries, obligations, knowledge, and world state continue through them.

## Authority

Story and continuity workers use Full Canon.

Reader and publishing workers use `publishing/showcase_chapters.json` to determine which whole canonical chapters appear in the public sequence.

The showcase manifest never outranks manuscript prose for story truth.

## Current terminal frontier

- Original Peg-Leg Greg / Run 1 Full Canon ends at **Chapter 503 - THE AMATEUR** unless explicit author authority reopens the manuscript.
- Chapters 501-503 have no hide overrides and therefore inherit the manifest default of **visible**.
- With the current visibility map, canonical Chapter 500 is Showcase Chapter 389, so canonical Chapters 501-503 publish as Showcase Chapters **390-392**.
- Chapter 503 is the terminal public Showcase chapter unless the manuscript is explicitly reopened or a later curation decision changes whole-chapter visibility.

## Non-negotiable rules

- Whole chapters only.
- Never hide a scene, paragraph, or prose range through this system.
- Never delete manuscript prose because a chapter is hidden from Showcase.
- Never renumber canonical chapter files, manuscript references, art registry entries, or continuity records to match Showcase numbers.
- Artwork remains keyed to canonical chapter identity.
- Missing canonical authority is not the same thing as an intentionally hidden chapter. Navigation may skip explicitly hidden canonical chapters, but it must not bridge a genuinely missing canonical chapter.

## Publishing behavior

Visible canonical chapters receive contiguous Showcase numbers in canonical order.

Example:

- Canon 1 -> Showcase 1
- Canon 2 -> Showcase 2
- Canon 3 -> hidden
- Canon 4 -> Showcase 3

Public labels use Showcase numbers. File paths continue to use canonical IDs, so Showcase Chapter 3 may live at `chapters/004.html`.

Homepage contents, Text Reader contents, Illustrated Reader navigation, Book/Act range labels, latest-chapter presentation, and Begin Reading should follow Showcase ordering.

## Manifest

Manual authority: `publishing/showcase_chapters.json`

Initial policy:

- `default: visible`
- sparse overrides only
- no hidden chapters at system launch

Allowed hide reasons:

- `redundant_progression`
- `duplicate_information`
- `low_consequence_mundane`
- `bridge_not_needed`
- `superseded_by_stronger_chapter`
- `pacing`
- `other`

The hidden percentage is an observed editorial result, not a quota. A 35-45% reduction may be evaluated, but no worker should hide material merely to hit a target percentage.

## Validation

Run:

`python scripts/project_check.py showcase`

The validator checks manifest shape, whole-chapter-only constraints, canonical chapter references, and contiguous Showcase numbering.

Reader tests additionally verify hidden-chapter navigation and display numbering.

## Curation workflow

For a bounded audit batch:

1. Read the exact canonical chapters plus enough neighboring prose to judge continuity.
2. Decide KEEP or HIDE at whole-chapter granularity.
3. Record only HIDE overrides unless a visible override is genuinely needed.
4. Keep reasons compact.
5. Run Showcase validation and reader tests.
6. Do not edit manuscript prose as part of the curation decision.

Later prose polishing should concentrate on the chapters that survive Showcase curation, while Full Canon remains available for continuity and future development.