# R2 Role Title Authority Design

## Goal

Make R2 chapter titles consistently answer **Who is Greg in this chapter?** without coupling title wording to stable chapter identity or forcing audio regeneration.

## Problem

R2 already treats chapter ID and numeric chapter number as stable identity while title is mutable metadata. That separation is correct, but title authority is inconsistent across selected written headings, public chapter manifests, the R2 production registry, and the Greg, Again audio manifest. Some public titles already use embodied Greg roles while other surfaces still carry older topic/event titles. That allows title drift and makes future reconciliation capable of restoring stale titles.

## Canonical rule

Every selected R2 chapter title should answer:

> **Who is Greg in this chapter?**

A valid title may name an occupation, social position, temporary function, relational role, situational identity, or clean metaphorical role that Greg actually inhabits.

A title fails when it primarily names an object, event, place, time span, abstraction, problem, or topic, or when the named role materially belongs to another character instead of Greg.

Duplicate roles are allowed. Broad roles are allowed when they are true. Do not invent awkward occupational nouns merely to satisfy the pattern.

Human-facing title style uses standard title case such as `The Boy`, `The Novice`, `The Neighbor`, and `The Adventurer`.

## Authority model

Stable identity remains:

- `r2-chNNN` for R2 chapter identity
- `ga-NNN` for Greg, Again audio identity
- numeric chapter number for cross-surface reconciliation

Title wording is mutable metadata and never owns identity.

For a selected/public R2 chapter, the **selected written chapter heading** is the semantic title authority. Public manifests, production registry metadata, audio manifest metadata, chapter lists, and future role-card/divider art consume that title.

Working story-search or rehearsal titles may differ before selection. Once a chapter is selected for public R2, its selected written heading must satisfy the role-title rule.

## Propagation

The title flow is:

```text
selected R2 written heading
        ↓
public chapter manifest
        ↓
production registry metadata
        ↓
audio manifest title metadata
        ↓
Listen / Read / future divider-card display
```

No downstream renderer should independently invent a competing chapter title.

Changing a title must not rename or regenerate:

- chapter IDs
- numeric chapter numbers
- audio files
- take maps
- route paths
- publication ownership
- chapter prose beyond the heading itself

## Reconciliation tooling

Add one deterministic R2 title synchronizer/checker. It should:

1. read the selected written heading for each published R2 chapter;
2. compare that title by numeric chapter number against the public chapter manifest, production registry, and audio manifest when audio exists;
3. update metadata-only surfaces when explicitly run in apply mode;
4. report drift in check mode;
5. never infer chapter identity from title text;
6. never alter prose body text or media binaries.

The tool does not judge whether prose content truly supports a role title. That remains an editorial judgment recorded in the role-title audit. The tool enforces propagation and continuity after that judgment is made.

## Current-frontier audit

Audit current selected R2 Chapters 1 through 26 against the actual selected chapter text.

For each chapter record:

- current selected heading
- KEEP or RENAME
- approved role title when renamed
- short evidence note explaining the Greg role

Only title headings and title metadata are changed. Chapter story text remains byte-for-byte unchanged below the heading.

## Forward-production rule

`r2/WRITTEN_PRODUCTION.md` must require role-title validation at selection/publication time. `r2/AUDIO_PRODUCTION.md` must state that audio title metadata follows selected written/R2 authority by stable chapter number and that title changes never imply missing or invalid audio.

## Tests

Regression coverage should verify:

- stable IDs/numbers are unchanged by title reconciliation;
- selected written heading and public chapter manifest title match;
- registry title matches selected written authority;
- existing audio-manifest entries match selected written authority by numeric chapter number;
- the known Chapter 2 style of drift cannot recur;
- the synchronizer changes only title metadata/headings and leaves routes/media references untouched;
- all current-frontier approved role titles pass the repository's expected snapshot.

## Five queued updates

1. **Doctrine:** durable R2 role-title policy and authority contract.
2. **Continuity:** current-frontier Chapters 1-26 role-title audit ledger.
3. **Leverage:** deterministic title reconciliation/check tooling keyed by stable chapter number.
4. **Guardrails:** regression tests for cross-surface title parity and stable identity.
5. **Routing:** forward written/audio production guidance that invokes the same title authority instead of independent title invention.

## Non-goals

- no story prose rewrite
- no audio regeneration
- no route renumbering
- no new role field that can drift from `title`
- no mechanical invention of role nouns
- no Run 1 manuscript-title changes
- no broad reader redesign
