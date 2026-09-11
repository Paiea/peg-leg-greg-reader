# Visual Evidence, Temporal State, and Purpose-Aware Presentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Connect PLG's existing PERFORMANCE visual consumer to rebuildable scene evidence, sparse temporal character state, the existing concrete-asset approval layer, and generated purpose-aware static reader presentation.

**Architecture:** Add one sparse temporal input and two rebuildable generated outputs. Reuse the existing PERFORMANCE freshness/anchor boundary and illustration registry. Persist creator taste only when a concrete asset is approved, then derive reader presentation from live registry state.

**Tech Stack:** Python 3, JSON state files, existing PLG static reader generator and CSS, assertion-based regression scripts.

**Spec:** `docs/superpowers/specs/2026-09-07-visual-evidence-temporal-presentation.md`

## Global Constraints

- Canon prose remains the only story authority.
- PERFORMANCE remains derived editorial evidence and must use the existing freshness + exact-anchor consumer boundary.
- Generated visual scene evidence and reader presentation are rebuildable and must not require hand edits.
- Temporal character state is sparse; unknown chapters return no state.
- `ILLUSTRATION_APPROVALS.json` remains the persistent concrete-asset creator-taste layer.
- Existing reader URLs, Showcase navigation, current live art choices, and `PRODUCTION_HOLD.json` remain unchanged by this implementation.

---

### Task 1: Sparse temporal visual state resolver

**Files:**
- Create: `state/visual/CHARACTER_VISUAL_TIMELINE.json`
- Create: `scripts/character_visual_timeline.py`
- Create: `scripts/test_character_visual_timeline.py`

**Interfaces:**
- Produces: `load_visual_timeline(path) -> list[dict]`
- Produces: `resolve_character_visual_state(records, character, chapter) -> dict | None`
- Produces: `resolve_scene_character_states(records, characters, chapter) -> dict[str, dict]`

- [ ] **Step 1: Write RED tests** proving Ch005 Greg resolves to pre-amputation state with light beard/stubble/fuzz, Ch497 resolves to the supervised prosthetic-trial state, an undeclared chapter returns `None`, and overlapping intervals raise `ValueError`.
- [ ] **Step 2: Run** `python scripts/test_character_visual_timeline.py` and verify failure because the module does not exist.
- [ ] **Step 3: Implement** validation and interval resolution. Scene-local callers may merge/override returned state later; the resolver itself returns only timeline state.
- [ ] **Step 4: Seed** Greg 1–18 and 496–499 only, with `authority: derived_editorial_reference` and `canon_authority: false`.
- [ ] **Step 5: Run** the test and verify GREEN.

### Task 2: Rebuildable visual scene evidence

**Files:**
- Create: `scripts/build_visual_scene_evidence.py`
- Create: `scripts/test_build_visual_scene_evidence.py`
- Generate: `state/visual/VISUAL_SCENE_EVIDENCE.json`

**Interfaces:**
- Consumes: normal scene candidates plus bounded pilot items, illustration registry, temporal timeline, and `load_visual_references(...)` from `scripts/performance_roundtrip_references.py`.
- Produces: `build_visual_scene_evidence(candidates, registry, temporal_states, performance_references) -> list[dict]`

- [ ] **Step 1: Write RED tests** with three candidates: prose-only, temporal-only, and exact-anchor PERFORMANCE-backed. Assert stale/nonmatching PERFORMANCE references are absent, temporal state is attached by character, and current live chapter art is exposed as comparison context.
- [ ] **Step 2: Run** `python scripts/test_build_visual_scene_evidence.py` and verify failure because the builder does not exist.
- [ ] **Step 3: Implement** candidate merge-by-id, existing-art lookup, temporal resolution, and the same normalized exact-anchor match required by the current generation queue. Do not load PERFORMANCE artifacts directly by path.
- [ ] **Step 4: Label** each record `prose_only`, `prose_temporal`, or `prose_temporal_performance` from evidence actually present.
- [ ] **Step 5: Run** the test and verify GREEN.
- [ ] **Step 6: Generate** `state/visual/VISUAL_SCENE_EVIDENCE.json` and verify the five pilot records are present with Ch007/013/018 PERFORMANCE-backed and both Ch005 controls not PERFORMANCE-backed.

### Task 3: Feed generated scene evidence into generation prompts

**Files:**
- Modify: `scripts/build_generation_queue.py`
- Modify: `scripts/build_prompt_packs.py`
- Modify: `scripts/test_build_generation_queue.py`
- Modify: `scripts/test_build_prompt_packs.py`

**Interfaces:**
- Queue records may carry `visual_scene_evidence`.
- Prompt packs render a `TEMPORAL CHARACTER STATE` section from evidence when present.
- Explicit candidate `continuity_notes` remain higher precedence than timeline state for conflicts.

