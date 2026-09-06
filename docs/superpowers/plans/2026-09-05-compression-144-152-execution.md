# Chapters 144-152 Structural Compression Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the approved structural compression map for Chapters 144-152 without allowing illustration state or legacy chapter numbering to veto stronger manuscript structure.

**Architecture:** Apply deterministic paragraph-block transformations to the existing HTML authority on `editor/voice-compression-pass`. Use stable chapter identities during surgery. Merge Chapter 150's surviving story function into Chapters 149 and 151 while retaining Chapter 150 only as a legacy alias until the separate publication-number migration is run. Apply prose cuts identically to illustrated and text-reader surfaces, then verify canon/callback continuity and reader navigation.

**Tech Stack:** Python 3.12, repository HTML reader files, unittest, GitHub Actions, existing PLG compression and reader verification scripts.

**Spec:** `state/COMPRESSION_MAP_144_152.md`

## Global Constraints

- Preserve canon outcomes, causality, Greg's voice, relationship development, disability/material continuity, theatre business/economics, later callbacks, and distinctive mundane comedy.
- Illustration state is advisory and currently held. Art does not veto prose cuts, moves, or chapter merges.
- No em dashes in new manuscript prose.
- Stable IDs remain authoritative during structural surgery.
- Do not renumber Chapters 151+ in this execution pass. Chapter 150 becomes an inactive legacy alias after its story material is merged; display renumbering belongs to the later publication migration.
- Boundary continuity with Chapters 143 and 153 must remain intact.

---

### Task 1: Deterministic structural-edit engine

**Files:**
- Create: `scripts/apply_structural_compression_144_152.py`
- Create: `tests/test_structural_compression_144_152.py`

**Interfaces:**
- Consumes: current `chapters/149.html`, `chapters/150.html`, `chapters/151.html`, `chapters/152.html` and matching `light/*.html` files.
- Produces: synchronized edited reader surfaces and a legacy Chapter 150 alias.

- [ ] Write tests for range replacement, bridge insertion, navigation skipping merged Chapter 150, idempotence, and failure on missing source markers.
- [ ] Run tests and confirm they fail before the script exists.
- [ ] Implement exact-marker paragraph transformations and idempotence guards.
- [ ] Run focused tests and confirm pass.
- [ ] Commit.

### Task 2: Execute the 149-152 structural merge wave

**Files:**
- Modify: `chapters/149.html`
- Modify: `chapters/150.html`
- Modify: `chapters/151.html`
- Modify: `chapters/152.html`
- Modify: `light/149.html`
- Modify: `light/150.html`
- Modify: `light/151.html`
- Modify: `light/152.html`

**Interfaces:**
- Consumes: approved map and Task 1 transformer.
- Produces: one fewer active chapter function, tighter first/second-show movement, preserved old URL for Chapter 150.

- [ ] Tighten Chapter 149's redundant backstage setup while preserving Roof Boy, listening/audience failure, spoon, Serra/yellow-scarf pressure, and ensemble improvisation.
- [ ] Move Chapter 150's surviving core into a compact post-rehearsal bridge: River House arrival, body cost, `That's the work`, scene-shape competence, pay-per-show logic, and confirmation of two shows.
- [ ] Replace Chapter 150 story body with a legacy merged-chapter alias that directs edited sequence navigation 149 -> 151 without deleting the old path.
- [ ] Tighten Chapter 151 by compressing repeated backstage repair/procedure after the main live-performance failures are established.
- [ ] Tighten Chapter 152's between-show reset so the second performance starts sooner while preserving first pay, exhaustion, Iven's dead-uncle warning, changed crowd, changed performance, and later Lucan Drell dependency.
- [ ] Apply identical prose transformations to light reader files.
- [ ] Commit.

### Task 3: Lighter compression wave for 144-148

**Files:**
- Modify: `chapters/144.html` through `chapters/148.html`
- Modify: matching `light/144.html` through `light/148.html`

**Interfaces:**
- Consumes: approved per-chapter KEEP/TIGHTEN map.
- Produces: less procedural repetition without collapsing unique tour/hall/roof functions.

- [ ] Chapter 144: compress repeated stall/horse/meal procedure while preserving no-stairs lodging and transfer/body logic.
- [ ] Chapter 145: compress repeated information-withholding, loading, and costume setup while preserving company fragmentation, slipped hitch, long box, and Teren hall problem.
- [ ] Chapter 146: compress front-half cup/room routing and duplicate local-worker argument while preserving wooden hand, Coln debt negotiation, Marek history, and Serra boundary.
- [ ] Chapter 147: compress repeat rehearsal attempts and duplicate costume-room chaos while preserving `waiting for ghosts`, `stop trying to make it good`, one-free-hand disability beat, and yellow-scarf boundary.
- [ ] Chapter 148: only trim route/roof evidence duplication that performs no new inference step; preserve independent town exploration and Roof reputation seed.
- [ ] Commit.

### Task 4: Structural manifest and dependency verification

**Files:**
- Create: `state/compression-batches/144-152.json`
- Update if required: chapter registry / dependency reports generated by existing tooling.

**Interfaces:**
- Consumes: edited chapter files.
- Produces: explicit stable-ID disposition and later publication migration inputs.

- [ ] Record `plg-ch-000150` as `merged` with surviving beats in `plg-ch-000149` and `plg-ch-000151`.
- [ ] Record 144-149,151-152 as active stable identities.
- [ ] Record old Chapter 150 URL as legacy alias pending final publication migration.
- [ ] Run dependency/readiness tooling and ensure no canon blocker was introduced.
- [ ] Commit.

### Task 5: Verification

- [ ] Run `python -m unittest tests.test_structural_compression_144_152`.
- [ ] Run existing relevant reader/compression tests.
- [ ] Verify 149 edited navigation bypasses 150 and 151 points back to 149 on both reader surfaces.
- [ ] Verify Chapter 153 still cashes out `Roof` and first troupe money coherently.
- [ ] Verify Chapter 154's Lucan Drell two-show observation still has two separately legible performances to refer to.
- [ ] Run `git diff --check` and project compression/readiness checks.
- [ ] Inspect word-count delta and reject any cut that makes the range feel summarized rather than denser.
