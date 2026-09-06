# PERFORMANCE Roundtrip Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve traceable successful PERFORMANCE intermediates as stale-detectable derived references and expose fresh visual evidence optionally to illustration generation without changing manuscript prose or authority.

**Architecture:** Add a chapter-keyed archive under `state/editorial/performance-roundtrip/`, backed by a small read-only Python validator that compares scene-local final-prose anchors against current canonical chapter prose. The illustration generation queue may attach fresh visual evidence as a supplemental field only; missing or stale references have no effect on queue behavior.

**Tech Stack:** Python 3 standard library, JSON, Markdown, existing `unittest` suite and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-performance-roundtrip-archive-design.md`

## Global Constraints

- CANON PROSE is the only story authority.
- `state/editorial/performance-roundtrip/` is derived editorial reference material only.
- Never promote temporary scene PERFORMANCE state into universal character state.
- Backfill 007 / 013 / 018 only from committed historical evidence at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`.
- Do not create heavy archives for source-win scenes by default.
- Stale or missing PERFORMANCE references must not block or change illustration generation behavior.
- Illustration use remains optional and must remain subordinate to canon prose and existing paragraph-anchor validation.
- No `chapters/*.html` manuscript changes are allowed in this implementation.

---

### Task 1: Define archive validation behavior test-first

**Files:**
- Create: `tests/test_performance_roundtrip_references.py`
- Create later in GREEN: `scripts/performance_roundtrip_references.py`

**Interfaces:**
- Produces: `load_reference(chapter: int, archive_root: Path | None = None, chapter_root: Path | None = None) -> dict | None`
- Produces: `validate_reference(chapter: int, archive_root: Path | None = None, chapter_root: Path | None = None) -> dict`
- Produces: `load_visual_reference(chapter: int, archive_root: Path | None = None, chapter_root: Path | None = None) -> dict | None`
- Produces CLI: `python scripts/performance_roundtrip_references.py --check`

- [ ] **Step 1: Write failing tests for missing/fresh/stale and authority behavior**

Tests must prove:

```python
self.assertIsNone(load_visual_reference(999, archive_root=..., chapter_root=...))
self.assertEqual(validate_reference(7, ...)["status"], "fresh")
self.assertEqual(validate_reference(7, chapter_root=mutated_root, ...)["status"], "stale")
self.assertIsNone(load_visual_reference(7, chapter_root=mutated_root, ...))
```

The fixture lock must require `authority == "derived_editorial_reference"` and `canon_authority is False`. Every `result_scene_anchor` must appear exactly once in normalized `article.prose` text.

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `python -m unittest tests.test_performance_roundtrip_references -v`

Expected: FAIL because `scripts.performance_roundtrip_references` does not exist yet.

- [ ] **Step 3: Implement the minimal reader/validator**

Use only the Python standard library. Extract `<article class="prose">`, strip tags, HTML-unescape, normalize whitespace, then validate exact normalized anchor occurrence counts. Return structured reasons for stale references. `load_visual_reference()` must return `None` unless validation is fresh.

- [ ] **Step 4: Run focused tests GREEN**

Run: `python -m unittest tests.test_performance_roundtrip_references -v`

Expected: PASS.

---

### Task 2: Backfill exact successful 007 / 013 / 018 evidence

**Files:**
- Create: `state/editorial/performance-roundtrip/README.md`
- Create: `state/editorial/performance-roundtrip/007/source.lock.json`
- Create: `state/editorial/performance-roundtrip/007/dramatic.md`
- Create: `state/editorial/performance-roundtrip/007/performance.md`
- Create: `state/editorial/performance-roundtrip/007/screenplay.md`
- Create: `state/editorial/performance-roundtrip/007/comparison.md`
- Repeat the same five files for `013/` and `018/`.

**Interfaces:**
- Consumes historical evidence from commit `48bf312924c5d1d6836587e9cb3e21f3944a4d43`.
- Consumed by `scripts/performance_roundtrip_references.py`.

- [ ] **Step 1: Add archive contract and three source locks**

Lock exact historical source provenance:

```text
007 source blob 70f79b2b11940cbadeb970c1e8cf39c7294fdb66, displayed 5
013 source blob 181a2b52326c3b190aa5ae6f9ee8967e4d206715, displayed 9
018 source blob 30538e320c31db744212e4c22922b0f0fe860975, displayed 14
source authority 35055180a116cf7a0dfd4a1fa94704c2c5b0bd40
performance lab 48bf312924c5d1d6836587e9cb3e21f3944a4d43
resulting canon commit fb703c47db1e682ea32f45da5e5bb89b319c4c93
```

