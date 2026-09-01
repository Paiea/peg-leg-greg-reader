# PEG-LEG GREG — GENERAL EDITOR STATE

Updated: 2026-08-31 HST

## Lane

06 — MANUSCRIPT POLISH / GENERAL EDITOR

Medium-strength whole-manuscript editorial pass.

Target:

**CLEAN → TIGHTEN → CLARIFY → SMOOTH → CHECK CONTINUITY**

Use Level 1–3 edits only. Stop before Level 4 and flag substantial rewrites for the Heavy Prose Editor.

Preserve voice, scene order, scene outcomes, ordinary-life texture, relationship residue, humor, and canon. Do not use em dashes in manuscript prose.

## Current authority

Fresh `main` authority for the completed first batch is commit `128208fb38a125f96cf90c2b18030f992ef01894`, with the forward Manuscript Engine at Chapter 238 — THE SEALER.

Heavy Prose Editor authority remains complete through Chapter 183, with Chapter 184 next. This front-book moderate-polish lane does not overlap that completed heavy-edit range.

## Current polish edge

POLISH COMPLETE AND SOURCE-SYNCHRONIZED:

- Chapter 1 — THE BOY
- Chapter 2 — THE BORROWER
- Chapter 3 — THE INVESTOR
- Chapter 4 — THE EXPERT
- Chapter 5 — THE WARRIOR

Branch:

`editor/general-polish-ch001-005-20260831`

PR:

`#34 — General polish: Chapters 1-5`

Next sequential range:

- Chapters 6–10

## Editorial character of first batch

Predominantly Level 2 polish with a small amount of Level 3 sentence/paragraph repair.

Main targets:

- reduce accidental fragment stacking while preserving intentional Greg cadence
- remove repeated conclusions and duplicated self-explanation
- smooth transitions between memory, inference, and present evidence
- preserve board/list humor and ordinary money/training/logistics texture
- repair dialogue attribution and speaker continuity where the intended speaker is clear

## Continuity notes

Confirmed repairs in the first batch:

- Chapter 2 loan-room dialogue incorrectly attributed one Antonius line to Pell; corrected to Antonius.
- Chapter 2 Sella encounter incorrectly attributed Greg's answer `You` to Sella; corrected to Greg.
- Chapter 3 Antonius meeting contained a broken Pell/Antonius dialogue residue; repaired without changing scene intent.
- The apparent Jorren duplicate is resolved by later manuscript authority: Chapter 14 establishes **Jorren** as Greg's recurring Bronze guild/sparring partner, while Chapter 5 later identifies **Rusk** as Antonius's large, quiet man whom Greg had already met twice. Chapter 3's scarred Vale associate is therefore corrected from Jorren to **Rusk**. Fighter Jorren remains unchanged.

## Book 1 source authority

Canonical Book 1 source remains:

`state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx`

`chapters/001.html` through `chapters/082.html` remain publishing/reader derivatives.

The source-authority gate is resolved through an explicit repository-supported promotion path:

- `scripts/promote_book1_polish.py`
- `tests/test_promote_book1_polish.py`
- `.github/workflows/book1-source-sync.yml`

The promotion tool:

- reads only the requested HTML chapter prose
- rejects em dashes in promoted manuscript prose
- replaces only requested chapter bodies between canonical DOCX headings
- reopens and verifies the saved DOCX
- verifies promoted chapter text matches the approved reader prose exactly
- verifies every untargeted Book 1 chapter remains text-identical
- preserves the canonical chapter-heading count
- is idempotent: when the requested canonical chapter bodies already match approved reader prose, it exits without rewriting the DOCX package

Chapters 1–5 have been promoted into the canonical Book 1 DOCX and reverified as already synchronized.

A full dry-run render of the synchronized canonical DOCX produced 1,293 pages successfully. Contact-sheet inspection covered the complete document and showed no visible truncation, runaway spacing, blank-page corruption, or damaged chapter headings.

Final validation after the idempotence repair:

- canonical Book 1 Chapters 1–5 rerun: already synchronized; DOCX hash unchanged
- edited-prose em-dash check: clean
- repository tests: 21 passed
- Light 156–219: 64 chapters generated and verified
- current Light 220–238: 19 chapters generated and verified
- publishing/navigation checks: passed
- generated reader presentation: current

For future Book 1 batches, edit the bounded reader prose, verify it, then promote the accepted range into the canonical DOCX before merge. Do not merge HTML-only Book 1 polish.
