# Illustration Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first durable manuscript-informed illustration pipeline: scene-candidate schema, registry schema, backlog generation, prompt-pack generation, and coverage validation.

**Architecture:** Visual production metadata lives in JSON sidecars under `state/visual/`; scripts consume those sidecars and current reader files to produce deterministic Markdown artifacts. Canonical manuscript prose remains untouched. Promotion of binary assets is deliberately deferred until this metadata/control plane is proven.

**Tech Stack:** Python 3.12 standard library, JSON, Markdown, unittest, existing static HTML reader.

**Spec:** `docs/superpowers/specs/2026-09-06-illustration-pipeline-design.md`

## Global Constraints

- Manuscript prose remains canonical and unmodified.
- Shared visual language remains `SKETCH + INK + PAINT`.
- Greg continuity: nineteen, permanent LEFT BKA with knee preserved, right leg intact, two crutches.
- Development art is not live until explicitly approved/promoted.
- Text Reader remains image-free.
- Prefer coverage first; normal `close_enough` art is acceptable when useful and non-contradictory.
- No em dashes in manuscript prose; this implementation does not edit manuscript prose.

---

### Task 1: Scene Candidate Schema and Validation

**Files:**
- Create: `state/visual/SCENE_CANDIDATES.json`
- Create: `scripts/illustration_state.py`
- Create: `tests/test_illustration_state.py`

**Interfaces:**
- Produces: `load_scene_candidates(path: Path) -> list[dict]`
- Produces: `validate_scene_candidates(records: list[dict]) -> None`

- [ ] **Step 1: Write failing tests** for duplicate ids, invalid status/priority/kind/fit target, missing scene summary/visual hook, and a valid candidate.
- [ ] **Step 2: Run** `python -m unittest tests.test_illustration_state -v` and confirm failure because the module/files do not exist.
- [ ] **Step 3: Implement minimal validation** using standard-library JSON and explicit allowed-value sets.
- [ ] **Step 4: Seed `SCENE_CANDIDATES.json`** with an empty `[]`, making empty state valid.
- [ ] **Step 5: Rerun test** and require PASS.
- [ ] **Step 6: Commit** `Add illustration scene candidate state`.

### Task 2: Illustration Registry Schema and Validation

**Files:**
- Create: `state/visual/ILLUSTRATION_REGISTRY.json`
- Modify: `scripts/illustration_state.py`
- Modify: `tests/test_illustration_state.py`

**Interfaces:**
- Produces: `load_registry(path: Path) -> list[dict]`
- Produces: `validate_registry(records: list[dict], root: Path | None = None) -> None`

- [ ] **Step 1: Add failing tests** for duplicate ids, bad status, missing alt text on approved/live records, missing live asset when status is live, and a valid queued record.
- [ ] **Step 2: Run** the focused test and confirm RED.
- [ ] **Step 3: Implement registry validation** with statuses `queued/generated/approved/live/rejected`, required fields, and optional existence checks when `root` is supplied.
- [ ] **Step 4: Seed `ILLUSTRATION_REGISTRY.json`** with `[]`.
- [ ] **Step 5: Rerun test** and require PASS.
- [ ] **Step 6: Commit** `Add illustration registry state`.

### Task 3: Illustration Backlog Generator

**Files:**
- Create: `scripts/build_illustration_backlog.py`
- Create: `state/visual/ILLUSTRATION_BACKLOG.md`
- Create: `tests/test_illustration_backlog.py`

**Interfaces:**
- Consumes: validated scene candidates and registry records.
- Produces: `build_backlog(candidates: list[dict], registry: list[dict], chapter_image_counts: dict[int, int]) -> list[dict]`
- Produces: deterministic Markdown ordered by priority.

