# R2 Temporal Engine Time + Constraints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make fictional time and at least one run constraint first-class Temporal Engine inputs, support conversational nudge overrides, and prevent planning/audit language from leaking into R2 prose.

**Architecture:** Keep the Temporal Engine as reusable doctrine, add one compact per-run contract template, and route temporal work through `AGENTS.md`. Temporal experiment state remains branch-local and non-canonical; useful survivors continue through the existing Future Survivor Protocol. Planner/scrubber state stays rich while the prose renderer receives only a reduced scene packet.

**Tech Stack:** Markdown repository doctrine and GitHub branch workflow; no runtime dependency changes.

**Spec:** `docs/superpowers/specs/2026-09-10-r2-temporal-engine-time-constraints-design.md`

## Global Constraints

- Accepted R2 story state and selected prose on current `main` remain authority.
- Every temporal run owns one clock and at least one meaningful run constraint.
- Explicit user instruction outranks inference.
- High-confidence inference is preferred over unnecessary clarification.
- Ask one concise question only when unresolved ambiguity would materially change the run.
- Soft nudges change selection pressure, not mechanical quotas.
- Word count is not temporal proof unless explicitly made hard.
- Planning/audit vocabulary must not leak into Greg-facing prose.
- Temporal experiment output remains non-canonical until normal survivor/re-performance/publication selection.
- No global permanent future-simulation ledger.

---

### Task 1: Rewrite the Temporal Engine contract

**Files:**
- Modify: `r2/editorial/character-rebuild/TEMPORAL_ENGINE.md`

**Interfaces:**
- Consumes: current character-first A/B/C/D horizon doctrine and the approved design spec.
- Produces: active reusable engine method with clock resolution, constraint resolution, nudge semantics, time-residue rules, renderer firewall, and run lifecycle.

- [ ] **Step 1: Preserve the existing character-first and survivor gates**

Read the current file and retain its useful horizon, character, friction, repetition, and re-performance rules.

- [ ] **Step 2: Replace obsolete experimental-only status**

Set status to active speculative-development doctrine on `main`; explicitly state that method authority does not make speculative prose canonical.

- [ ] **Step 3: Add the Temporal Run Contract**

Document required fields: authority anchor, clock, at least one hard constraint or soft nudge, optional output/fidelity target, and stop condition.

- [ ] **Step 4: Add clock inference behavior**

Encode resolution order: explicit user instruction → active run contract → high-confidence inference → one concise question only when material ambiguity remains.

- [ ] **Step 5: Add elapsed-time residue behavior**

Document that meaningful gaps should normally leave at least two concrete consequences before the new action fully settles, while remaining diagnostic rather than quota-driven.

- [ ] **Step 6: Add constraint and nudge behavior**

Differentiate hard constraints from soft nudges and include concrete examples such as `one year`, `Gold party`, `more action`, `a little more tropes`, and `do not make Greg Gold yet`.

- [ ] **Step 7: Add planner / renderer firewall**

Define the reduced Scene Packet and prohibit experiment/audit vocabulary from being fed into or emitted by prose merely because planning uses it.

- [ ] **Step 8: Verify continuity with existing doctrine**

Confirm A/B/C/D, character-first survivor gate, independent clocks, repetition gate, re-performance, and survivor labels remain represented.

### Task 2: Add the reusable per-run template

**Files:**
- Create: `r2/editorial/character-rebuild/TEMPORAL_RUN_TEMPLATE.md`

**Interfaces:**
- Consumes: Temporal Engine contract.
- Produces: a copyable branch-local `TEMPORAL_RUN.md` structure and reduced `SCENE_PACKET` handoff shape.

- [ ] **Step 1: Define run metadata**

Include status, authority anchor, experiment question, clock source/confidence, start, horizon/end, checkpoint strategy, stop condition, hard constraints, soft nudges, and explicit non-goals.

- [ ] **Step 2: Define nudge update log**

Record only changes that alter the current run contract; do not turn chat history into permanent transcript state.

- [ ] **Step 3: Define current state snapshot**

Track only clocks materially relevant to the active run: people, body, money, work, relationships, gear, geography, magic, reputation, obligations, and similar domains.

- [ ] **Step 4: Define reduced Scene Packet template**

Include time/gap, location, people/wants, physical situation, current state changes, scene-relevant constraints, non-contradiction facts, and surviving consequences. Explicitly exclude planning/audit vocabulary.

- [ ] **Step 5: Define resume behavior**

A fresh worker should be able to read the run contract and current authority, then continue after a simple `continue` without asking the user to repeat already-durable inputs.

### Task 3: Route temporal work and survivor handoff

**Files:**
- Modify: `AGENTS.md`
- Modify: `r2/FUTURE_SURVIVOR_PROTOCOL.md`
- Modify: `state/PROJECT_STATE.md`

**Interfaces:**
- Consumes: active Temporal Engine and run template.
- Produces: discoverable routing and clean authority handoff into existing survivor doctrine.

- [ ] **Step 1: Update `AGENTS.md` routing**

Add a Temporal Engine route for temporal/year/season/future-rehearsal requests and natural-language nudges. Require reading the current authority plus engine/run contract; keep speculative prose non-canonical.

- [ ] **Step 2: Update Future Survivor discovery contract**

Require surviving temporal material to carry its time horizon and relevant constraint state as experiment evidence, while preventing stale run constraints from becoming canon.

- [ ] **Step 3: Update project engine ownership**

List the Temporal Engine as a specialist speculative-development method and clarify it does not replace 01/02/03 or publish directly.

### Task 4: Verify the doctrine as a coherent system

**Files:**
- Verify: `r2/editorial/character-rebuild/TEMPORAL_ENGINE.md`
- Verify: `r2/editorial/character-rebuild/TEMPORAL_RUN_TEMPLATE.md`
- Verify: `AGENTS.md`
- Verify: `r2/FUTURE_SURVIVOR_PROTOCOL.md`
- Verify: `state/PROJECT_STATE.md`
- Verify: design + plan documents

**Interfaces:**
- Consumes: all prior tasks.
- Produces: a resumable, non-contradictory temporal-development workflow.

- [ ] **Step 1: Search for obsolete status language**

Confirm the engine no longer says it is active only on `experiment/r2-character-rebuild`.

- [ ] **Step 2: Check required semantics**

Verify the final doctrine contains: `clock`, `hard constraint`, `soft nudge`, `high-confidence inference`, `Scene Packet`, `continue`, and explicit non-canon authority boundaries.

- [ ] **Step 3: Run a paper test against the user's latest nudges**

Expected contract interpretation:

```text
CLOCK: one year
HARD CONSTRAINT: meaningful Gold-caliber party appears
SOFT NUDGES: more action; a little more recognizable fantasy/isekai trope pleasure
CONTINUE: preserve the current contract unless a later nudge changes it
WORD COUNT: fidelity target only unless explicitly hardened
```

- [ ] **Step 4: Review for renderer contamination**

Confirm the writer-facing packet does not require architecture terms such as horizon, rehearsal, quarry, authority, survivor label, or audit verdict.

- [ ] **Step 5: Review authority boundaries**

Confirm no temporal run can directly overwrite accepted R2 story truth or publish itself merely by completion.