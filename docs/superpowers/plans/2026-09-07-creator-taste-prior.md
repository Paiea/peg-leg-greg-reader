# Creator Taste Prior Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, evidence-backed creator-taste prior that changes long-form search/rehearsal priority without becoming story authority.

**Architecture:** Add one focused `creator_taste_prior.py` module for schemas, validation, evidence append/rebuild, and compact runtime context. STORY SYNC will consume only the compact prior + project overlay, expose creator-prior and creator-surprise signals in branch decisions/rehearsal targeting, and continue to let viability, canon, character/causal constraints, and repeated rehearsal evidence own convergence. The full evidence ledger remains durable Git-tracked editorial provenance and is never loaded into normal generation packets.

**Tech Stack:** Python 3.12, stdlib `json`/`pathlib`, `unittest`, existing STORY SYNC and PLG AI tool surface.

**Spec:** `docs/superpowers/specs/2026-09-07-creator-taste-prior-design.md`

## Global Constraints

- Creator taste is a search prior only, never canon or branch authority.
- Accepted canon / story truth, character truth, causal continuity, strong repeated REHEARSAL evidence, and explicit project/audience constraints outrank creator taste.
- Keep creator taste and audience promise separately inspectable.
- Preserve creator surprise as productive counter-pressure, not random novelty.
- Normal generation must not load `evidence.jsonl`.
- Keep active cross-project signals bounded to 10–25.
- Project-local taste never auto-promotes to cross-project taste.
- No embeddings, vector database, learned ML taste model, or generalized personality engine.

---

### Task 1: Creator-taste storage contract and rebuildable runtime prior

**Files:**
- Create: `scripts/creator_taste_prior.py`
- Create: `tests/test_story_sync_creator_taste.py`

**Interfaces:**
- Produces: `validate_prior(prior)`, `validate_project_overlay(overlay)`, `validate_evidence_record(record)`, `append_evidence_record(path, record)`, `rebuild_prior(records, *, max_signals=25)`, `compile_taste_context(prior, overlay=None)`.
- Runtime prior schema: `creator_taste_prior/v1`.
- Project overlay schema: `creator_taste_project/v1`.
- Evidence schema: `creator_taste_evidence/v1`.

- [ ] **Step 1: Write failing tests** proving valid compact priors/overlays compile without ledger contents, invalid schemas/confidence/counts fail, evidence append is duplicate-safe and append-only, project-local signals remain project-local, counterexamples reduce confidence without erasing supported history, and `max_signals` is enforced.
- [ ] **Step 2: Run focused test**: `python -m unittest tests.test_story_sync_creator_taste` and confirm RED because `scripts.creator_taste_prior` does not exist.
- [ ] **Step 3: Implement the smallest module** using stdlib only. Represent evidence observations explicitly as `{id, direction, summary, effect}` where `effect` is `support` or `challenge`; rebuild groups only cross-project observations and computes bounded confidence from support/challenge counts.
- [ ] **Step 4: Re-run focused test** and confirm GREEN.
- [ ] **Step 5: Commit** creator-taste storage/rebuild support.

### Task 2: STORY SYNC search bias and creator-surprise preservation

**Files:**
- Modify: `scripts/story_sync_engine.py`
- Modify: `tests/test_story_sync_creator_taste.py`

**Interfaces:**
- Modify `sync_story(state, *, creator_taste=None)` where `creator_taste` is the compact output of `compile_taste_context`.
- Add qualitative possibility metadata validation for `creator_prior_match` and `creator_surprise`: `low|medium|high`.
- Add deterministic `branch_search_priority(possibility, *, phase)` returning `high|medium|low|none` while never changing viability/kill authority.

- [ ] **Step 1: Add failing tests** proving a creator-likely branch receives greater search priority but cannot rescue an invalidated/redundant branch; a high-surprise viable branch remains rehearsal-eligible during explore/compare; and late convergence does not upgrade creator-taste authority.
- [ ] **Step 2: Run focused tests** and confirm RED for missing behavior.
- [ ] **Step 3: Implement minimal branch metadata/search-priority logic** and add creator signals to `branch_decisions` plus bounded creator-surprise rehearsal targets.
- [ ] **Step 4: Run `tests.test_story_sync_engine` + creator-taste tests** and confirm GREEN.
- [ ] **Step 5: Commit** STORY SYNC integration.

### Task 3: AI-facing compact taste loading

**Files:**
- Modify: `scripts/plg_ai_tools.py`
- Modify: `tests/test_plg_ai_tools.py`

**Interfaces:**
- `sync_story` accepts optional `creator_prior` / `creator_prior_path` and `project_taste` / `project_taste_path`.
- It calls `creator_taste_prior.compile_taste_context(...)` and passes only that compact context to `story_sync_engine.sync_story(state, creator_taste=context)`.
- Evidence-ledger paths are intentionally unsupported in `sync_story`.

- [ ] **Step 1: Add failing tests** for object/path loading, compact delegation, and explicit rejection of a supplied evidence-ledger runtime input.
- [ ] **Step 2: Run `python -m unittest tests.test_plg_ai_tools`** and confirm RED.
- [ ] **Step 3: Implement the narrow adapter** without adding a new canon-write tool.
- [ ] **Step 4: Re-run AI-tool and STORY SYNC tests** and confirm GREEN.
- [ ] **Step 5: Commit** runtime loading support.

### Task 4: Durable Git-tracked state and Dragon Spotter overlay

**Files:**
- Create: `state/long-form/creator-taste/CONTRACT.md`
- Create: `state/long-form/creator-taste/CURRENT.json`
- Create: `state/long-form/creator-taste/evidence.jsonl`
- Create: `state/long-form/creator-taste/projects/dragon-spotter.json`
- Modify: `.github/workflows/story-sync-validation.yml`
- Modify: `tests/test_story_sync_creator_taste.py`

**Interfaces:**
- `CURRENT.json` is the compact cross-project runtime prior.
- `evidence.jsonl` contains only explicit decision evidence and is not a generation input.
- Dragon Spotter overlay contains only project-local deviations/strong local taste.

- [ ] **Step 1: Add failing fixture tests** loading the checked-in prior/overlay and proving both validate and compile separately.
- [ ] **Step 2: Run focused tests** and confirm RED while state files are absent.
- [ ] **Step 3: Add minimal seeded state** with conservative confidence and explicit evidence provenance. Do not manufacture a large historical profile.
- [ ] **Step 4: Update validation workflow paths** to include `scripts/creator_taste_prior.py` and `state/long-form/creator-taste/**`.
- [ ] **Step 5: Run focused + full unit suite** and commit.

### Task 5: Verification and trailhead

**Files:**
- Modify only existing long-form status/trailhead if one exists and the update is directly relevant.

- [ ] **Step 1: Run** `python -m unittest tests.test_story_sync_creator_taste tests.test_story_sync_engine tests.test_story_sync_rehearsal_bridge tests.test_story_sync_report_evidence tests.test_plg_ai_tools`.
- [ ] **Step 2: Run** `python -m unittest discover -s tests -p 'test_*.py'`.
- [ ] **Step 3: Inspect PR CI at final head** and require green focused/full tests before claiming completion.
- [ ] **Step 4: Verify authority contract**: no creator-taste function writes canon prose; `sync_story` remains derived-only; evidence ledger is absent from normal runtime packet; creator-surprise cannot revive invalidated/redundant branches.
- [ ] **Step 5: Leave PR #161 unmerged unless separately authorized.**
