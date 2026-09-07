# PLG Outward 4D Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a derived-only PLG experiment that uses accepted Chapters 1-500 as evidence to explore constrained pre-Chapter-1 histories and post-Chapter-500 futures, then tests a high-value bidirectional collision without canon writes.

**Architecture:** Extend the existing generic temporal/REHEARSAL compiler only where a generic seam is missing. Keep PLG-specific evidence, old-life candidates, future candidates, collisions, and results project-local under a new experiment directory. The known manuscript remains sole story authority; outward state is derived and explicitly capped below canon.

**Tech Stack:** Python 3, existing `scripts/persistent_act_runtime.py`, `scripts/story_sync_engine.py`, `scripts/plg_ai_tools.py`, JSON/Markdown experiment state, unittest/pytest as already used by the repository.

**Spec:** `docs/superpowers/specs/2026-09-07-plg-outward-4d-design.md`

## Global Constraints

- Accepted PLG canon prose remains sole story authority.
- No old-life or future candidate may automatically become canon.
- No rewrite of Chapters 1-500 in this plan.
- Creative search may be wild; epistemic status must remain explicit.
- Preserve provenance to canon evidence.
- Constraint generally weakens and uncertainty increases with temporal distance.
- REHEARSAL chooses the cheapest discriminating representation.
- PERFORMANCE is optional and evidence-triggered.
- Keep PLG-specific state out of generic compiler code.
- Do not add new visible cognitive UI or unrelated cognitive features.

---

### Task 1: Lock generic outward-temporal contracts

**Files:**
- Modify only if required: `scripts/persistent_act_runtime.py`
- Test: existing persistent-runtime test module plus a focused outward-temporal contract test file following repository naming conventions.

**Interfaces:**
- Consumes: existing temporal coordinates, forward consequences, backward requirements, REHEARSAL target/fidelity contracts, derived-only state.
- Produces: a generic way to represent temporal regions outside an observed evidence interval without granting them canon authority.

- [ ] **Step 1: Read the current runtime and tests at branch head**

Confirm whether arbitrary pre-observation/post-observation temporal coordinates and derived authority ceilings already exist. Do not implement a second abstraction if the current runtime can express the experiment unchanged.

- [ ] **Step 2: Write the smallest failing contract only if a seam is actually missing**

The contract must prove that an outward temporal candidate can carry: direction (`past`/`future`), temporal distance, evidence status, provenance, forward/backward messages, and a derived-only authority ceiling.

- [ ] **Step 3: Run the focused test and confirm RED**

Run the repository's existing focused Python test command for the selected module. Expected: failure only for the missing outward contract, not unrelated architecture.

- [ ] **Step 4: Implement the minimum generic seam**

Reuse existing temporal structures. Do not add PLG names, Greg, Chapter 500, old-life occupations, or future plot assumptions to generic code.

- [ ] **Step 5: Run focused runtime tests**

