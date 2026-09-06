# Showcase Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a non-destructive whole-chapter showcase layer that preserves canonical chapter identity while generating contiguous reader-facing numbering and visible-only navigation.

**Architecture:** A sparse publishing manifest records only chapter visibility overrides. A focused `scripts/showcase.py` module validates that manifest and builds an immutable mapping from canonical chapter IDs to showcase numbers. Reader generators and home contents consume that mapping while manuscript and art systems continue to use canonical IDs.

**Tech Stack:** Python 3 standard library, unittest, existing static HTML generators.

**Spec:** `docs/superpowers/specs/2026-09-05-showcase-canon-design.md`

## Global Constraints

- Whole-chapter curation only.
- Full manuscript authority must not be rewritten by showcase tooling.
- Canonical chapter IDs and file paths remain stable.
- Showcase numbering is generated and contiguous.
- Version 1 defaults every chapter to visible.
- Artwork remains keyed to canonical chapter ID.
- No archive UI or full/showcase toggle in version 1.

---

### Task 1: Showcase manifest and mapping core

**Files:**
- Create: `publishing/showcase_chapters.json`
- Create: `scripts/showcase.py`
- Create: `tests/test_showcase.py`

**Interfaces:**
- Produces: `load_showcase_manifest(path: Path) -> dict`
- Produces: `build_showcase_map(canonical_numbers: list[int], manifest: dict) -> ShowcaseMap`
- Produces: `ShowcaseMap.visible_canon: tuple[int, ...]`
- Produces: `ShowcaseMap.showcase_number(canon: int) -> int | None`
- Produces: `ShowcaseMap.previous_visible(canon: int) -> int | None`
- Produces: `ShowcaseMap.next_visible(canon: int) -> int | None`

- [ ] Write tests covering default-all-visible, one hidden chapter, contiguous display numbering, previous/next skipping hidden chapters, invalid reason codes, unsupported scene-level fields, and references to unknown canonical chapters.
- [ ] Run `python -m unittest tests.test_showcase -v` and confirm failures before implementation.
- [ ] Implement the smallest parser/map needed to satisfy those tests using only the Python standard library.
- [ ] Run `python -m unittest tests.test_showcase -v` and confirm pass.
- [ ] Commit the manifest, module, and tests.

### Task 2: Make Illustrated Reader navigation showcase-aware

**Files:**
- Modify: `scripts/generate_illustrated.py`
- Create: `tests/test_generate_illustrated_showcase.py`

**Interfaces:**
- Consumes: `ShowcaseMap` from Task 1.
- Rendered chapter path remains canonical: `chapters/{canon:03d}.html`.
- Reader-visible heading/meta/nav labels use `showcase_number(canon)`.

- [ ] Write a test with canonical `[1,2,3,4]` and hidden `3` proving Canon 4 renders as reader Chapter 3 and Canon 2 links next to `004.html` labeled Chapter 3.
- [ ] Run the focused test and confirm failure.
- [ ] Change `render_chapter` to accept a `ShowcaseMap`; remove arithmetic previous/next logic and use visible-order navigation.
- [ ] In `main`, build the showcase map from all known canonical chapter numbers and generate only requested chapters that are visible; keep source/path identity canonical.
- [ ] Run the focused test and existing illustrated-reader tests.
- [ ] Commit.

### Task 3: Make Text Reader and homepage contents showcase-aware

**Files:**
- Modify: `scripts/generate_light.py`
- Modify: `scripts/update_home_contents.py`
- Modify: `scripts/reader_sections.py`
- Modify: `tests/test_generate_light.py`
- Modify: `tests/test_generate_light_index.py`
- Modify: `tests/test_update_home_contents.py`

**Interfaces:**
- Consumes: `ShowcaseMap` from Task 1.
- Homepage/text-reader links use canonical paths but visible labels use showcase numbers.
- Book/Act grouping remains canonical; rendered range labels are computed from visible showcase numbers in each section.

- [ ] Add tests proving hidden chapters are absent from Text Reader and homepage indexes.
- [ ] Add tests proving previous/next navigation skips hidden chapters and uses showcase labels.
- [ ] Add tests proving an Act with visible canon chapters `[1,2,4]` reports its showcase span without exposing a canonical-number gap.
- [ ] Run focused tests and confirm failures.
- [ ] Thread `ShowcaseMap` through index/render functions and filter chapter dictionaries to visible canonical IDs.
- [ ] Extend `reader_sections` with optional display-number mapping while preserving current behavior when none is supplied.
- [ ] Run all touched tests and confirm pass.
- [ ] Commit.

### Task 4: Validation and project integration

**Files:**
- Modify: `scripts/project_check.py`
- Modify: `state/PROJECT_STATE.md`
- Modify: `AGENTS.md`
- Create or modify: `tests/test_project_check.py` as appropriate

**Interfaces:**
- Adds project check result key `showcase`.
- `python scripts/project_check.py showcase` validates manifest against canonical numbers discoverable from current reader/manuscript authority.

- [ ] Add tests for valid default manifest and invalid unknown chapter override.
- [ ] Run focused validation tests and confirm failure.
- [ ] Add `showcase_check` using the Task 1 parser/map.
- [ ] Document that manuscript/editorial/continuity workers use Full Canon, while Reader/Publishing workers consume Showcase for public sequence.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/project_check.py showcase` and relevant existing project checks.
- [ ] Verify an empty override manifest yields identity numbering and no reader-visible removals.
- [ ] Commit.

## Final verification

- [ ] Confirm `publishing/showcase_chapters.json` contains no hidden chapters at launch.
- [ ] Confirm no manuscript prose files changed.
- [ ] Confirm no art registry or art files changed.
- [ ] Confirm Canon 1..N maps to Showcase 1..N with the launch manifest.
- [ ] Confirm a temporary test fixture hiding one chapter produces contiguous reader numbering and skips it in navigation.
- [ ] Compare branch against `main` and review every changed file for scope.
