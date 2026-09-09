# Greg, Again — First-Pass Sprint Archive, Chapters 27–34

Status: **HISTORICAL EXPERIMENTAL EVIDENCE / READ-ONLY REFERENCE**

Archived: 2026-09-09

Purpose: preserve the completed first-pass Chapters 27–34 campaign exactly before a bounded second full REHEARSAL campaign reopens story possibility.

## Provenance

- source branch: `experiment/plg-r2-opening`
- first-pass campaign boundary commit: `c7d3d1c6261341ae1b2bcf3a99855923f46f787d` (`story: add compact frontier through Chapter 34`)
- Chapter 35 search begins only afterward at `4f02db773be06651e085f7f533eea65ae66f9df7`
- copied chapter, rehearsal, and evaluation files retain their original Git blob identities; they are not rewritten snapshots

## Archived surfaces

- `prose/027-*.md` through `prose/034-*.md`
- `rehearsals/027-story-search.md` through `rehearsals/034-story-search.md`
- `rehearsals/034-story-eval.md`
- durable evaluation files that actually exist under `evals/` for Chapters 27–33
- `written/CURRENT_FRONTIER.md` as the compact first-pass campaign state snapshot

## Known first-pass state-path drift

The archived `CURRENT_FRONTIER.md` refers Chapters 27–33 to `rehearsals/*-story-eval.md`. Those paths were not durable files at the campaign boundary. The corresponding actual durable evaluations are the archived `evals/027-student-eval.md` through `evals/033-share-eval.md`. Chapter 34's durable evaluation is `rehearsals/034-story-eval.md`.

This note records the mismatch. It does not repair or rewrite the historical snapshot.

## Archive rule

Do not edit these archived copies when integrating second-pass discoveries. Current prose and current REHEARSAL state may evolve elsewhere; this directory exists so the first pass remains directly recoverable and comparable.