- [ ] **Step 1: Write failing tests** proving zero-art chapters rank ahead of one-art chapters, high priority ranks ahead of medium at equal coverage, and live/rejected candidates are excluded.
- [ ] **Step 2: Run** `python -m unittest tests.test_illustration_backlog -v` and confirm RED.
- [ ] **Step 3: Implement chapter image counting** by scanning current `chapters/*.html` for chapter-art `<img>` references.
- [ ] **Step 4: Implement deterministic backlog sorting** by card priority, image count, candidate priority, chapter, id.
- [ ] **Step 5: Generate Markdown** with chapter, title, candidate id, visual hook, status, fit target, and current image count.
- [ ] **Step 6: Run tests and script**; require PASS and deterministic no-diff on immediate second run.
- [ ] **Step 7: Commit** `Generate illustration backlog from reader coverage`.

### Task 4: Prompt Pack Generator

**Files:**
- Create: `scripts/build_prompt_packs.py`
- Create: `state/visual/prompt-packs/.gitkeep`
- Create: `tests/test_illustration_prompt_packs.py`

**Interfaces:**
- Consumes: scene candidate records with `status` of `candidate` or `prompt_ready`.
- Produces: `render_prompt_pack(candidate: dict) -> str`
- Produces: `state/visual/prompt-packs/<candidate-id>.md`

- [ ] **Step 1: Write failing tests** requiring the pack to include scene summary, visual hook, camera/movement guidance, continuity block, `SKETCH + INK + PAINT`, fit target, and deterministic filename.
- [ ] **Step 2: Run** focused tests and confirm RED.
- [ ] **Step 3: Implement renderer** with the Visual Bible prompt order: subject + action + camera + foreground + environmental movement + eye path + manuscript details + continuity + style.
- [ ] **Step 4: Ensure Greg continuity block appears only when `Greg` is listed in candidate characters; Lyssa continuity likewise when present.
- [ ] **Step 5: Run tests** and require PASS.
- [ ] **Step 6: Commit** `Generate reusable illustration prompt packs`.

### Task 5: Coverage Report and CI Contract

**Files:**
- Create: `scripts/report_illustration_coverage.py`
- Create: `state/visual/ILLUSTRATION_COVERAGE.md`
- Create: `tests/test_illustration_coverage.py`
- Modify: `.github/workflows/light-edition.yml`

**Interfaces:**
- Consumes: registry, scene candidates, current `chapters/*.html`, and manuscript/reader frontier discovered by existing tooling.
- Produces: deterministic coverage Markdown and non-zero exit on invalid registry/reader drift.

- [ ] **Step 1: Write failing tests** for zero/one/two/three-plus buckets, approved-but-unpublished count, candidate backlog count, and a chapter image reference missing from the registry.
- [ ] **Step 2: Run** focused tests and confirm RED.
- [ ] **Step 3: Implement report generation** and reader-to-registry consistency check.
- [ ] **Step 4: Add CI steps** after reader generation to run backlog generation, prompt-pack generation, coverage report, and `git diff --check`.
- [ ] **Step 5: Run full suite** `python -m unittest discover -s tests -p 'test_*.py'` and require PASS.
- [ ] **Step 6: Run all three generation/report scripts twice** and require the second run to be idempotent.
- [ ] **Step 7: Commit** `Verify illustration production coverage`.

## Self-review

- Spec coverage: scene candidates, registry, backlog, prompt packs, and coverage/CI are implemented. Binary asset promotion is intentionally deferred to the next bounded phase because it mutates chapter HTML and art assets and should build on the validated metadata layer.
- Placeholder scan: no TODO/TBD placeholders.
- Type consistency: all scripts consume list-of-dict JSON records and share validation through `scripts/illustration_state.py`.

## Verification gate

Before promotion to `main`:

1. `python -m unittest discover -s tests -p 'test_*.py'`
2. `python scripts/build_illustration_backlog.py`
3. `python scripts/build_prompt_packs.py`
4. `python scripts/report_illustration_coverage.py`
5. rerun 2–4 and require no diff
6. run the repository `Refresh Light edition` workflow on the integration branch
7. re-read fresh `main`; rebase/transplant without overwriting newer manuscript work
8. run the exact `main` workflow and require success before calling shipped.