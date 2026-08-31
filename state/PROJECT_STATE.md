# PEG-LEG GREG — PROJECT STATE

**Repository role:** durable project source and savestate.
**Reader role:** primary human reading interface.
**Manuscript role:** authoritative story text.
**State-file role:** compact operating memory for production/editorial/visual/development workers.

## Authority

For story content: newest authoritative manuscript prose → explicit author decisions → established Story Control decisions → current state files → Writers' Room exploration → external research / analogy.

For editorial execution: newest authoritative manuscript prose → explicit author decisions → established craft updates → Editor state → exploratory discussion.

`STORY_NORTH_STAR.md` is durable artistic direction. It helps workers choose between valid options but does not override manuscript canon.

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
- 02 / Writers' Room: `WRITERS_ROOM_STATE.md` + `DEVELOPMENT_CYCLE.md` + `RESEARCH_LEDGER.md`
- 03 / Story Control: `STORY_CONTROL_STATE.md` + `DEVELOPMENT_CYCLE.md` + plot/character/setting brains
- 04 / Editor: `EDITOR_STATE.md`
- Codex/repository integration: synchronize, validate, preserve supplied engine state; do not invent canon or rewrite engine decisions.

`MANUSCRIPT_ENGINE_PLAYBOOK.md` preserves HOW 01 should think/work. It is durable method, not a canon summary. Current facts belong in manuscript state/open threads and exact prose belongs in the manuscript.

## Shared artistic direction

`STORY_NORTH_STAR.md` defines the current project-wide artistic target.

Core principles include:
- accumulation as the repeatable pleasure
- belonging through accumulated work, relationships, obligations, routes, money, jokes, and social memory
- make time leave residue
- social density over lore density
- world continues offscreen
- different relationships have different languages
- Greg may be messy / wrong / insecure without becoming artificially dysfunctional
- ordinary life remains present when stakes rise
- money and material improvement remain real
- reputation is networked and inconsistent
- long-delay continuity and micro-payoffs are strengths
- major payoffs should often emerge from ordinary accumulated competence
- resist fragment spam, over-explanation, neat lesson endings, protagonist gravity, and power-fantasy escalation

## Development loop — 02 ↔ 03

`DEVELOPMENT_CYCLE.md` defines the continuous development system around 01.

Preferred cycle:

**02: EXPLORE → RESEARCH → SYNTHESIZE → UPDATE WRITERS' ROOM STATE → HANDOFF**

**03: INTEGRATE → PRESSURE-TEST → CLASSIFY → UPDATE DURABLE BRAINS → RETURN NEW EDGE**

Then repeat as useful while 01 continues writing.

02 may research real acting, stagecraft, backstage practice, garment work, disability/mobility, experimental method, commerce/logistics, travel, institutions, and other focused questions when real knowledge can replace generic invented texture.

Reusable research belongs in `RESEARCH_LEDGER.md` and must separate:
- supported source/practice
- confidence / limits
- story translation
- canon status

Research does not become canon automatically.

03 decides what should remain POSSIBILITY, what creates PRESSURE, what is AVOID, what is already ESTABLISHED, and what needs another RESEARCH EDGE.

01 should consume compact graduated residue, not every exploratory note. Preserve manuscript throughput.

## Durable specialist brains

These files store reusable method/knowledge without outranking manuscript prose:

- `STORY_NORTH_STAR.md` — durable artistic direction / what the serial is trying to become
- `DEVELOPMENT_CYCLE.md` — 02↔03 exploration/research/integration workflow
- `RESEARCH_LEDGER.md` — sourced external knowledge and story translations; not canon by default
- `PROSE_PLAYBOOK.md` — craft guidance for drafting/editing
- `CHARACTER_BIBLE.md` — durable character knowledge and anti-flattening constraints
- `SETTING_BIBLE.md` — lived setting/world continuity
- `PLOT_CONTROL.md` — active engines, pressures, possibilities, avoidances
- `VISUAL_BIBLE.md` — illustration language, movement, continuity, KEEP/RETRY
- `IMAGE_PRODUCTION.md` — coverage-first 5x5 batch workflow
- `READER_DESIGN_LAB.md` — UI/graphics ideas and experiments not yet project law
- `HANDSHAKE_PROTOCOL.md` — cross-chat continuation convention

The Manuscript Engine should not read every specialist file every chapter. Preserve throughput: read core manuscript files first and consult specialist brains only when the chapter/task needs them. `STORY_NORTH_STAR.md` is compact enough to use as shared orientation, especially in fresh chats and at batch boundaries.

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

Current recorded story endpoint is Chapter 226 — **THE REFERENCE**. Always verify `MANUSCRIPT_STATE.md` / running manuscript before using this number if newer work exists.

Repository exact-text availability is now:
- illustrated/static prose through Chapter 155 — **THE LEAK**
- recovered exact Chapters 156–219 in `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`
- Chapter 220+ forward prose in `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`

The Light Reader may use the recovered 156–219 file directly to provide continuous text navigation. The recovered block has not yet been consolidated into the permanent running manuscript; do not reconstruct or rewrite it from summaries.

## Forward production workflow

For every new chapter:
1. Read current GitHub authority first, including the engine playbook.
2. Write one chapter at a time.
3. Preserve canon, character, plot, and scene intent.
4. Run the light prose/continuity pass.
5. Verify roughly 2,500–4,000 words and clear 2,500 unless the author explicitly changes the target.
6. Verify no em dashes in manuscript prose.
7. Update the SAME permanent running manuscript file in place.
8. Update the SAME compact state files in place. Do not create chapter-numbered state clones.
9. Ship/checkpoint in small batches when following the current batch workflow.
10. Update reader surfaces only as needed, preserving newer UI/artwork work and exact-text authority.
11. In chat, give a compact production note and then a full copyable next-edge re-prompt in ONE code block when the active workflow calls for it.

Normal forward production may update `main` directly when explicitly requested. Broad prose passes, reader rebuilds, mass illustration work, manuscript consolidation, broad renames, and structural cleanup should normally use a branch first.

## Visual production

Visual state remains separate from manuscript state. Existing reader artwork and visual-production material are preserved. Development contact sheets remain DEVELOPMENT unless explicitly promoted.

Use `VISUAL_BIBLE.md` + `IMAGE_PRODUCTION.md` for future coverage work. Reader/UI experimentation belongs in `READER_DESIGN_LAB.md` until validated principles graduate into production guidance.

## Current synchronization rule

Update existing compact state before adding new state. Preserve engine-owned substance. Consult the manuscript whenever exact prose, chronology, wording, or scene detail matters. Prefer one living file over range-stamped successor files. Historical files may remain temporarily for provenance/cleanup, but they are not the forward naming convention.

## NEXT_TASK — development

Restart the 02↔03 cycle from the current manuscript era.

First wave:
1. 02 researches acting / rehearsal-note practice using credible sources and records reusable findings in `RESEARCH_LEDGER.md`
2. 02 translates the strongest findings into recurring behaviors for the existing troupe, with emphasis on social memory / informal authority / offscreen life
3. 03 pressure-tests those possibilities against current manuscript evidence and graduates only useful residue
4. 03 identifies the next focused research edge back to 02
5. repeat without making 01 wait

Use the live `RE-PROMPT [02]` and `RE-PROMPT [03]` trailheads in their state files.
