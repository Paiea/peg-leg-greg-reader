# Autonomous REHEARSAL Campaign Queue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a resumable serial campaign queue that lets an authorized Codex worker rehearse canon 061-491 in ten-chapter batches and route surviving prose only through the existing validated REHEARSAL return path.

**Architecture:** A deterministic queue-state module owns batch ordering, resume semantics, settled-authority checks, and advancement. A Codex campaign instruction artifact supplies the approved creative worker contract. GitHub Actions validates and applies one completed batch at a time; it never performs creative inference itself and never advances past a blocked batch.

**Tech Stack:** Python 3.12, JSON state/manifests, GitHub Actions, existing `scripts/apply_rehearsal_returns.py`, existing PLG validation scripts.

**Spec:** `docs/superpowers/specs/2026-09-07-rehearsal-autonomous-campaign-queue-design.md`

## Global Constraints

- Canon prose remains the only story authority.
- Queue range is canon 061-491, batch size 10 except final 491.
- Batches are serial and read settled authority from the preceding batch.
- No edit quota; SOURCE WIN is valid.
- Boundary-hunt heat remains the 051-060 calibration unless separately changed by editorial authority.
- Creative workers never write chapter prose directly.
- Exact source means literal current HTML; no fuzzy matching.
- Canon writes are serialized through `scripts/apply_rehearsal_returns.py`.
- `speaker_legibility` and `relationship_behavior` are not writable surfaces.
- Canon Kellan must not be conflated with the synthetic Jorren actor.
- One ordinary worker retry maximum.
- Any hard-lock, exact-source, authority, or repository-validation failure blocks the queue.

---

### Task 1: Deterministic queue state and batch ordering

**Files:**
- Create: `scripts/rehearsal_campaign_queue.py`
- Create: `tests/test_rehearsal_campaign_queue.py`
- Create: `state/editorial/rehearsal/queue/canon-061-491.json`

**Interfaces:**
- Produces: `build_batches(start: int, end: int, batch_size: int) -> list[tuple[int,int]]`
- Produces: `next_batch(state: dict) -> dict | None`
- Produces: `validate_state(state: dict) -> None`
- Produces: CLI commands `status`, `claim`, `settle`, and `block` operating on the queue JSON.

- [ ] **Step 1: Write failing tests** for exact batch sequence `061-070 ... 481-490, 491-491`, first-pending selection, refusal to skip blocked/running batches, and invalid settled-authority state.
- [ ] **Step 2: Run** `python -m unittest tests.test_rehearsal_campaign_queue -v` and verify RED for missing module/functions.
- [ ] **Step 3: Implement minimal queue module** with strict schema validation and atomic JSON rewrite.
- [ ] **Step 4: Run focused tests** and verify GREEN.
- [ ] **Step 5: Commit** queue module, tests, and initialized queue state.

### Task 2: Authority-safe claim and settlement transitions

**Files:**
- Modify: `scripts/rehearsal_campaign_queue.py`
- Modify: `tests/test_rehearsal_campaign_queue.py`

**Interfaces:**
- Consumes: current branch HEAD supplied to CLI.
- Produces: claim record with `source_authority`, `batch_start`, `batch_end`, `retry_count`.
- Produces: settled record with `result` in `applied|source_win`, `settled_authority`, manifest/report paths, and validation result.

- [ ] **Step 1: Add failing tests** proving a claim records the current SHA, a settle refuses a different source authority unless it is the expected post-apply authority, retry count cannot exceed one, and a blocked batch prevents later claims.
- [ ] **Step 2: Run focused tests** and verify the new tests fail for the intended transition errors.
- [ ] **Step 3: Implement transition guards** without adding any creative/editorial logic.
- [ ] **Step 4: Run focused tests** and full existing queue tests GREEN.
- [ ] **Step 5: Commit** authority transition support.

### Task 3: Codex REHEARSAL worker contract

**Files:**
- Create: `state/editorial/rehearsal/queue/CODEX_REHEARSAL_CAMPAIGN.md`
- Create: `state/editorial/rehearsal/queue/worker-result.schema.json`
- Create: `tests/test_rehearsal_campaign_worker_schema.py`

**Interfaces:**
- Consumes: claimed batch, exact chapter HTML, fresh derived evidence, actor/relationship memory, approved design spec.
- Produces: compact worker result containing source wins, discoveries, rejected-too-hot evidence, and zero-or-more prose return candidates.

- [ ] **Step 1: Write failing schema tests** requiring batch/source authority, per-chapter disposition, rejected-hot labels, and exact candidate `before`/`after` prose while rejecting hard surfaces and invalid writable surfaces.
- [ ] **Step 2: Run** `python -m unittest tests.test_rehearsal_campaign_worker_schema -v` and verify RED because schema/validator is absent.
- [ ] **Step 3: Add the schema and worker contract** reproducing the approved heat, actor-entrance rule, repetition rule, Kellan namespace warning, and no-direct-prose-write rule.
- [ ] **Step 4: Run schema tests GREEN.**
- [ ] **Step 5: Commit** worker contract and schema.

