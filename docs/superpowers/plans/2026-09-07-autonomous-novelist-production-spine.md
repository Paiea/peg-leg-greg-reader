# Autonomous Novelist Production Spine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and test-driven-development task-by-task. This branch is operated through the GitHub connector rather than a local worktree, so every write must re-read moving authority and use GitHub contents SHA guardrails where applicable.

**Goal:** Extend the settled four-act / REHEARSAL / PERFORMANCE / STORY SYNC architecture into an AI-native production spine that can spend disposable compute on speculative search, render locally stable regions in parallel, preserve dependency provenance, survive worker/context death, and advance toward a complete derived manuscript without granting prose canon authority.

**Architecture:** Keep STORY STATE and STORY SYNC as conservative persistent authority layers. Add small deterministic reducers around them: DREAM search for disposable speculative populations, RENDERABILITY for local prose gates and dependency versions, richer rendering reduction for diagnosis/reprompt/prose discoveries, and an EPOCH ORCHESTRATOR that schedules bounded jobs from immutable snapshots and emits hot-start continuation packets. Model workers remain external disposable executors; reducers compile packets and integrate only derived evidence.

**Tech Stack:** Python stdlib, existing `persistent_act_runtime.py`, `story_rehearsal_orchestrator.py`, `story_sync_engine.py`, `long_form_rendering_loop.py`, `plg_ai_tools.py`, unittest, GitHub Actions.

**Specs:**
- `docs/superpowers/specs/2026-09-07-dream-form-search-design.md`
- user-approved autonomous-novelist production direction in PR #161 development history

## Global Constraints

- Preserve STORY STATE = memory, ACT I-IV = persistent temporal perspectives, REHEARSAL, PERFORMANCE, STORY SYNC, and downstream PROSE roles.
- DREAM may speculate aggressively but has no story or canon authority.
- Nothing moves directly from DREAM or prose into STORY STATE.
- `apply_survivors` remains the only canon-writing `plg_ai_tools` surface.
- Generic compiler code contains no Dragon Spotter or Gravity's Embrace story assumptions.
- Project-specific fixtures remain under their project experiment roots.
- Preserve concurrent Gravity work and validate its existing fixtures after generic changes.
- No global current chapter. New scheduling is dependency/frontier driven.
- Workers consume immutable snapshot versions and emit proposed derived deltas/evidence.
- Bounded compute budgets and stop conditions are mandatory.
- Context death must lose at most active disposable work, not durable integrated state.
- Do not claim autonomous overnight novel completion until an end-to-end model-driven proving run actually produces one.

---

### Update 1: DREAM search, novelty pressure, mutation provenance, and FORM shifts

**Files:**
- Create: `tests/test_story_sync_dream_search.py`
- Create: `scripts/dream_search_engine.py`

**Interfaces:**
- `build_candidate(...)` -> `dream_candidate/v1`, authority `none`, canon write false.
- `candidate_value(candidate)` -> transparent `surprise * causality * reach` base plus bounded novelty/form-information bonuses.
- `conceptual_similarity(a, b)` -> deterministic overlap over worker-supplied concept keys.
- `select_diverse_survivors(candidates, limit=...)` -> cheap-causal-pass, diversity-preserving survivors plus rejected/suppressed provenance.
- `mutate_candidate(...)`, `cross_candidates(...)`, `shift_form(...)` -> new derived candidates with parent provenance.
- `compile_rehearsal_probe(candidate)` -> derived rehearsal question only, never discovery maturity.

- [ ] Write RED tests for authority isolation, causal kill, dense-cluster suppression, form diversity, mutation/crossover provenance, and rehearsal bridge authority.
- [ ] Verify RED in GitHub Actions full suite.
- [ ] Implement minimum deterministic reducer.
- [ ] Verify focused/full suite GREEN.

### Update 2: Local RENDERABILITY and dependency/staleness tracking

**Files:**
- Create: `tests/test_story_sync_renderability.py`
- Create: `scripts/story_renderability.py`

**Interfaces:**
- `assess_renderability(region)` -> `renderability_report/v1` with renderable/blocked, reasons, dependency snapshot, and safe prose-discovery uncertainty.
- Required local signals: state-in stability, required dramatic movement, character-state availability, incoming dependency stability, invalidation risks.
- `capture_dependencies(region)` -> exact `{dependency_id: version}` mapping.
- `assess_staleness(candidate_dependencies, current_versions)` -> stale only when a dependency actually used by the candidate changed.
- Whole-novel convergence is explicitly not required.

