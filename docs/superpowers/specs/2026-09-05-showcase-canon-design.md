# Showcase Canon Design

## Purpose

Peg-Leg Greg keeps one complete canonical chronology while publishing a curated reader-facing sequence made only from whole canonical chapters.

The showcase is a presentation layer, not a second canon. Hidden chapters remain fully canonical and continue to govern continuity, character memory, economic state, relationships, and future manuscript work.

## Core rule

Curation is whole-chapter only.

A canonical chapter is either visible in the showcase or hidden from the showcase. No scene, paragraph, prose-range, or partial-chapter hiding is supported.

## Authority

1. Full manuscript authority remains unchanged and outranks the showcase layer for story truth.
2. `publishing/showcase_chapters.json` is the only manually edited showcase-selection authority.
3. Generated showcase maps are derivatives and must never be hand-edited.
4. Reader, illustrated-reader, text-reader, and future publishing surfaces may consume showcase ordering without changing canonical chapter IDs or source files.

## Manifest

Create `publishing/showcase_chapters.json` with schema version 1.

```json
{
  "version": 1,
  "mode": "whole_chapter_only",
  "default": "visible",
  "chapters": {
    "143": {
      "showcase": false,
      "reason": "redundant_progression"
    }
  }
}
```

The manifest is sparse. Chapters omitted from `chapters` inherit `default`, which is initially `visible`. This makes adoption non-destructive and avoids a 400+ line manifest that must be updated whenever the manuscript advances.

Allowed reason codes for hidden chapters:

- `redundant_progression`
- `duplicate_information`
- `low_consequence_mundane`
- `bridge_not_needed`
- `superseded_by_stronger_chapter`
- `pacing`
- `other`

Visible overrides may exist but do not require a reason.

## Stable identity and display numbering

Canonical chapter number is permanent identity. Existing source names, chapter HTML paths, art registry references, state files, and continuity references remain keyed to canonical chapter number.

Showcase chapter number is generated from the ordered list of visible canonical chapters.

Example:

- Canon 1 -> Showcase 1
- Canon 2 -> Showcase 2
- Canon 3 -> hidden
- Canon 4 -> Showcase 3

A generated map records both directions. The reader displays showcase numbering but links to canonical file paths, e.g. showcase Chapter 3 may live at `chapters/004.html`.

## Navigation

Reader navigation follows visible canonical order, never arithmetic `chapter - 1` or `chapter + 1` when showcase mode is active.

A visible chapter links to the previous and next visible canonical chapter while labeling those links with showcase chapter numbers.

Hidden canonical chapter pages may continue to exist in repository artifacts, but they are excluded from normal showcase indexes and navigation.

## Books and Acts

Canonical Book/Act membership remains based on canonical chapter identity. The showcase does not rewrite story chronology or structural membership.

Reader-facing chapter labels and counts use showcase numbering. A Book or Act with zero visible chapters must not render. Book/Act range labels should describe the showcase-number span of the visible chapters they contain rather than exposing canonical-number gaps.

## Artwork

Artwork remains keyed to canonical chapter number. Hiding a chapter does not move, delete, retire, or reinterpret its artwork. If a chapter is later restored to showcase visibility, its existing art remains attached automatically.

## Validation

Validation must fail when:

- manifest version or mode is unsupported;
- default is not `visible` or `hidden`;
- a chapter key is not a positive integer canonical ID;
- a manifest chapter references no known canonical chapter when checked against current authority;
- `showcase` is not boolean;
- a hidden chapter has an unsupported reason code;
- scene/range/paragraph-level selection fields are present;
- generated showcase numbering is non-contiguous or non-bijective;
- a rendered Book/Act section contains no visible chapters but is emitted;
- previous/next navigation points to a hidden chapter.

## Initial state

Version 1 launches with `default: visible` and no hidden chapters. Therefore introducing the system changes no reader content until an explicit curation decision is recorded.

No archive UI, full/showcase toggle, extended-edition UI, scene hiding, duplicate manuscript copy, or automated AI curation is part of version 1.

## Editorial workflow

A curation pass reads full canonical prose and neighboring context, then classifies chapters. Editorial decisions update only the sparse showcase manifest. The manuscript remains untouched.

The hide percentage is an observed outcome, not a quota. A likely 35-45% hidden rate may be evaluated, but the system must never enforce a target percentage.

## Success criteria

- Full canon remains byte-for-byte unaffected by showcase curation.
- With an empty override set, the public sequence is behaviorally identical to current chapter order.
- Hiding one canonical chapter removes it from indexes and normal navigation without renaming files.
- Later visible chapters are renumbered sequentially for readers.
- Existing art remains attached to canonical chapter IDs.
- A worker can curate a batch by changing only `publishing/showcase_chapters.json` and running validation/build commands.