- [ ] **Step 1: Add RED assertions** that a queue record carries matching scene evidence and that prompt rendering includes early Greg's temporal beard/body/mobility state without emitting the legacy BKA/crutch fallback.
- [ ] **Step 2: Run both focused tests** and verify the new assertions fail.
- [ ] **Step 3: Implement** optional evidence-map joining in queue construction and prompt-pack rendering.
- [ ] **Step 4: Preserve** current behavior when no generated evidence file/map is provided.
- [ ] **Step 5: Run both tests** and verify GREEN.

### Task 4: Persist creator taste through existing asset approvals

**Files:**
- Modify: `scripts/illustration_state.py`
- Modify: `scripts/apply_illustration_approvals.py`
- Create: `scripts/test_apply_illustration_approvals.py`

**Interfaces:**
- Optional approval fields: `presentation_role`, `editorial_purpose`, `editorial_note`.
- Allowed presentation roles: `sketch-beat`, `scene-illustration`, `feature-illustration`, `feature-portrait`.
- Approved registry records copy these fields; omitted role defaults later to `scene-illustration`.

- [ ] **Step 1: Write RED tests** showing an approved generated record receives all three taste fields, invalid roles fail, and a legacy approval without new fields still works.
- [ ] **Step 2: Run** `python scripts/test_apply_illustration_approvals.py` and verify failure on missing behavior.
- [ ] **Step 3: Implement** enum validation in illustration state and optional taste propagation in `apply_approvals`.
- [ ] **Step 4: Run** the test and verify GREEN.

### Task 5: Generate purpose-aware reader presentation

**Files:**
- Create: `scripts/build_reader_presentation.py`
- Create: `scripts/test_build_reader_presentation.py`
- Generate: `state/visual/READER_PRESENTATION.json`

**Interfaces:**
- Produces: `build_reader_presentation(registry) -> list[dict]` for live chapter illustrations only.
- Each record contains chapter, asset, paragraph anchor, `presentation_role`, `editorial_purpose`, alt text, and caption.
- Missing role defaults to `scene-illustration`.

- [ ] **Step 1: Write RED tests** for live-only filtering, default role, explicit `feature-portrait`, and deterministic chapter/asset ordering.
- [ ] **Step 2: Run** `python scripts/test_build_reader_presentation.py` and verify failure because the module does not exist.
- [ ] **Step 3: Implement** the pure builder and JSON writer.
- [ ] **Step 4: Run** the test and verify GREEN.
- [ ] **Step 5: Generate** current presentation state without changing any registry status.

### Task 6: Make Illustrated Reader consume presentation roles

**Files:**
- Modify: `scripts/generate_illustrated.py`
- Create: `scripts/test_generate_illustrated_presentation.py`

**Interfaces:**
- `_art_figure(path, number, record=None, presentation=None) -> str`
- Role-to-class mapping:
  - `sketch-beat` -> `chapter-art sketch-beat`
  - `scene-illustration` -> `chapter-art scene-illustration`
  - `feature-illustration` -> `chapter-art feature-illustration`
  - `feature-portrait` -> `chapter-art feature-illustration feature-portrait`

- [ ] **Step 1: Write RED tests** for all four role classes and legacy default rendering.
- [ ] **Step 2: Run** `python scripts/test_generate_illustrated_presentation.py` and verify the explicit roles fail because the generator hardcodes `scene-illustration`.
- [ ] **Step 3: Implement** presentation lookup and class mapping while preserving existing alt/caption/anchor behavior.
- [ ] **Step 4: Keep** static URLs, Showcase mapping, and prose unchanged.
- [ ] **Step 5: Run** the test and verify GREEN.

### Task 7: Rebuild pilot outputs and verify boundaries

**Files:**
- Regenerate: `state/visual/VISUAL_SCENE_EVIDENCE.json`
- Regenerate: `state/visual/GENERATION_QUEUE.json`
- Regenerate: five pilot prompt packs
- Regenerate: `state/visual/GENERATION_PACKET.md`
- Regenerate: `state/visual/READER_PRESENTATION.json`

- [ ] **Step 1: Run** all new and modified focused regression scripts.
- [ ] **Step 2: Rebuild** visual scene evidence, queue, prompt packs, generation packet, and reader presentation.
- [ ] **Step 3: Verify** Ch005 x2 = temporal/prose controls; Ch007/013/018 = temporal + fresh PERFORMANCE.
- [ ] **Step 4: Verify** early Greg prompts include light beard/stubble/fuzz and intact/no-crutch state.
- [ ] **Step 5: Compare branch diff** against main and confirm no chapter prose, Showcase manifest, current live asset choice, illustration approval decision, or production hold is changed merely by the rebuild.
- [ ] **Step 6: Update PR #165** summary/verification to describe the new architecture and exact test evidence.