### Task 4: Deterministic worker-result to return-manifest compiler

**Files:**
- Create: `scripts/compile_rehearsal_campaign_returns.py`
- Create: `tests/test_compile_rehearsal_campaign_returns.py`

**Interfaces:**
- Consumes: one schema-valid worker result plus literal current `chapters/NNN.html` files.
- Produces: `rehearsal_free_returns/v1` manifest or an explicit SOURCE-WIN marker when no prose candidates survive.

- [ ] **Step 1: Write failing tests** proving literal HTML anchors are required, semantic/rendered paragraph hallucinations fail, zero candidates produce SOURCE WIN, invalid writable surfaces fail, and chapter range cannot escape the claimed batch.
- [ ] **Step 2: Run focused tests** and verify RED.
- [ ] **Step 3: Implement compiler** using literal file reads and exact substring counts only; no fuzzy matching.
- [ ] **Step 4: Run focused tests GREEN** plus `python -m unittest tests.test_apply_rehearsal_returns -v`.
- [ ] **Step 5: Commit** compiler.

### Task 5: One-batch serialized integration workflow

**Files:**
- Create: `.github/workflows/rehearsal-campaign-queue.yml`
- Create: `tests/test_rehearsal_campaign_workflow_contract.py`

**Interfaces:**
- Consumes: a completed worker-result artifact for the currently claimed batch.
- Produces: validated prose commit or SOURCE-WIN settlement, then advances queue state exactly one batch.

- [ ] **Step 1: Write failing workflow-contract tests** checking concurrency serialization, queue-state validation, exact-source compilation before apply, existing apply runner use, hard-surface/no-em-dash checks, unit/PERFORMANCE/Showcase validation, and no advancement on failure.
- [ ] **Step 2: Run focused test** and verify RED because workflow is absent.
- [ ] **Step 3: Add workflow** with `concurrency` preventing parallel canon writes and a single-batch settlement boundary.
- [ ] **Step 4: Run workflow-contract tests GREEN** and repository workflow/static checks.
- [ ] **Step 5: Commit** integration workflow.

### Task 6: Codex campaign handoff and resume instructions

**Files:**
- Modify: `state/editorial/rehearsal/queue/CODEX_REHEARSAL_CAMPAIGN.md`
- Create: `state/editorial/rehearsal/queue/README.md`
- Modify: `AGENTS.md` only if the existing Codex policy requires a discoverability pointer.

**Interfaces:**
- Produces: a single durable instruction surface an authorized Codex session can execute repeatedly without chat reconstruction.

- [ ] **Step 1: Write failing discoverability test** if AGENTS/policy conventions provide a machine-readable campaign pointer; otherwise add a focused file-presence/content test.
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Document start/resume/blocked behavior**, including the rule that the worker must stop after one failed retry and must never skip a blocked batch.
- [ ] **Step 4: Run focused tests GREEN.**
- [ ] **Step 5: Commit** handoff documentation.

### Task 7: End-to-end dry simulation and repository verification

**Files:**
- Modify only test fixtures if needed; do not touch canon prose during the simulation.

**Interfaces:**
- Demonstrates: pending -> claim -> SOURCE WIN settle -> next claim; pending -> claim -> manifest compile -> mocked/dry exact application boundary -> settle; and blocked -> halt.

- [ ] **Step 1: Add an end-to-end test fixture** covering one SOURCE-WIN batch, one prose-candidate batch, and one blocked batch.
- [ ] **Step 2: Run the test and verify RED** before fixture-support changes.
- [ ] **Step 3: Add only minimal support needed** for the dry simulation.
- [ ] **Step 4: Run** `python -m unittest discover -s tests -p 'test_*.py'`, `python scripts/performance_roundtrip_references.py --check`, `python scripts/project_check.py showcase`, and `git diff --check` and require all GREEN.
- [ ] **Step 5: Commit** final verified queue implementation.

### Task 8: Start campaign at canon 061 only after 051-060 settles

**Files:**
- Update: `state/editorial/rehearsal/queue/canon-061-491.json`

**Interfaces:**
- Consumes: final settled authority after the current 051-060 boundary-hunt workflow.
- Produces: first claim for 061-070 against that exact authority.

- [ ] **Step 1: Verify 051-060 workflow/report is green and prose commit exists, or record SOURCE WIN if that campaign ultimately produces none.**
- [ ] **Step 2: Run full repository validation on the settled 051-060 authority.**
- [ ] **Step 3: Claim 061-070 using that exact settled SHA.**
- [ ] **Step 4: Start the authorized Codex worker for only the claimed batch.**
- [ ] **Step 5: Verify the queue reports 061-070 running and all later batches pending; do not claim 071-080 yet.**
