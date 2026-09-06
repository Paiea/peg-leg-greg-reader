# PEG-LEG GREG — STABLE CHAPTER IDENTITY MODEL

Purpose: decouple a chapter's durable identity from its current display number so structural editing can merge, cut, reorder, and renumber without breaking art, metadata, reader links, or historical references.

## Core rule

**Chapter number is presentation order, not identity.**

A chapter should eventually have a permanent internal `chapter_id` that does not change when the published chapter number changes.

Example conceptual model:

- stable id: `plg-origin-0187`
- current display number: `172`
- current title: `THE ...`
- book/act placement: mutable presentation metadata
- illustration links: attach to stable id, not display number

The exact machine format may evolve, but the identity principle is durable.

## Why this matters

Structural compression can otherwise create cascading breakage across:
- manuscript file names;
- chapter index entries;
- public reader navigation;
- act/book listings;
- illustration manifests;
- image coverage reports;
- generated prompt packets;
- approved-art references;
- historical editorial notes;
- old public links and bookmarks.

A chapter surviving under a different display number should remain the same durable chapter object.

## Identity semantics

A stable chapter id should represent the durable prose lineage, not the current number.

Rules:
- KEEP/TIGHTEN: retain original stable id.
- MERGE: choose one surviving primary stable id and record absorbed source ids in migration metadata.
- SUMMARIZE-IN-SCENE: surviving destination chapter retains its id; compressed source id is recorded as absorbed/retired.
- CUT: source id becomes retired, not silently erased from migration history.
- SPLIT, if ever explicitly authorized: original id remains on the primary descendant and new descendant receives a new stable id with ancestry recorded.

Do not reuse retired ids for unrelated chapters.

## Display numbering

Current chapter numbers may change only during a dedicated publication finalization step after the structural map and prose are frozen.

During compression work, preserve source chapter numbers or map labels long enough to audit changes safely.

The final number sequence is derived from surviving chapter order.

## Migration ledger

Every structural batch that changes chapter boundaries should preserve an old-to-new ledger containing at least:
- source chapter number;
- source stable id;
- action: KEEP/TIGHTEN/MERGE/SUMMARIZE/CUT;
- destination stable id, if absorbed;
- final display number after publication rebuild;
- illustration disposition;
- redirect/alias disposition when public links exist.

This ledger is audit history. Do not delete it merely because renumbering succeeds.

## Adoption strategy

Do not mass-convert every existing file immediately just to satisfy this rule.

Adopt stable identity in stages:
1. build identity registry from current authoritative chapter index;
2. preserve current chapter numbers as original/source numbers;
3. teach compression maps to reference both source number and stable id;
4. teach illustration/publication tooling to resolve stable id -> current number;
5. only then allow broad renumbering.

## Backward compatibility

Existing number-based assets and metadata remain valid historical inputs during migration.

Do not rename thousands of files prematurely.

Instead build a resolver layer that can map:
- old chapter number -> stable id;
- stable id -> current chapter number;
- stable id -> current art assets;
- old public chapter path -> current chapter path or redirect.

## Editorial rule

Illustration cost, existing URLs, or historical chapter numbering are migration constraints, not reasons to preserve weak manuscript structure.

Likewise, structural compression is not permission to break published infrastructure.

The system must support both truths:

**edit the book honestly**

and

**migrate the surrounding project deliberately.**