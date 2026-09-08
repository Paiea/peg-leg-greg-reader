# Persistent Four-Act Convergence Implementation Plan

**Goal:** preserve four always-present act-local search channels while adding a conservative shared story layer for bidirectional constraint exchange, targeted REHEARSAL, and evidence-based convergence.

**Architecture:** keep ACT I–IV as persistent local speculative states. Add shared Story IR as the only cross-act communication surface. Local states may invent freely; shared state accepts only explicit promoted constraints/discoveries. Scheduling guarantees nonzero baseline search for all acts and allocates bonus attention to high-value cross-act pressure.

**Spec:** `docs/superpowers/specs/2026-09-07-persistent-four-act-convergence-design.md`

## Task 1: Persistent topology contracts

**Files:**
- Modify: `tests/test_story_sync_engine.py`
- Modify: `scripts/story_sync_engine.py`

Test first that:

- exactly ACT I–IV are represented as persistent channels for this experiment
- every channel keeps local possibilities and unresolved questions independently
- local ideas are not automatically copied into Shared Story State
- missing/duplicate act channels are rejected

## Task 2: Bidirectional cross-act constraints

**Files:**
- Modify: `tests/test_story_sync_engine.py`
- Modify: `scripts/story_sync_engine.py`

Add explicit records for:

- forward consequence: source act -> target later act
- backward requirement: source later act -> target earlier act
- closure status / contradiction status

Test that a backward requirement is reported to the earlier act without mutating its local state or becoming story truth automatically.

## Task 3: Persistent scheduler

**Files:**
- Modify: `tests/test_story_sync_engine.py`
- Modify: `scripts/story_sync_engine.py`

Add deterministic scheduling output with:

- baseline allocation for ACT I–IV every cycle
- bonus heat for major contradictions
- bonus heat for forward/backward collisions
- bonus heat for major relationship transitions
- bonus heat for book-shaping discoveries
- bonus heat for important REHEARSAL uncertainty
- bonus heat for strongly supported candidate endings

Test that no act receives zero opportunity, including late convergence.

## Task 4: STORY SYNC integration

**Files:**
- Modify: `scripts/story_sync_engine.py`
- Modify: `scripts/plg_ai_tools.py`
- Modify: `tests/test_story_sync_creator_taste.py`
- Modify: `tests/test_plg_ai_tools.py`

Keep existing discovery promotion, branch viability, hidden canon, and reader-gap logic intact.

Creator taste may affect extra search priority only. It must not alter baseline per-act allocation or branch/canon authority.

## Task 5: Dragon Spotter bounded trial

**Files:**
- Modify/add under: `state/experiments/dragon-spotter/story-sync/`
- Modify: `tests/test_dragon_spotter_story_sync_trial.py`

Represent four persistent act-local states and at least one real bidirectional collision:

- ACT IV proposes a late payoff
- emits backward requirement to ACT I/II
- earlier act local state does not automatically accept it
- STORY SYNC reports the collision and assigns extra rehearsal/search heat

## Task 6: Verification

Run:

`python -m unittest tests.test_story_sync_engine tests.test_story_sync_creator_taste tests.test_story_sync_rehearsal_bridge tests.test_story_sync_report_evidence tests.test_plg_ai_tools tests.test_dragon_spotter_story_sync_trial`

Then:

`python -m unittest discover -s tests -p 'test_*.py'`

Require final PR-head CI green before claiming completion. Leave PR #161 draft/unmerged unless separately authorized.