Each lock must carry multiple unique final-scene anchors and a compact `visual_reference` derived only from the committed performed screenplay.

- [ ] **Step 2: Copy historical dramatic/performance/screenplay evidence without reconstruction**

Use the exact committed `fixture.md` dramatic block and `performed.md` frames/script for each scene. Do not add inferred character state that was absent from those files.

- [ ] **Step 3: Write comparison records from committed reports plus published result metadata**

Preserve the historical verdict and why, list the source behavior deliberately retained, identify rejected dry-counter/refusal structures only where the historical report did so, and record PR #141 / merge commit `fb703c47...` as the resulting canon publication.

- [ ] **Step 4: Run archive freshness tests**

Run: `python -m unittest tests.test_performance_roundtrip_references -v`

Expected: all three committed references validate fresh against current canon.

---

### Task 3: Make illustration consumption optional and read-only

**Files:**
- Modify: `scripts/build_generation_queue.py`
- Modify or extend tests: `tests/test_performance_roundtrip_references.py`
- Modify: `state/IMAGE_PRODUCTION.md`

**Interfaces:**
- Consumes: `load_visual_reference(chapter: int) -> dict | None`
- Produces: optional queue field `performance_reference`

- [ ] **Step 1: Add a failing queue test**

Create one prompt-ready candidate for a chapter with supplied fresh PERFORMANCE visual evidence and assert the queue record contains:

```python
"performance_reference": {
    "archive_path": "state/editorial/performance-roundtrip/007",
    "chapter": 7,
    "visual_reference": {...},
}
```

Then pass no evidence and assert queue eligibility and all existing fields are unchanged and the supplemental field is absent.

- [ ] **Step 2: Run focused test and verify RED**

Run: `python -m unittest tests.test_performance_roundtrip_references -v`

Expected: FAIL because `build_generation_queue()` does not yet attach optional references.

- [ ] **Step 3: Add the smallest queue integration**

Extend `build_generation_queue(..., performance_references: dict[int, dict] | None = None)` and attach `performance_reference` only when a caller supplied a fresh reference for that chapter. In `main()`, load fresh references through the archive reader. Do not merge PERFORMANCE characters, props, or scene facts into canonical candidate fields automatically.

- [ ] **Step 4: Document illustration authority**

Add a concise section to `state/IMAGE_PRODUCTION.md` stating:

- canonical prose remains visual/story authority;
- fresh successful screenplay archives are optional derived visual evidence;
- they may help scene choice, blocking, props, action ownership, and physical behavior;
- stale/missing references are ignored;
- canonical prose and paragraph-anchor validation still gate generation.

- [ ] **Step 5: Run focused tests GREEN**

Run: `python -m unittest tests.test_performance_roundtrip_references -v`

Expected: PASS.

---

### Task 4: Put stale-reference detection into normal validation

**Files:**
- Modify: `.github/workflows/showcase-canon.yml`
- Modify: `state/editorial/performance-lab/VISIBLE_001_020_ROUNDTRIP.md`

**Interfaces:**
- Consumes CLI from Task 1.

- [ ] **Step 1: Add archive validation to Showcase CI**

Run after existing repository tests:

```yaml
- name: Validate PERFORMANCE roundtrip references
  run: python scripts/performance_roundtrip_references.py --check
```

The command exits nonzero if any committed successful reference is stale/malformed.

- [ ] **Step 2: Amend the first-20 record's persistence language**

Replace the old blanket statement that all intermediates are disposable with the new rule: unsuccessful/source-win intermediates remain disposable by default; successful surviving PERFORMANCE evidence is archived as derived reference material and remains non-authoritative.

- [ ] **Step 3: Run full verification**

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
```

Expected: all unit tests pass; archive validator reports 007/013/018 fresh; Showcase reports zero errors.

- [ ] **Step 4: Verify no manuscript prose changed**

Compare branch against base and assert no `chapters/*.html` file appears in the diff.

- [ ] **Step 5: Open/update PR and use the merged-tree CI result as final evidence**

The PR description must state the authority boundary, exact backfills, stale behavior, optional illustration integration, and that manuscript prose is untouched.
