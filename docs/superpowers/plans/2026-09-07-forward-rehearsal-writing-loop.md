# Forward REHEARSAL Writing Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair forward manuscript routing, lock REHEARSAL before prose, prove the loop across Chapters 493-500, evaluate it at 500, and graduate it if the evidence is positive.

**Architecture:** Keep exact prose and `MANUSCRIPT_STATE.md` as authority. Add a compact forward REHEARSAL contract and proving-run ledger. Each chapter begins from current GitHub authority, explores a few story-beat possibilities, invokes PERFORMANCE only for material embodied uncertainty, renders one chapter, records what actually survived, and ships before the next chapter begins.

**Tech Stack:** Markdown/JSON project state, existing Peg-Leg Greg manuscript workflow, existing REHEARSAL/PERFORMANCE runtime concepts, GitHub validation workflows.

**Spec:** `docs/superpowers/specs/2026-09-07-forward-rehearsal-writing-loop-design.md`

## Global Constraints

- Canon prose remains the only story authority.
- `MANUSCRIPT_STATE.md` owns the exact endpoint and executable next trailhead.
- REHEARSAL happens before prose from Chapter 493 onward during the proving run.
- PERFORMANCE is optional and used only for materially important embodied-behavior uncertainty.
- One complete chapter is one durable shipping transaction.
- No em dashes in manuscript prose.
- Preserve body, money, magic, relationship, chronology, geography, and knowledge ceilings.
- Do not force every story engine into every chapter.
- Do not promote rehearsal-only private motives into canon.
- At Chapter 500 evaluate the workflow itself before scaling.

---

### Task 1: Repair the forward state spine

**Files:**
- Modify: `state/OPEN_THREADS.md`
- Modify: `state/MANUSCRIPT_CHAPTER_INDEX.md`
- Read: `state/MANUSCRIPT_STATE.md`

**Interfaces:**
- Consumes: current Chapter 492 authority from `MANUSCRIPT_STATE.md` and exact recent checkpoint prose.
- Produces: compact current routing that cannot mislead a fresh worker into treating Chapter 320 or Chapter 248 as the active edge.

- [ ] **Step 1: Replace stale open-thread history with current live pressures**

Keep only material that can still change a future chapter: Chapter 492 gray-freight follow-up, work-limb completion, magic 59/53/159 evidence ceilings, theatre current state, current economic/capital direction, unresolved artifact/provenance lanes, relationships that materially changed, and protected uncertainty that is still truly live.

- [ ] **Step 2: Make the chapter index compact and current**

Set endpoint to Chapter 492. Preserve the existing historical 1-248 title list as archival title history if useful, but remove any implication that 248 is the story endpoint. Add a recent-title window sourced from exact checkpoint headers and direct workers to search checkpoint headers for full post-248 title history rather than manually caching 244 titles in this file.

- [ ] **Step 3: Re-read both files against `MANUSCRIPT_STATE.md`**

Verify there is no conflicting current money, body, magic, debt, work-limb, or endpoint claim.

- [ ] **Step 4: Commit the state-spine repair**

Commit message: `Repair forward manuscript state spine`

---

### Task 2: Lock the pre-prose REHEARSAL contract

**Files:**
- Create: `state/editorial/rehearsal/FORWARD_WORKFLOW.md`
- Create: `state/editorial/rehearsal/forward/proving-run-493-500.json`
- Modify: `state/MANUSCRIPT_WORKFLOW.md`

**Interfaces:**
- Consumes: `CONVERGENCE_001_491.md`, `converged-memory.json`, `MANUSCRIPT_STATE.md`, relevant current story state.
- Produces: a durable per-chapter input/output contract and proving-run ledger used by Chapters 493-500.

- [ ] **Step 1: Write `FORWARD_WORKFLOW.md`**

Define the exact per-chapter order:

`GitHub authority -> recent rhythm -> relevant story memory -> 2-5 competing scene possibilities -> REHEARSAL discoveries -> optional PERFORMANCE -> selected scene packet -> prose -> light validation -> story sync -> durable chapter transaction`.

Explicitly state that REHEARSAL returns discoveries, not chapter prose.

- [ ] **Step 2: Define the proving-run ledger schema**

Use one JSON document with `schema`, `range`, `status`, `chapters`, and `evaluation`.

Each chapter record contains:

```json
{
  "chapter": 493,
  "status": "pending",
  "source_authority": null,
  "pressure": null,
  "possibilities": [],
  "selected_discoveries": [],
  "performance": {"used": false, "reason": null},
  "prose_result": null,
  "character_surprise": null,
  "protagonist_gravity": null,
  "memory_helped": null,
  "next_trailhead": null
}
```

Create records for 493-500.

- [ ] **Step 3: Insert REHEARSAL into `MANUSCRIPT_WORKFLOW.md` before drafting**

Replace the current private light-contract drafting step with a pre-prose REHEARSAL step. Keep artifact/economy/action routing intact. Add PERFORMANCE escalation criteria and a post-prose ledger/story-sync step.

- [ ] **Step 4: Verify YAGNI**

Confirm there is no new router, no required performance call, no second canon state, and no mandatory large packet for simple chapters.

- [ ] **Step 5: Commit the workflow contract**

