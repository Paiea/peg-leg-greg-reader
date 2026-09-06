# PEG-LEG GREG — CHAPTER IDENTITY REGISTRY SPEC

Purpose: define a stable chapter identity model so structural edits can change presentation order without breaking illustrations, metadata, links, or historical auditability.

## Core rule

A chapter's permanent identity is NOT its current chapter number.

Chapter number is presentation order.

Every chapter should eventually have a stable immutable `chapter_id` that survives:
- renumbering;
- act changes;
- book-boundary changes;
- chapter-title changes;
- merged sequencing;
- illustration reassignment;
- publication rebuilds.

## Recommended identity shape

Use a compact immutable identifier such as:

`plg-ch-000187`

The exact initial assignment may derive from historical chapter origin for migration convenience, but once assigned the ID never changes even if presentation number changes.

Do not recycle IDs from deleted/merged chapters.

## Registry fields

A durable registry entry should support:

- `chapter_id`
- `origin_chapter_number`
- `current_display_number`
- `current_title`
- `book`
- `act`
- `status`: active / merged / retired / archived
- `merged_into`: stable chapter_id or null
- `source_path`
- `public_slug`
- `legacy_slugs`
- `illustration_refs`
- `notes`

## Merge behavior

When Chapter A and Chapter B merge:
- choose one surviving chapter_id for the canonical resulting chapter;
- mark the other identity as `merged` rather than deleting its existence from history;
- record `merged_into`;
- migrate surviving art/callback metadata according to illustration rules;
- preserve legacy URL aliases where feasible.

Do not create identity churn by assigning a new ID every time prose is rewritten.

## Cut behavior

When a chapter is cut:
- keep its chapter_id in the registry;
- mark status `retired`;
- preserve historical title/origin number;
- record whether any art, callbacks, or assets were reassigned;
- do not include retired IDs in current sequential numbering.

## Title behavior

Titles are mutable presentation metadata attached to stable identity.

If structural merging changes the role represented by a title, the resulting chapter may receive a new title without losing identity continuity.

## Illustration behavior

Illustration manifests should migrate toward `chapter_id` association rather than relying only on chapter number.

During transition, support both:
- stable `chapter_id` as authoritative association;
- current chapter number as generated/display metadata.

## Safety rules

Do not mass-assign or rewrite all existing assets until a migration tool/process is explicitly approved.

Do not infer stable IDs from display number after renumbering has begun.

Do not let historical IDs become reader-visible clutter unless useful for debugging/admin surfaces.

## Success condition

After this system is implemented, deleting or merging three chapters near Chapter 180 should not require manually renaming every downstream illustration and metadata record simply because display numbers shifted.