- [ ] Write RED tests proving locally stable early regions render while unrelated later uncertainty remains open.
- [ ] Prove high-probability invalidation blocks rendering and prose-safe uncertainty does not.
- [ ] Prove unrelated story-state version changes do not stale a candidate.
- [ ] Implement minimum reducer and verify GREEN.

### Update 3: Parallel rendering evidence, actionable diagnosis, and PROSE_DISCOVERY

**Files:**
- Create: `tests/test_story_sync_rendering_pipeline.py`
- Modify: `scripts/long_form_rendering_loop.py`

**Interfaces:**
- Preserve all existing rendering APIs for compatibility.
- Add independent interval job/reduction surfaces so epoch scheduling is not cursor-bound.
- Evaluation contract exposes `survives`, `fails`, `uncertain`, and `future_repair_obligations` in addition to compatibility fields.
- Directed reprompt packets lock surviving dependencies and alter only diagnosed failure scope.
- Candidate comparison prefers contract survival and explicit dimensions over vague scalar quality.
- `extract_prose_discoveries(...)` returns derived `prose_discovery/v1` proposals with evidence provenance; no direct STORY SYNC maturity mutation.
- Losing candidates may contribute explicitly marked useful evidence without becoming retained prose.

- [ ] Write RED tests for independent interval jobs, actionable diagnosis, dependency locks, useful loser evidence, and prose-discovery authority.
- [ ] Verify RED.
- [ ] Implement minimum extension without removing existing sequential compatibility path.
- [ ] Verify GREEN.

### Update 4: EPOCH ORCHESTRATOR and hot-start relay state

**Files:**
- Create: `tests/test_story_sync_epoch_orchestrator.py`
- Create: `scripts/story_epoch_orchestrator.py`

**Interfaces:**
- `plan_epoch(snapshot, *, budget_units)` -> bounded `story_epoch_plan/v1`.
- Lanes: `dream`, `rehearsal`, `performance`, `story_sync`, `render`, `evaluate`, `reprompt`, `compare`, `stale_repair`.
- Task priority considers information gain, uncertainty reduction, downstream reach, novelty, dramatic importance, render readiness, staleness, and expected cost.
- Tasks carry exact snapshot version, cost cap, stop conditions, and target id.
- Four persistent act channels retain nonzero baseline search opportunity when budget permits.
- `reduce_epoch_results(...)` records completed derived deltas/evidence and queues integration, but does not bypass STORY SYNC.
- `compile_hot_start(...)` / `compile_next_epoch_packet(...)` emit compact continuation state: epoch, story version, phase, high-value targets, renderable/blocked/stale regions, queues, contradictions, convergence, budget allocation, continuation hint, and explicit do-not-revisit list.

- [ ] Write RED tests for phase-sensitive allocation, bounded total cost, snapshot immutability, four-act baseline, stale-repair priority, and useful next-worker packet after partial completion.
- [ ] Verify RED.
- [ ] Implement deterministic scheduler/reducer.
- [ ] Verify GREEN.

### Update 5: Public execution seams, project-local proving fixtures, CI, and trailhead

**Files:**
- Modify: `tests/test_plg_ai_tools.py`
- Modify: `scripts/plg_ai_tools.py`
- Modify: `.github/workflows/story-sync-validation.yml`
- Create project-local Dragon Spotter DREAM/renderability/epoch fixture(s) under `state/experiments/dragon-spotter/`
- Modify Dragon `CURRENT.md` / `CURRENT.json` only after observed verification.
- Modify generic `state/story-compiler/CURRENT.md` / `CURRENT.json` only after observed verification.

**Interfaces:**
- Derived-only public seams for DREAM reduction, renderability/staleness, and epoch planning/reduction.
- Every new public seam has `write: false`; only `apply_survivors` remains `write: true`.
- Dragon proves: bounded first-bargain DREAM cloud, duplicate suppression, at least one FORM shift, local renderability, dependency capture, parallel rendering packet creation, and hot-start next-epoch output without reopening broad discovery or canonizing choices.
- Gravity existing fixtures must remain green; do not edit Gravity project state unless an actual generic compatibility defect requires a project-local fixture correction.

- [ ] Add RED public-tool metadata/delegation tests.
- [ ] Implement adapters.
- [ ] Extend CI focused paths/tests.
- [ ] Add Dragon proving fixture and observations.
- [ ] Run focused and full repository suites at final head.
- [ ] Confirm PR #161 remains open, draft, and unmerged.

## Completion Gate

This plan is complete when the repository can deterministically orchestrate disposable speculative/model work into durable derived state across repeated short-lived epochs, locally render stable regions without waiting for global convergence, stale only affected prose, and emit continuation packets that let a fresh worker resume immediately. A complete autonomous novel remains a separate empirical proving run, not an implementation claim.