Expected: all focused temporal/REHEARSAL contracts pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/persistent_act_runtime.py tests/
git commit -m "Support derived outward temporal candidates"
```

If Step 1 proves no generic code is needed, record that finding in the experiment state and skip the code commit.

---

### Task 2: Build the PLG canon evidence compiler

**Files:**
- Create: `state/experiments/plg-outward-4d/CURRENT.md`
- Create: `state/experiments/plg-outward-4d/CURRENT.json`
- Create: `state/experiments/plg-outward-4d/evidence-ledger.json`
- Modify: `scripts/plg_ai_tools.py` only if the existing compile/retrieval surface cannot produce the needed bounded evidence packet.
- Test: focused PLG AI-tools test following repository conventions if tooling changes.

**Interfaces:**
- Consumes: accepted manuscript authority through Chapter 500, current project/manuscript state, exact chapter retrieval surfaces.
- Produces: compact longitudinal evidence grouped by persistent thread with exact provenance pointers and no invented prehistory/future claims.

- [ ] **Step 1: Verify exact Chapter 1-500 authority and retrieval paths**

Read current `state/MANUSCRIPT_STATE.md`, chapter index/checkpoints, and existing `plg_ai_tools` retrieval/compiler interfaces. Do not reconstruct exact prose from summaries.

- [ ] **Step 2: Define the project-local evidence ledger schema**

Each evidence item must include at minimum: `id`, `thread`, `observation`, `evidence_kind`, `chapter_or_range`, `source_pointer`, `confidence`, and `notes`. Evidence kinds must distinguish explicit canon fact from interpretation.

- [ ] **Step 3: Compile longitudinal thread evidence**

Cover identity, capability/work, body, money/status, authority, violence/risk, intimacy/dependence, home/belonging, major relationships, social obligations, failure/loss/avoidance, and reputation when supported. Add or remove thread families based on actual manuscript evidence rather than forcing empty categories.

- [ ] **Step 4: Validate provenance and compression**

Spot-check ledger claims against exact canon. The ledger must be substantially smaller than the manuscript and must not replace exact prose authority.

- [ ] **Step 5: Commit evidence state**

```bash
git add state/experiments/plg-outward-4d scripts/plg_ai_tools.py tests/
git commit -m "Compile PLG outward temporal evidence"
```

---

### Task 3: Generate competing old-life candidates

**Files:**
- Create: `state/experiments/plg-outward-4d/past-candidates.json`
- Update: `state/experiments/plg-outward-4d/CURRENT.json`

**Interfaces:**
- Consumes: `evidence-ledger.json`.
- Produces: multiple structurally distinct pre-Chapter-1 trajectories at near and distant temporal coordinates.

- [ ] **Step 1: Generate a wide candidate population**

Permit invented relationships, careers, places, institutions, failures, loves, enemies, obligations, and losses. Include at least one deliberately surprising distant candidate and an `unknown-other` escape hatch.

- [ ] **Step 2: Type every candidate epistemically**

Use only the statuses from the approved spec. No invented event may be labeled `CANON_FACT` without explicit canon evidence.

- [ ] **Step 3: Attach explanatory predictions**

For each serious candidate, record which independent canon observations it explains, what residue it predicts should exist in Chapters 1-500, what would contradict it, and what transformation would be required where it conflicts with repeated Greg behavior.

- [ ] **Step 4: Remove semantic cousins, not diversity**

Cluster candidates that are the same mechanism with cosmetic changes. Preserve genuinely different causal histories.

- [ ] **Step 5: Commit**

```bash
git add state/experiments/plg-outward-4d/past-candidates.json state/experiments/plg-outward-4d/CURRENT.json
git commit -m "Explore PLG old-life temporal candidates"
```

---

### Task 4: Generate competing post-500 futures

**Files:**
- Create: `state/experiments/plg-outward-4d/future-candidates.json`
- Update: `state/experiments/plg-outward-4d/CURRENT.json`

**Interfaces:**
- Consumes: Chapter-500 authority plus `evidence-ledger.json`.
- Produces: multiple structurally distinct near and distant future trajectories.

- [ ] **Step 1: Lock Chapter-500 constraints before invention**

Preserve current chronology, Duskport temporary-resident state, Hark & Venn timing/body state, acquisition latency, Lyssa's independent Carrow life, economic state, Lakeward silence, and any newer main authority if main has advanced before execution.

- [ ] **Step 2: Generate near-future candidates**

These should be tightly constrained and should not schedule every unresolved lane.

- [ ] **Step 3: Generate distant-future candidates**

Push divergence. Include multiple different future Gregs and at least one surprising candidate not reducible to current plot lanes.

- [ ] **Step 4: Record prerequisites and falsifiers**

Each serious future candidate must state what current/near-future transformations it requires, which are already evidenced, which are missing, and what canon behavior would make the future false-character or implausibly expensive.

- [ ] **Step 5: Commit**

```bash
git add state/experiments/plg-outward-4d/future-candidates.json state/experiments/plg-outward-4d/CURRENT.json
git commit -m "Explore PLG post-500 temporal candidates"
```

---

### Task 5: Force bidirectional collision and REHEARSAL

**Files:**
- Create: `state/experiments/plg-outward-4d/collisions.json`
- Create: `state/experiments/plg-outward-4d/rehearsal-evidence.json`
- Update: `state/experiments/plg-outward-4d/CURRENT.json`

**Interfaces:**
- Consumes: past/future candidate populations and evidence ledger.
- Produces: ranked collisions and one bounded discriminating experiment result.

- [ ] **Step 1: Build cross-direction collisions**

At minimum include one future candidate that raises a question about old Greg and one old-life candidate that materially changes the cost/meaning of a future state.

- [ ] **Step 2: Rank by information value**

Prefer collisions that separate multiple live candidates, affect character truth or long-range trajectory, and can be tested cheaply against existing canon evidence.

- [ ] **Step 3: Select the cheapest useful REHEARSAL mode**

Start with a probe/state/trajectory/backward-forward test. Escalate to PERFORMANCE only if embodied behavior is the unresolved variable.

- [ ] **Step 4: Run one bounded rehearsal**

Record inputs, tested uncertainty, evidence, strengthened/weakened/rejected candidates, unresolved alternatives, and provenance. Preserve a rejection if evidence earns one.

- [ ] **Step 5: Reduce full trace to compact evidence**

Keep full artifact only if it qualifies as useful case law. Otherwise retain compact discovery plus provenance.

- [ ] **Step 6: Commit**

```bash
git add state/experiments/plg-outward-4d/collisions.json state/experiments/plg-outward-4d/rehearsal-evidence.json state/experiments/plg-outward-4d/CURRENT.json
git commit -m "Rehearse PLG outward temporal collision"
```

---

### Task 6: STORY SYNC evaluation and experiment checkpoint

**Files:**
- Create: `state/experiments/plg-outward-4d/EVALUATION.md`
- Update: `state/experiments/plg-outward-4d/CURRENT.md`
- Update: `state/experiments/plg-outward-4d/CURRENT.json`

**Interfaces:**
- Consumes: all experiment evidence.
- Produces: derived-only convergence state, rejected hypotheses, capability findings, and exact next edge.

- [ ] **Step 1: Evaluate candidates through STORY SYNC rules**

Score independent recurrence, explanatory reach, forward/backward agreement, character truth, contradiction, retrofit cost, causal reach, dramatic usefulness, predicted residue, and hidden-fact dependence.

- [ ] **Step 2: Enforce authority ceiling**

Even strongest surviving history/future remains derived. Verify zero manuscript/canon writes.

- [ ] **Step 3: Evaluate the architecture, not just the story ideas**

Record whether the 500-chapter middle materially constrained both directions, whether a surprising candidate survived, whether an attractive candidate died/weakened, whether temporal distance behaved usefully, and whether REHEARSAL selected an appropriately cheap test.

- [ ] **Step 4: Write exact next edge**

Choose among: another outward epoch, deeper evidence retrieval for a contested thread, selective PERFORMANCE, or freeze outward state and prepare a separately approved rewrite/recomposition experiment. Do not automatically choose rewrite.

- [ ] **Step 5: Run full relevant verification**

Run focused story-compiler/runtime/PLG tool tests plus the repository's normal full CI/test command available on the branch. Record exact counts and failures; do not claim green without evidence.

- [ ] **Step 6: Commit**

```bash
git add state/experiments/plg-outward-4d/EVALUATION.md state/experiments/plg-outward-4d/CURRENT.md state/experiments/plg-outward-4d/CURRENT.json
git commit -m "Evaluate PLG outward 4D proving run"
```
