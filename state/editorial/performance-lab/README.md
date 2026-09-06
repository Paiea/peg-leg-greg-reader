# PERFORMANCE Lab

Status: EXPERIMENTAL, PRE-NOVELIZATION

Purpose: test whether the approved PERFORMANCE contract produces more human, asymmetric, character-specific scene behavior while preserving dramatic truth.

Pipeline under test:

`CURRENT PROSE -> DRAMATIC SCRIPT -> PERFORMANCE FRAMES -> PERFORMED SCRIPT -> SOURCE COMPARISON`

This lab does not produce novel prose and does not modify canon.

## Authority

- Manuscript source is pinned current-main prose recorded in `authority.lock.json`.
- Dialogue/performance guidance is pinned approved WIP authority recorded in `authority.lock.json`.
- WIP guidance informs the experiment only. It does not become manuscript authority.

## Artifact rules

- `fixture.md` stores exact source evidence and a compact Dramatic Script.
- `performed.md` stores ephemeral performance frames and an ownership-explicit performed script.
- `report.md` stores validation and source comparison evidence.
- `SUMMARY.md` records only the aggregate lab decision.

Temporary frames and performed scripts are experimental artifacts. Persistent character authority is not updated by this lab.

## Hard stop

Do not create novelized prose, patch `chapters/`, modify manuscript authority, or wire PERFORMANCE into forward generation. A successful lab may recommend a separate novelization design only.
