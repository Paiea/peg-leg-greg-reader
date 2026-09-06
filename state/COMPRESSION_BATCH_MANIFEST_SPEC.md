# PEG-LEG GREG — COMPRESSION BATCH MANIFEST SPEC

Purpose: define the durable record for each approved structural-compression batch so edits remain auditable and reversible.

## One manifest per executed batch

A structural batch should produce a durable manifest before final publication migration.

Recommended filename shape:

`publishing/compression_batches/batch_0150_0172.json`

Exact path can change when tooling is implemented, but every executed batch needs one authoritative manifest.

## Required fields

Each manifest should record:
- batch identifier;
- source branch/commit;
- target range at time of audit;
- compression strength;
- author approval timestamp or approval note;
- source chapter IDs;
- classifications for every source chapter;
- approved merge groups;
- approved cuts;
- surviving chapter IDs;
- relocated beats;
- dependency notes;
- illustration migration requirements;
- legacy-number implications;
- resulting ordered chapter IDs;
- validation status;
- execution commit(s).

## Classification records

For each source chapter, store:
- `chapter_id`
- source display number/title;
- `classification`;
- `primary_function`;
- `unique_value`;
- `redundant_functions`;
- `dependencies`;
- `destination_id` when merged/cut;
- risk/confidence;
- author overrides.

## Merge groups

A merge group must explicitly name:
- all source IDs;
- survivor/new destination ID;
- which concrete beats survive;
- which facts must remain for later continuity;
- which source titles/numbers become aliases only;
- affected art asset IDs.

## Cut records

CUT requires a record of what happened to every meaningful residue:
- relocated;
- already duplicated elsewhere;
- intentionally removed;
- archived only.

A chapter must not disappear merely because its status became CUT.

## Approval freeze

Once the author approves a structural map, freeze a manifest version before prose execution.

If execution discovers a dependency requiring structural change:
- revise manifest;
- increment revision;
- record reason;
- reapprove the affected local structure before continuing.

Do not silently drift from the approved map.

## Reversibility

The manifest should make it possible to answer:
- what did Chapter 211 become?;
- where did its important scene go?;
- why was it merged?;
- what happened to its art?;
- what public links once pointed there?;
- which commit contains the pre-compression authority?

The goal is not effortless automatic rollback of prose. The goal is a reliable audit trail that prevents archaeology later.

## Relationship to numbering

Compression manifests use stable chapter IDs as primary identity.

Display numbers are recorded as historical context only.

Final numbering is generated after structural regions freeze.

## Success rule

No structural batch should leave the project asking, six weeks later:

`Wait, what the fuck happened to old Chapter 238?`

The manifest should answer it immediately.