Commit message: `Lock forward REHEARSAL before prose`

---

### Task 3: Validate and merge the workflow branch

**Files:**
- Review all files changed in Tasks 1-2.

**Interfaces:**
- Consumes: branch `editor/forward-rehearsal-493-500`.
- Produces: green merged workflow/state authority on `main` before Chapter 493 is drafted.

- [ ] **Step 1: Open a PR against `main`**

PR title: `Lock forward REHEARSAL loop for chapters 493-500`.

- [ ] **Step 2: Run repository PR validation**

Require the existing Showcase/reader/repository validation to complete green on the exact PR head.

- [ ] **Step 3: Review the diff for stale authority leakage**

Check that no prose, chapter canon, or unrelated specialist state was changed.

- [ ] **Step 4: Merge the exact validated head**

Use the repository-supported merge method and record the merge SHA.

- [ ] **Step 5: Re-read `main`**

Verify Chapter 492 remains the endpoint and the new workflow/state spine is present.

---

### Task 4: Run Chapters 493-499 one chapter at a time

**Files per chapter N:**
- Create: `state/manuscript/Peg_Leg_Greg_Chapter_N_EXACT_WIP.md`
- Modify: `state/MANUSCRIPT_STATE.md`
- Modify: `state/editorial/rehearsal/forward/proving-run-493-500.json`
- Modify only when materially changed: `state/OPEN_THREADS.md`
- Modify compact recent-title window when useful: `state/MANUSCRIPT_CHAPTER_INDEX.md`

**Interfaces:**
- Consumes: current `main` after Chapter N-1.
- Produces: exact Chapter N plus synchronized state and one completed proving-run record.

For each N from 493 through 499:

- [ ] **Step 1: Re-read current `main` authority**

Read `MANUSCRIPT_STATE.md`, exact Chapter N-1, relevant recent chapters, `FORWARD_WORKFLOW.md`, converged memory, and only the specialist files demanded by the actual pressure.

- [ ] **Step 2: Run pre-prose REHEARSAL**

Write 2-5 beat-level possibilities into the proving-run record. Identify which pressure is strongest, who owns decisive knowledge/action, what uncertainty stays protected, and which alternatives lose.

- [ ] **Step 3: Decide PERFORMANCE**

Set `performance.used=true` only if embodied behavior is materially uncertain or important under the contract. Record the reason either way.

- [ ] **Step 4: Render one complete chapter**

Target roughly 2,500-4,000 words unless the story strongly earns a different length. Use `THE [ROLE]` title and check title collision against repository history.

- [ ] **Step 5: Run chapter validation**

Verify sequential chapter number, title, no em dash, relevant numerical continuity, protected uncertainty, economic calibration when money matters, and dialogue ownership.

- [ ] **Step 6: Story Sync from actual prose**

Update `MANUSCRIPT_STATE.md` with what actually happened and the next executable trailhead. Update `OPEN_THREADS.md` only for materially changed live pressures. Complete the proving-run record with what survived, what surprised, protagonist-gravity assessment, and whether memory materially helped.

- [ ] **Step 7: Ship and re-read main**

Commit the complete Chapter N transaction to `main`, then re-fetch `MANUSCRIPT_STATE.md` and Chapter N from `main` before starting N+1.

---

### Task 5: Write Chapter 500 and evaluate the forward system

**Files:**
- Create: `state/manuscript/Peg_Leg_Greg_Chapter_500_EXACT_WIP.md`
- Modify: `state/MANUSCRIPT_STATE.md`
- Modify: `state/editorial/rehearsal/forward/proving-run-493-500.json`
- Create: `state/editorial/rehearsal/FORWARD_PROVING_RUN_493_500.md`
- Modify if graduating: `state/MANUSCRIPT_WORKFLOW.md`
- Modify only when materially changed: `state/OPEN_THREADS.md`

**Interfaces:**
- Consumes: accumulated 493-499 proving-run evidence.
- Produces: Chapter 500 plus an explicit decision to graduate, simplify, or stop the workflow.

- [ ] **Step 1: Produce Chapter 500 through the same loop**

Do not make Chapter 500 artificially climactic merely because it is the evaluation boundary.

- [ ] **Step 2: Complete the eight system questions**

Evaluate scene selection, character surprise, protagonist gravity, PERFORMANCE value, memory value, throughput, rejected-option value, and state cleanliness.

- [ ] **Step 3: Write the proving-run report**

Include chapter-by-chapter rehearsal depth, PERFORMANCE calls, notable discoveries, prose deviations from rehearsal, failures, and overall recommendation.

- [ ] **Step 4: Graduate only if evidence is positive**

If the loop improved story choice without unacceptable overhead, remove proving-run-only wording and make pre-prose REHEARSAL the permanent default in `MANUSCRIPT_WORKFLOW.md`. Keep PERFORMANCE optional. If overhead dominated, simplify the contract instead of adding machinery.

- [ ] **Step 5: Verify the final Chapter 500 authority**

Re-read current main, confirm Chapter 500 endpoint, durable next trailhead, updated live threads, and final proving-run status.

- [ ] **Step 6: Commit the evaluation/graduation transaction**

Commit message should identify the Chapter 500 proving-run conclusion.
