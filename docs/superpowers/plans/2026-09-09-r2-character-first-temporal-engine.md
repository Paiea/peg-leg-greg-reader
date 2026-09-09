# R2 Character-First Temporal Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Activate a compact A/B/C/D temporal engine on the isolated R2 character-rebuild branch, use reconstructed 27–31 as calibration, and continue the rebuild from Chapter 32 without touching public R2.

**Architecture:** Keep routing state and operating rules inside `r2/editorial/character-rebuild/`. A is a numbered 3–5 chapter full-fidelity run; B is high-fidelity replaceable future material; C/D are unnumbered character-clock rehearsals. Promotion requires fresh character reference, connected-read challenge, and re-performance rather than direct speculative copy.

**Tech Stack:** Markdown editorial state/prose in GitHub; existing R2 Shared Greg Surface conventions; GitHub branch isolation.

**Spec:** `docs/superpowers/specs/2026-09-09-r2-character-first-temporal-engine-design.md`

## Global Constraints

- Work only on `experiment/r2-character-rebuild`.
- Do not modify public R2 written, reader, data/registry, audio, or image surfaces.
- Historical later R2 is quarry/evidence, never rebuild chronology authority.
- A contains 3–5 connected full-fidelity chapters.
- B contains 3–5 high-fidelity replaceable scene/chapter-equivalent units.
- C/D remain unnumbered until promotion earns chronology.
- No C/D prose promotes directly; B also receives fresh re-performance when it approaches A.
- Character-specific wants, independent clocks, scene discovery, and unresolved residue outrank procedural neatness.
- No new permanent doctrine hierarchy or giant simulation ledger.

---

### Task 1: Install compact temporal control layer

**Files:**
- Create: `r2/editorial/character-rebuild/TEMPORAL_ENGINE.md`
- Create: `r2/editorial/character-rebuild/HORIZON_STATE.md`

**Interfaces:**
- Consumes: character-first rebuild `SPEC.md`, 27–31 `evaluation.md`, temporal-engine design spec.
- Produces: the operational A/B/C/D contract and the single current routing/clocks state used by later tasks.

- [ ] **Step 1:** Create `TEMPORAL_ENGINE.md` with A/B/C/D confidence definitions, survivor gate, connected-run challenger, re-performance rule, and public-surface boundary.
- [ ] **Step 2:** Create initial `HORIZON_STATE.md` with A = Chapters 32–35 HARD; B = next hard material provisional; C/D = unnumbered pressure clusters; relevant current clocks for Greg, Mara, Jorren, Noll, filtration group, Tavin, and support assessment.
- [ ] **Step 3:** Read both files against the design spec and remove any extra doctrine, numbered far-future destiny, or duplicated character bible material.
- [ ] **Step 4:** Compare branch against `main`; expected changed paths remain only docs/rebuild-editorial paths.

### Task 2: Fresh-search and write A run 32–35

**Files:**
- Create: `r2/editorial/character-rebuild/run-032-035/scene-search.md`
- Create: `r2/editorial/character-rebuild/run-032-035/ch032.md`
- Create: `r2/editorial/character-rebuild/run-032-035/ch033.md`
- Create: `r2/editorial/character-rebuild/run-032-035/ch034.md`
- Create: `r2/editorial/character-rebuild/run-032-035/ch035.md`

**Interfaces:**
- Consumes: exact revised 27–31, current relevant earlier character references, later quarry only when a specific live pressure calls for it, `HORIZON_STATE.md`.
- Produces: first numbered temporal A run after calibration.

- [ ] **Step 1:** Fresh-read exact revised 27–31 continuously plus exact relevant Mara/Noll/filtration references.
- [ ] **Step 2:** Write a compact immediate-only `scene-search.md` for 32–35. It must specify each chapter's scene grammar, independent clock, wants, discovery, and residue without outlining beyond 35.
- [ ] **Step 3:** Write Chapter 32 at full R2 Shared Greg Surface fidelity.
- [ ] **Step 4:** Write Chapter 33 at full fidelity from the new state created by 32.
- [ ] **Step 5:** Write Chapter 34 at full fidelity from the new state created by 32–33.
- [ ] **Step 6:** Write Chapter 35 at full fidelity from the new state created by 32–34.
- [ ] **Step 7:** Stop numbered A writing at 35 before judging the connected run.

### Task 3: Evaluate and accept only the A-side contiguous win

**Files:**
- Create: `r2/editorial/character-rebuild/run-032-035/evaluation.md`
- Modify only clear losing `ch032.md`–`ch035.md` files if needed.

**Interfaces:**
- Consumes: complete 32–35 run and calibration 27–31 evaluation.
- Produces: PASS/MIXED/FAIL evidence and the accepted branch-only A frontier.

- [ ] **Step 1:** Fresh-read 32–35 continuously without editing.
- [ ] **Step 2:** Run character, anonymous, repetition, scene-discovery, independent-agency, and unresolved-residue challengers.
- [ ] **Step 3:** Record chapter and run verdicts in `evaluation.md`.
- [ ] **Step 4:** Revise only clear losers; preserve source wherever challenger does not clearly win.
- [ ] **Step 5:** Fresh-read the revised connected run.
- [ ] **Step 6:** If the run still materially fails, do not activate further hard chronology. If it passes, set rebuild A frontier to 35 in `HORIZON_STATE.md`.

### Task 4: Populate B/C/D without turning them into railroad

**Files:**
- Create: `r2/editorial/character-rebuild/temporal/b-hard/` files for 3–5 high-fidelity scene units.
- Create: `r2/editorial/character-rebuild/temporal/c-warm.md`
- Create: `r2/editorial/character-rebuild/temporal/d-cold.md` only if a real far-edge contrast exists.
- Modify: `r2/editorial/character-rebuild/HORIZON_STATE.md`

**Interfaces:**
- Consumes: accepted A through 35.
- Produces: replaceable future rehearsal material, not accepted chronology.

- [ ] **Step 1:** Ask what current 35 actually claims forward; do not reuse pre-A guesses automatically.
- [ ] **Step 2:** Write 3–5 B units at high fidelity using provisional scene labels, not protected chapter numbers.
- [ ] **Step 3:** Create one C warm rehearsal around the strongest independent character clock not already exhausted by B.
- [ ] **Step 4:** Create D only if another materially distinct pressure needs cheap scouting; otherwise record D as intentionally empty.
- [ ] **Step 5:** Update horizon state with survival status, uncertainty, and what must be re-read before any promotion.

### Task 5: Reconcile and verify first temporal cycle

**Files:**
- Create: `r2/editorial/character-rebuild/temporal/reconciliation-001.md`
- Modify: `r2/editorial/character-rebuild/HORIZON_STATE.md`

**Interfaces:**
- Consumes: accepted A, B/C/D rehearsal, branch compare.
- Produces: first explicit temporal cycle reconciliation and safe next action.

- [ ] **Step 1:** Compare A against B/C/D only for facts/pressures that can affect the accepted front.
- [ ] **Step 2:** Classify future material `SOURCE WIN / REPERFORM / FORK / DISCOVERY ONLY / KILL`.
- [ ] **Step 3:** Record what B/C/D survives without assigning chronology to material that has not earned it.
- [ ] **Step 4:** Fresh compare `main...experiment/r2-character-rebuild` and confirm all changes remain under docs or rebuild-editorial paths.
- [ ] **Step 5:** Record the next A action in `HORIZON_STATE.md`; do not publish public R2.
