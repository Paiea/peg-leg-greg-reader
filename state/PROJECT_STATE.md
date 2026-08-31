# PEG-LEG GREG — PROJECT STATE

**Repository role:** durable project source and savestate.
**Reader role:** primary human reading interface.
**Manuscript role:** authoritative story text.
**State-file role:** compact operating memory for production/editorial/visual workers.

## Authority

For story content: newest authoritative manuscript prose → explicit author decisions → established Story Control decisions → current state files → Writers' Room exploration.

For editorial execution: newest authoritative manuscript prose → explicit author decisions → established craft updates → Editor state → exploratory discussion.

When overlapping files conflict, the newer GitHub-authoritative version outranks stale incoming copies. Do not silently replace newer repository work with older local material.

## Universal worker routing

Root `AGENTS.md` is the entry point for a fresh repository-aware worker.

Normal pattern:
- CHAT: exploration / temporary working context
- GITHUB BRANCH: durable work in progress for broad/risky changes
- GITHUB MAIN: accepted current authority

`state/HANDSHAKE_PROTOCOL.md` defines how one disposable worker leaves a trailhead for the next.

## Engine ownership

- 01 / Manuscript Engine: `MANUSCRIPT_ENGINE_PLAYBOOK.md`, `MANUSCRIPT_STATE.md`, `MANUSCRIPT_WORKFLOW.md`, `OPEN_THREADS.md`, `MANUSCRIPT_CHAPTER_INDEX.md`
- 02 / Writers' Room: `WRITERS_ROOM_STATE.md`
- 03 / Story Control: `STORY_CONTROL_STATE.md`
- 04 / Editor: `EDITOR_STATE.md`
- Codex/repository integration: synchronize, validate, preserve supplied engine state; do not invent canon or rewrite engine decisions.

`MANUSCRIPT_ENGINE_PLAYBOOK.md` preserves HOW 01 should think/work. It is durable method, not a canon summary. Current facts belong in manuscript state/open threads and exact prose belongs in the manuscript.

## Durable specialist brains

These files store reusable method/knowledge without outranking manuscript prose:

- `PROSE_PLAYBOOK.md` — craft guidance for drafting/editing
- `CHARACTER_BIBLE.md` — durable character knowledge and anti-flattening constraints
- `SETTING_BIBLE.md` — lived setting/world continuity
- `PLOT_CONTROL.md` — active engines, pressures, possibilities, avoidances
- `VISUAL_BIBLE.md` — illustration language, movement, continuity, KEEP/RETRY
- `IMAGE_PRODUCTION.md` — coverage-first 5x5 batch workflow
- `READER_DESIGN_LAB.md` — UI/graphics ideas and experiments not yet project law
- `HANDSHAKE_PROTOCOL.md` — cross-chat continuation convention

The Manuscript Engine should not read every specialist file every chapter. Preserve throughput: read core manuscript files first and consult specialist brains only when the chapter/task needs them.

## Book 1

Closed at Chapter 82 — **THE RECONCILER**.

Current Book 1 manuscript authority: `state/manuscript/Peg_Leg_Greg_authoritative_ch82_final_name_map.docx`.

Approved canonical continuity:
- Pel Marris → Silas Marris
- Pellian / Pell → Arlo
- Ressa Vale → Iona Vale
- Pera → Iris
- Lysa → Lyssa, same existing character

No additional Book 1 naming decisions are authorized.

The manuscript-wide social-names pass preserves established nickname ownership and chronology. Late/private **Aileen** belongs only to Lyssa at Chapter 123; it is not a general name for Greg.

## Book 2

Active manuscript.

Locked earlier source remains `state/manuscript/Peg_Leg_Greg_Book2_Manuscript_Ch83-137.docx`.

Permanent forward path:

`state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`

Do NOT create a new `Peg_Leg_Greg_Running_Manuscript_ChXXX-YYY.md` file for each chapter or shipping pass. Update the permanent running manuscript in place.

Current story endpoint is Chapter 224 — **THE CHECKER**.

Repository prose was previously validated continuously through Chapter 155 — **THE LEAK**. Chapters 156–219 remain newer forward material pending exact-text synchronization into the permanent file and must not be reconstructed from summaries. Chapters 220 and later are materialized directly in the permanent running manuscript.

## Forward production workflow

For every new chapter:
1. Read current GitHub authority first, including the engine playbook.
2. Write one chapter at a time.
3. Preserve canon, character, plot, and scene intent.
4. Run the prose/continuity pass.
5. Verify roughly 2,500–4,000 words and clear 2,500 unless the author explicitly changes the target.
6. Verify no em dashes in manuscript prose.
7. Update the SAME permanent running manuscript file in place.
8. Update the SAME compact state files in place. Do not create chapter-numbered state clones.
9. Update reader surfaces only as needed, preserving newer UI/artwork work and known synchronization gaps.
10. In chat, give a compact production note and then a full copyable next-edge re-prompt in ONE code block. The re-prompt ritual remains part of the workflow even though GitHub is the durable savestate.

Normal one-chapter forward production may update `main` directly when explicitly requested. Broad prose passes, reader rebuilds, mass illustration work, manuscript consolidation, broad renames, and structural cleanup should normally use a branch first.

## Visual production

Visual state remains separate from manuscript state. Existing reader artwork and visual-production material are preserved. Development contact sheets remain DEVELOPMENT unless explicitly promoted.

Use `VISUAL_BIBLE.md` + `IMAGE_PRODUCTION.md` for future coverage work. Reader/UI experimentation belongs in `READER_DESIGN_LAB.md` until validated principles graduate into production guidance.

## Current synchronization rule

Update existing compact state before adding new state. Preserve engine-owned substance. Consult the manuscript whenever exact prose, chronology, wording, or scene detail matters. Prefer one living file over range-stamped successor files. Historical files may remain temporarily for provenance/cleanup, but they are not the forward naming convention.

## NEXT_TASK — infrastructure

After this brain integration lands, highest-value safe side-lane work is:

1. consolidate `assets/reader.css` without changing good behavior
2. validate representative desktop/mobile chapter pages and image roles
3. update `READER_DESIGN_LAB.md` with only durable findings
4. do not touch manuscript prose or reconstruct missing Chapters 156–219 from summaries

Use a dedicated branch for the CSS pass.