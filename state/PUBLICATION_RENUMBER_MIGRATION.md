# PEG-LEG GREG — PUBLICATION RENUMBER MIGRATION

Purpose: make structural compression compatible with the public reader, act/book structure, chapter URLs, image manifests, and historical metadata.

## Core rule

**Do not renumber while deciding structure. Renumber only after a structural batch is accepted and frozen.**

Structural editing and publication migration are separate operations.

## Migration order

For a batch that changes chapter count or order:

1. freeze the accepted structural map;
2. freeze surviving prose and chapter lineage;
3. build old-number -> stable-id -> new-number mapping;
4. reconcile illustration associations;
5. update chapter index and act/book placement;
6. update reader navigation and generated manifests;
7. create redirects/aliases for old public chapter paths where feasible;
8. validate previous/next links and no-gap sequence;
9. update exports/coverage reports derived from chapter numbering;
10. retain migration ledger for audit.

## Do not eagerly rename assets

Existing assets may contain chapter numbers in:
- filenames;
- directories;
- JSON records;
- prompt packets;
- coverage reports;
- image manifests.

Do not mass-rename them simply because display numbering changed.

Prefer stable-id resolver metadata so historical filenames can remain intact while current presentation maps correctly.

## Public URL policy

Where the reader currently exposes number-derived chapter URLs, preserve old links through aliases or redirects whenever practical.

Old links should not silently land on a different chapter after renumbering.

At minimum, migration QA must detect this failure mode.

## Book and act structure

Compression may alter chapter counts without automatically changing the governing act movement.

After a structural batch:
- reassess act boundaries by story movement, not old chapter arithmetic;
- do not preserve an act break solely because it used to fall after Chapter N;
- do not move an act break casually if the story transition still lands correctly;
- update presentation metadata only after the structural range is accepted.

## Reader/navigation validation

After renumber migration verify:
- first/last chapter of each book/act is correct;
- previous/next navigation points to surviving adjacent chapters;
- no removed chapter remains in primary navigation;
- no surviving chapter is skipped;
- titles remain attached to correct prose;
- illustration associations resolve to the intended surviving scenes;
- `latest` or endpoint links point to current authority;
- chapter counts shown in UI agree with generated sequence.

## Illustration migration

Follow `state/ILLUSTRATION_REASSIGNMENT_RULES.md`.

A chapter-number shift must not automatically rename, duplicate, or delete its image files.

Publication manifest should become the translation layer between historical asset identity and current chapter display order.

## Structural branch rule

Large compression/renumber work belongs on a durable editing branch until:
- structural QA passes;
- publication migration QA passes;
- image associations are reconciled;
- reader sequence is validated.

Do not make `main` temporarily contain a half-renumbered book.

## Rollback requirement

Every renumber batch should retain enough mapping to restore or inspect:
- old chapter number;
- stable chapter id;
- new chapter number;
- old title;
- new/surviving title;
- merge/cut ancestry;
- old and new image placement.

## Final principle

A cleaner manuscript should not require destroying the history of the published project.

**Structure may change. Identity must remain traceable.**