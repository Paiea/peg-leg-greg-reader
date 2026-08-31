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

**02: EXPLORE → RESEARCH WHEN A REAL GAP EXISTS → SYNTHESIZE → UPDATE WRITERS' ROOM STATE → HANDOFF**

**03: INTEGRATE → PRESSURE-TEST → CLASSIFY → UPDATE DURABLE BRAINS → RETURN NEW EDGE**

Then repeat as useful while 01 continues writing.

Reusable research belongs in `RESEARCH_LEDGER.md` and must separate supported practice, confidence / limits, story translation, and canon status. Research does not become canon automatically.

`LONG_SERIAL_RESIDUE_MAP.md` is the specialist possibility map for making time leave residue. It is not mandatory 01 boot material and does not outrank prose.

## Durable specialist brains

- `STORY_NORTH_STAR.md` — durable artistic direction
- `DEVELOPMENT_CYCLE.md` — 02↔03 workflow
- `LONG_SERIAL_RESIDUE_MAP.md` — longitudinal social/residue possibility map
- `RESEARCH_LEDGER.md` — sourced external knowledge; not canon by default
- `PROSE_PLAYBOOK.md` — craft guidance
- `CHARACTER_BIBLE.md` — durable character knowledge / anti-flattening
- `SETTING_BIBLE.md` — lived setting/world continuity
- `PLOT_CONTROL.md` — active engines, pressures, possibilities, avoidances
- `VISUAL_BIBLE.md` — illustration language / continuity
- `IMAGE_PRODUCTION.md` — image workflow
- `READER_DESIGN_LAB.md` — UI/graphics development ideas
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

Do NOT create a new range-stamped running manuscript for each forward chapter/pass.

Current recorded story endpoint is Chapter 226 — **THE REFERENCE**. Always verify `MANUSCRIPT_STATE.md` / running manuscript before using this number if newer work exists.

Repository exact-text availability:
- illustrated/static prose through Chapter 155 — **THE LEAK**
- recovered exact Chapters 156–219 in `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`
- Chapter 220+ forward prose in `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`

The recovered 156–219 block has not yet been consolidated into the permanent running manuscript. Do not reconstruct or rewrite it from summaries.

## Forward production workflow

For every new chapter:
1. Read current GitHub authority first, including the engine playbook.
2. Write one chapter at a time.
3. Preserve canon, character, plot, and scene intent.
4. Run the light prose/continuity pass.
5. Verify roughly 2,500–4,000 words and clear 2,500 unless explicitly changed.
6. Verify no em dashes in manuscript prose.
7. Update the SAME permanent running manuscript file in place.
8. Update the SAME compact state files in place.
9. Ship/checkpoint in small batches when following the current batch workflow.
10. Update reader surfaces only as needed, preserving newer UI/artwork work and exact-text authority.
11. In chat, give the active workflow's compact production note / handoff.

Normal forward production may update `main` directly when explicitly requested. Broad prose passes, reader rebuilds, mass illustration work, manuscript consolidation, broad renames, and structural cleanup should normally use a branch first.

## Visual production

Visual state remains separate from manuscript state. Existing reader artwork and visual-production material are preserved. Development contact sheets remain DEVELOPMENT unless explicitly promoted.

Use `VISUAL_BIBLE.md` + `IMAGE_PRODUCTION.md` for future coverage work. Reader/UI experimentation belongs in `READER_DESIGN_LAB.md` until validated principles graduate.

## Current synchronization rule

Update existing compact state before adding new state. Preserve engine-owned substance. Consult manuscript whenever exact prose, chronology, wording, or scene detail matters. Prefer one living file over range-stamped successors.

## NEXT_TASK — development

The first current-era theatre research cycle is integrated and parked. The first Lyssa alteration/rework external research wave is also integrated through Chapter 226.

Current graduated Lyssa residue:
- Chapter 224 explicitly establishes three active customers;
- customer visits can occur at the apartment;
- jobs can be delivered / paid while Greg is elsewhere;
- the brown-cuff customer creates separately paid requested rework;
- multiple unrelated garments can be active at once;
- Chapter 222 establishes Maren as a garment/thread supply shop and useful matching route.

Current non-canon pressures / possibilities include queue consequences, fitting-confirmation semantics, repeat/referral customers, remembered customer preferences, and alteration constraints. Do not promote them without prose.

Next 02↔03 cycle is **manuscript-first, not new external research**:
1. 02 audits authoritative exact Chapters 156–226 for Lyssa's existing customer / supplier / delivery / payment / referral / repeat-preference / work-space history.
2. 02 returns a compact evidence map distinguishing ESTABLISHED / UNCERTAIN / POSSIBILITY; no invented names or retroactive garment connections.
3. 03 pressure-tests that longitudinal evidence and graduates only useful residue.
4. Only then decide whether a new external research question is actually needed. Deliberate research pause is valid.
5. 01 continues forward production without waiting.

Always re-read current manuscript authority first because 01 may advance while development work continues.

Use the live `RE-PROMPT [02]` and `RE-PROMPT [03]` trailheads in their state files.