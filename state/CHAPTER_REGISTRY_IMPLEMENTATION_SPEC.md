# PEG-LEG GREG — CHAPTER REGISTRY IMPLEMENTATION SPEC

Purpose: define the practical data model that lets manuscript structure change without treating display chapter numbers as permanent identity.

## Stable identity rule

Every chapter receives one immutable `chapter_id`.

Example shape:

`plg-ch-0187`

The exact naming scheme may be replaced before tooling is implemented, but once assigned in production, a `chapter_id` must never be recycled for another chapter.

## Registry responsibilities

The registry must be able to answer:
- what durable chapter entity is this?;
- what is its current display number?;
- what is its current title?;
- what book/act currently contains it?;
- what source chapter(s) contributed to it after compression?;
- what previous public aliases point to it?;
- what illustrations/assets belong to it?;
- whether it is active, merged, cut, archived, or redirected.

## Minimum record shape

Each chapter record should support:

- `chapter_id`
- `display_number`
- `title`
- `book_id`
- `act_id`
- `status`
- `source_chapter_ids`
- `legacy_numbers`
- `legacy_slugs`
- `current_slug`
- `manuscript_path`
- `illustration_asset_ids`
- `notes`

## Status values

Recommended values:
- `active`
- `merged`
- `cut`
- `archived`
- `redirect`

A merged source chapter remains historically addressable in the registry even if it no longer renders as an independent public chapter.

## Merge behavior

If Chapters A and B become one surviving chapter:
- surviving entity may keep A's stable ID or receive a new explicitly approved merged ID;
- the other source ID remains in history;
- `source_chapter_ids` records both;
- legacy links for both must resolve to the surviving public destination;
- art attached to both is reconciled explicitly.

Default preference: preserve one existing stable ID when one source chapter is clearly the structural survivor. Create a new merged ID only when the resulting unit is materially a new composite and the migration cost is justified.

## Cut behavior

A cut chapter is not erased from registry history.

It becomes `cut` or `redirect` and records:
- where any surviving beats moved;
- where legacy URLs should resolve;
- where illustrations moved or were archived;
- why the chapter ceased to exist independently.

## Display numbering

Display numbers are generated from the current ordered list of active chapters.

Do not use display number as foreign-key identity for:
- art;
- chapter metadata;
- reader navigation;
- internal dependencies;
- compression maps;
- redirects.

## Transitional adoption

Do not force a one-shot migration of every current file before the registry tooling exists.

Recommended transition:
1. assign stable IDs to current canonical chapters;
2. create registry mapping without changing public numbering;
3. teach art/reader tooling to resolve through stable IDs;
4. run validation while output remains identical;
5. only then permit structural renumber migrations.

## Validation requirements

A registry build must reject:
- duplicate stable IDs;
- two active chapters with same display number;
- active chapters missing manuscript paths;
- unknown source IDs;
- redirect cycles;
- art bindings to nonexistent chapter IDs;
- broken current slugs;
- active chapters missing title/book placement.

## Design principle

The chapter is the durable object.

The number is where that object currently appears in the reading order.
