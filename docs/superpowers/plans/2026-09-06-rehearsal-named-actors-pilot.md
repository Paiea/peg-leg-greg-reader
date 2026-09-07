# REHEARSAL Named Actors Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal named-actor layer to PLG REHEARSAL and run a bounded pilot that compares named-role rehearsal against anonymous scene packets.

**Architecture:** Keep canon and existing PERFORMANCE evidence authoritative. Add one derived actor registry with sticky user casting anchors, compile scene-local role packets from that registry plus existing scene evidence, and persist only compact rehearsal pilot outputs. Named actors are synthetic performers assigned to PLG roles by Mana; actor identity and visual/casting interpretation remain derived and recastable.

**Tech Stack:** Python 3 standard library, JSON/Markdown state artifacts, existing `scripts/performance_production_funnel.py`, unittest.

**Spec:** `docs/superpowers/specs/2026-09-06-rehearsal-simulation-engine-design.md` plus `docs/superpowers/specs/2026-09-06-rehearsal-named-actor-amendment.md`

## Global Constraints

- Canonical `chapters/*.html` prose remains the only story authority.
- REHEARSAL never writes canon directly.
- Sticky user casting anchors outrank generated actor interpretation but do not become prose canon facts unless already canon-supported.
- Synthetic rehearsal cannot self-confirm a character tendency.
- Actor packets are scene-local compiled views, not permanent full-context agents.
- Visual identity is derived, recastable, and era-sensitive.
- Early Greg must not inherit the later peg.
- No em dashes in generated PLG prose candidates.

---

### Task 1: Named actor registry and validation

**Files:**
- Create: `state/editorial/rehearsal/actors.json`
- Create: `scripts/rehearsal_engine.py`
- Create: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Consumes: JSON actor registry.
- Produces: `load_actor_registry(path) -> dict`, `validate_actor_registry(registry) -> None`, `actor_for_role(registry, role) -> dict`.

- [x] Write tests that reject duplicate actor IDs, duplicate role bindings, missing user-anchor provenance, and invalid visual state.
- [x] Run focused tests and verify expected behavior.
- [x] Implement minimal registry loading/validation and role lookup.
- [x] Seed the first Mana-cast company with Greg, Lyssa, Antonius, Hessa, Alden, and Arlo role bindings plus sticky user anchors.
- [x] Run the unit test and verify PASS.
- [x] Commit.

### Task 2: Scene-local actor packet compiler

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Consumes: one actor record, one PLG character role, scene context, optional promoted tendencies.
- Produces: `compile_actor_packet(actor, *, scene_id, role_context, promoted_tendencies=()) -> dict`.

- [x] Write tests proving user anchors persist, unrelated actor history stays cold, scene state overrides era-sensitive visual state, and promoted tendencies are labeled derived.
- [x] Run the focused test and verify expected behavior.
- [x] Implement the compiler with compact fields only.
- [x] Run the focused test and verify PASS.
- [x] Commit.

### Task 3: Rehearsal packet and discovery validators

**Files:**
- Modify: `scripts/rehearsal_engine.py`
- Modify: `tests/test_rehearsal_engine.py`

**Interfaces:**
- Produces: `build_rehearsal_packet(scene, dramatic_lock, actor_packets, baseline=None) -> dict`, `validate_discovery(discovery) -> None`, `independent_support_count(evidence) -> int`.

- [x] Write tests for locked/unlocked surfaces, unique role ownership, discovery provenance, and anti-self-confirmation support counting.
- [x] Verify expected behavior.
- [x] Implement minimal packet/discovery functions.
- [x] Verify PASS.
- [x] Commit.

### Task 4: Bounded current-canon pilot

**Files:**
- Create: `state/editorial/rehearsal/pilots/2026-09-06-named-actors/README.md`
- Create: `state/editorial/rehearsal/pilots/2026-09-06-named-actors/results.json`
- Optional exact evidence files only for genuinely useful rehearsal findings.

**Interfaces:**
- Consumes: current branch canon scenes and existing fresh PERFORMANCE evidence where available.
- Produces: compact comparison between anonymous packet interpretation and named-actor interpretation.

- [x] Select 3-6 bounded scenes containing recurring cast, including at least one dialogue-ownership-sensitive scene.
- [x] Compile named actor packets.
- [x] Produce one ensemble take per scene; produce a second take only if a critic identifies a reason.
- [x] Record discoveries before any prose candidate.
- [x] Compare against anonymous packet baseline for character specificity, movement, speaker legibility, and lock violations.
- [x] Persist only compact findings and any exact evidence that materially supports a surviving candidate.
- [x] Keep canon prose unchanged in the pilot.
- [x] Commit pilot artifacts.

### Task 5: Verification and PR update

**Files:**
- Existing files above only.

- [x] Run focused local rehearsal-engine unit tests: 8/8 pass.
- [x] Run repository CI unit tests and existing validators through `Validate Showcase Canon`: success.
- [x] Inspect PR changed-file list: no `chapters/*.html` files changed.
- [x] Update draft PR #160 with implementation/pilot summary and verification result.
- [x] Leave PR draft because pilot evidence is still exploratory.
