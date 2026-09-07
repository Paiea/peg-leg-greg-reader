# AI-Native Long-Form Rendering Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn a converged derived story state into an autonomous candidate-prose pipeline that can render, diagnose, targeted-reprompt, compare, retain, advance, and route genuine story gaps back to REHEARSAL without granting prose canon authority.

**Architecture:** Add one generic derived-only rendering orchestrator downstream of STORY SYNC. It does not call a particular model itself; it compiles render/evaluation/reprompt packets and reduces returned attempts deterministically, so any executor can supply model outputs. Rendering memory is separate from STORY STATE. Only genuine causal gaps escape to REHEARSAL. Forward motion is budgeted so local polish cannot consume an overnight novel run.

**Tech Stack:** Python stdlib, existing `plg_ai_tools.py` JSON tool surface, unittest/GitHub Actions.

**Spec:** `state/experiments/dragon-spotter/persistent-act-runtime/CURRENT.md`

## Global Constraints

- Generic compiler changes remain project-agnostic.
- Dragon-specific rendering evidence remains under `state/experiments/dragon-spotter/`.
- Candidate prose is derived-only and never canon-writing authority.
- `apply_survivors` remains the only canon-writing `plg_ai_tools` surface.
- Preserve exactly four persistent temporal act channels upstream.
- Preserve concurrent Gravity work.
- Reprompt prose failures locally; route only genuine story/causal gaps to REHEARSAL.
- Prefer forward motion: ordinary intervals receive at most one targeted reprompt by default; high-value intervals may explicitly receive a larger budget.
- No automatic sustained prose generation is introduced by the orchestrator itself.

---

### Update 1: Rendering packet and authority boundary

**Files:**
- Create: `tests/test_long_form_rendering_loop.py`
- Create: `scripts/long_form_rendering_loop.py`

**Produces:** `compile_render_packet(...)` with state-in/out, reader state, relevant truths/threads/case law, unresolved renderer choices, and explicit derived-only authority.

- [ ] Write RED contract tests.
- [ ] Verify missing module/function fails.
- [ ] Implement minimal packet compiler.
- [ ] Verify focused tests green.

### Update 2: Failure diagnosis and targeted reprompt

**Files:**
- Modify: `tests/test_long_form_rendering_loop.py`
- Modify: `scripts/long_form_rendering_loop.py`

**Produces:** deterministic failure classes `accept`, `prose`, `performance`, `continuity`, `story`; `build_reprompt_packet(...)`; story failures are never papered over with prose reprompting.

- [ ] Add RED diagnosis/reprompt tests.
- [ ] Verify RED.
- [ ] Implement smallest diagnosis and reprompt reducer.
- [ ] Verify focused tests green.

### Update 3: Candidate comparison, retention, and rendering memory

**Files:**
- Modify: `tests/test_long_form_rendering_loop.py`
- Modify: `scripts/long_form_rendering_loop.py`

**Produces:** `compare_candidates(...)` and `retain_candidate(...)`. Retained candidate records why it won and compact renderer lessons, but cannot mutate STORY SYNC discovery maturity.

- [ ] Add RED comparison/memory tests.
- [ ] Verify RED.
- [ ] Implement deterministic ranking and compact memory.
- [ ] Verify focused tests green.

### Update 4: Forward-motion budget and advancement

**Files:**
- Modify: `tests/test_long_form_rendering_loop.py`
- Modify: `scripts/long_form_rendering_loop.py`

**Produces:** `advance_rendering_run(...)` with interval ledger, state-out propagation, bounded attempts, and minimal invalidation. Acceptable prose advances instead of endlessly polishing.

- [ ] Add RED advancement/budget tests.
- [ ] Verify RED.
- [ ] Implement bounded advancement.
- [ ] Verify focused tests green.

### Update 5: Public derived-only execution seam and Dragon proving packet

**Files:**
- Modify: `tests/test_long_form_rendering_loop.py`
- Modify: `scripts/plg_ai_tools.py`
- Create: `state/experiments/dragon-spotter/rendering/first-dragon-bargain-input.json`
- Update: `state/experiments/dragon-spotter/persistent-act-runtime/CURRENT.md`
- Update: `state/experiments/dragon-spotter/persistent-act-runtime/CURRENT.json`

**Produces:** `plg_ai_tools.run_story_rendering_cycle`, which accepts executor-supplied candidate/evaluation returns, never writes canon, and returns either `advance`, `reprompt`, `performance_rehearsal`, `story_rehearsal`, or `complete`. Dragon packet proves the first bounded interval can enter the renderer without resolving land/relic or canonizing gift/title choices.

- [ ] Add RED public-seam test.
- [ ] Verify RED.
- [ ] Wire minimal public seam.
- [ ] Add Dragon project-local proving input.
- [ ] Run focused validation and full repository suite.
- [ ] Update Dragon CURRENT with observed authority and next edge.
