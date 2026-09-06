# Universal PERFORMANCE Compiler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evolve the existing PERFORMANCE production funnel into a Git-native, scene-addressable AI interface that performs rich deterministic extraction cheaply, caches structured semantic/PERFORMANCE evidence by dependency fingerprint, renders narrow task views, and preserves the existing fail-closed canon patch boundary.

**Architecture:** Keep `scripts/performance_production_funnel.py` as the stable entrypoint and `state/editorial/performance-production/` as the owning state surface. Chapter HTML is parsed into stable scene records with rich mechanical IR. Agent-produced semantic, PERFORMANCE, screenplay, and comparison fields are validated as derived data and reused only while their dependency fingerprints remain valid. Screenplay remains generated/disposable by default; only successful expensive residue continues into the existing roundtrip archive.

**Tech Stack:** Python 3.12 standard library, unittest, JSON, Git/GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-universal-performance-compiler-design.md`

## Global Constraints

- CANON PROSE remains the only story authority.
- Do not create a parallel compiler/editorial pipeline or new root lane.
- `scripts/performance_production_funnel.py` remains the stable entrypoint.
- `state/editorial/performance-production/` remains the owning production state surface.
- Chapter is the scheduling/user-command unit; scene is the caching/invalidation unit.
- Use lineage-stable scene IDs such as `214.s010`; paragraph numbers are locations, not identities.
- Mechanical IR is deterministic and may be rich.
- Semantic/PERFORMANCE fields are derived and must preserve provenance (`observed`, `inferred`, `locked_derived`).
- Stored scene records may be wide; task views loaded into model context must be narrow.
- Screenplay is generated output by default, not canon and not mandatory archival state.
- Exact-boundary canon patching remains fail-closed and preserves the no-em-dash rule.
- Replacement-first cleanup only: prove a stronger primitive, reroute consumers, preserve unique residue, then retire weaker duplicate machinery.

---

### Task 1: Rich deterministic scene extraction

**Files:**
- Modify: `tests/test_performance_production_funnel.py`
- Modify: `scripts/performance_production_funnel.py`

**Interfaces:**
- Produces: `extract_paragraphs(page: str) -> list[str]`
- Produces: `segment_chapter(page: str, chapter: int, previous_manifest: dict | None = None) -> list[dict]`
- Produces: `build_mechanical_ir(scene: dict) -> dict`
- Produces: `source_fingerprint(paragraphs: list[str]) -> str`

- [ ] **Step 1: Write failing tests for deterministic paragraph extraction, fallback scene segmentation, explicit `<hr>` boundaries, stable `s010` spacing, source hashes, dialogue counts, question counts, entity-like capitalized tokens, money mentions, and physical-action candidates.**

Representative assertions:

```python
page = '<article class="prose"><p>Greg lifted the box.</p><p>"Five silver?" Antonius asked.</p><hr><p>Later, Hessa moved the tray.</p></article>'
scenes = funnel.segment_chapter(page, 214)
self.assertEqual(["214.s010", "214.s020"], [scene["scene_id"] for scene in scenes])
self.assertEqual(2, scenes[0]["mechanical"]["paragraph_count"])
self.assertEqual(1, scenes[0]["mechanical"]["dialogue_turns"])
self.assertIn("five silver", scenes[0]["mechanical"]["money_mentions"])
self.assertTrue(scenes[0]["source"]["hash"])
```

- [ ] **Step 2: Push the tests alone and verify the branch workflow fails because the new compiler functions are missing.**

Run via branch CI: `python -m unittest tests.test_performance_production_funnel -v`

Expected: FAIL with missing `segment_chapter` / `build_mechanical_ir` behavior.

- [ ] **Step 3: Implement the smallest deterministic extraction that satisfies the tests.**

Implementation requirements:

```python
SCENE_BREAK_RE = re.compile(r"<hr\\b[^>]*>", re.I)
DIALOGUE_RE = re.compile(r'[“\"](.+?)[”\"]', re.S)
MONEY_RE = re.compile(r"\\b(?:\\d+|one|two|three|four|five|six|seven|eight|nine|ten)\\s+(?:copper|silver|gold)\\b", re.I)
ACTION_WORDS = {"lifted", "moved", "picked", "set", "turned", "walked", "reached", "tapped", "shook", "opened", "closed"}
```

`extract_paragraphs` must parse only `<article class="prose">` and return normalized paragraph text. `segment_chapter` must split on explicit `<hr>` boundaries when present and otherwise safely fall back to one scene for the chapter. IDs are allocated in increments of ten. `build_mechanical_ir` records counts/ratios and conservative text signals without claiming semantic truth.

- [ ] **Step 4: Run focused tests and full suite.**

Run:

```bash
python -m unittest tests.test_performance_production_funnel -v
python -m unittest discover -s tests -p 'test_*.py'
```

Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add scripts/performance_production_funnel.py tests/test_performance_production_funnel.py
git commit -m "Build deterministic PERFORMANCE scene IR"
```

---

### Task 2: Scene manifests, dependency fingerprints, and cache validity

**Files:**
- Modify: `tests/test_performance_production_funnel.py`
- Modify: `scripts/performance_production_funnel.py`

**Interfaces:**
- Consumes: `segment_chapter(...)`
- Produces: `build_chapter_manifest(chapter: int, source_path: str, scenes: list[dict], compiler_versions: dict, previous_manifest: dict | None = None) -> dict`
- Produces: `dependency_fingerprint(*parts: object) -> str`
- Produces: `cache_status(scene_record: dict, *, source_hash: str, semantic_version: str, performance_version: str) -> dict`
- Produces: `write_compiled_chapter(chapter: int, page: str, output_root: Path, previous_manifest: dict | None = None) -> list[Path]`

- [ ] **Step 1: Write failing tests for small chapter manifests, per-scene files, stable IDs across paragraph insertion before an unchanged scene, changed-source invalidation, and unchanged dependency reuse.**

Representative behavior:

```python
manifest = funnel.build_chapter_manifest(214, "chapters/214.html", scenes, funnel.COMPILER_VERSIONS)
self.assertEqual(["214.s010", "214.s020"], manifest["scene_order"])
self.assertNotIn("mechanical", manifest)

status = funnel.cache_status(record, source_hash=record["source"]["hash"], semantic_version="scene-semantic/v1", performance_version="performance/v1")
self.assertTrue(status["mechanical_valid"])
```

`write_compiled_chapter` must write:

```text
state/editorial/performance-production/214/manifest.json
state/editorial/performance-production/214/s010.json
state/editorial/performance-production/214/s020.json
```

- [ ] **Step 2: Push tests alone and verify RED.**

Expected: FAIL because manifest/cache/write APIs are absent.

- [ ] **Step 3: Implement canonical JSON fingerprints and persistence.**

Use deterministic JSON serialization:

```python
def dependency_fingerprint(*parts: object) -> str:
    payload = json.dumps(parts, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

The manifest must stay routing-sized: chapter/source/compiler versions/ordered scene IDs/per-scene source hashes/status/lineage only. Scene records hold rich IR. Reuse a prior scene ID only when deterministic anchors/fingerprint/order matching is unambiguous; otherwise allocate a new spaced ID rather than attaching stale semantics to the wrong prose.

- [ ] **Step 4: Run focused and full tests.**

Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add scripts/performance_production_funnel.py tests/test_performance_production_funnel.py
git commit -m "Cache PERFORMANCE scenes by dependency"
```

---

### Task 3: Provenance-aware semantic/PERFORMANCE state and narrow AI views

**Files:**
- Modify: `tests/test_performance_production_funnel.py`
- Modify: `scripts/performance_production_funnel.py`

**Interfaces:**
- Produces: `validate_claim(claim: dict) -> None`
- Produces: `merge_derived_layer(scene_record: dict, layer: str, payload: dict, *, compiler: str, dependency_hash: str) -> dict`
- Produces: `render_scene_view(scene_record: dict, view: str) -> dict`

Supported views: `performance`, `dialogue`, `continuity`, `illustration`, `comparison`.

- [ ] **Step 1: Write failing tests that reject semantic claims without provenance, preserve locked derived claims against silent overwrite, record material inferred conflicts, and keep each view narrower than the full record.**

Valid claim:

```python
{"value": "recover bargaining leverage", "kind": "inferred", "confidence": 0.88, "compiler": "scene-semantic/v1"}
```

Valid kinds are exactly `observed`, `inferred`, and `locked_derived`.

- [ ] **Step 2: Push tests alone and verify RED.**

Expected: FAIL due missing provenance/view APIs.

- [ ] **Step 3: Implement validation, conflict-preserving merge, and task projections.**

Projection contracts:

- `performance`: source pointer/hash, active task, cast/character state, relationship pressure, required outcome, must-not-drift, physical/dialogue diagnostics, PERFORMANCE fields.
- `dialogue`: source pointer/hash, cast, speaker topology, attribution signals, turn metrics, relationship/social state, voice/performance modulation.
- `continuity`: source pointer/hash, entities, money/measurements, inferred new/reinforced/possible-conflict facts, state/relationship deltas.
- `illustration`: source pointer/hash, cast, location, objects/props, physical actions/body state, scene turn, visual anchors.
- `comparison`: source pointer/hash, diagnostics, source strengths, PERFORMANCE fields, screenplay metadata/content only when supplied.

Do not copy full source prose into every stored record; task callers may load exact source separately when required.

- [ ] **Step 4: Run focused and full tests.**

Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add scripts/performance_production_funnel.py tests/test_performance_production_funnel.py
git commit -m "Add AI-native PERFORMANCE scene views"
```

---

### Task 4: Universal screenplay/comparison record contract with legacy batch compatibility

**Files:**
- Modify: `tests/test_performance_production_funnel.py`
- Modify: `scripts/performance_production_funnel.py`
- Add/update generated state only for bounded golden validation under `state/editorial/performance-production/007/`, `013/`, `018/` if the command explicitly writes it.

**Interfaces:**
- Produces: `validate_scene_record(record: dict) -> None`
- Produces: `set_screenplay_result(scene_record: dict, screenplay: str, *, compiler: str, dependency_hash: str) -> dict`
- Produces: `set_comparison_result(scene_record: dict, comparison: dict, *, compiler: str, dependency_hash: str) -> dict`
- CLI adds `--compile-chapter N`, `--output-root PATH`, and `--view VIEW --scene ID` while preserving existing `--batch` / `--apply` behavior.

- [ ] **Step 1: Write failing tests proving every compiled scene can carry screenplay output regardless of prior screening, `source_win` is valid after screenplay, `performance_candidate` requires a bounded possible-win description, and legacy `performance_production_batch/v1` still validates/applies unchanged.**

Comparison outcomes are exactly:

```text
source_win
performance_candidate
ambiguous
```

Screenplay stays derived/generated; presence never authorizes a canon patch.

- [ ] **Step 2: Push tests alone and verify RED.**

- [ ] **Step 3: Implement the universal record contract and CLI while leaving model generation external/agent-driven.**

`--compile-chapter` performs deterministic scene extraction/cache refresh only. `--view` emits a narrow JSON packet suitable for ChatGPT/Codex. Agent workers may then write semantic/PERFORMANCE/screenplay/comparison data through the validated record contract. Do not add an API key, network model client, or parallel service.

- [ ] **Step 4: Golden-case check against successful archives 007, 013, 018.**

The deterministic compiler must produce addressable scene records whose source anchors overlap each archive's `result_scene_anchors`. It is not required to regenerate historical screenplay text byte-for-byte. It must preserve enough addressing/provenance to let an AI worker load the exact successful scene plus its locked derived evidence without scanning the chapter blindly.

- [ ] **Step 5: Run focused tests, full suite, existing archive validation, and Showcase validation.**

```bash
python -m unittest tests.test_performance_production_funnel -v
python -m unittest discover -s tests -p 'test_*.py'
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
```

Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add scripts/performance_production_funnel.py tests/test_performance_production_funnel.py state/editorial/performance-production
git commit -m "Make PERFORMANCE screenplay compilation universal"
```

---

### Task 5: Workflow integration and replacement-first audit surface

**Files:**
- Modify: `.github/workflows/performance-production-funnel.yml`
- Modify: `docs/superpowers/specs/2026-09-06-universal-performance-compiler-design.md`
- Create: `state/editorial/performance-production/REPLACEMENT_AUDIT.json`

**Interfaces:**
- Workflow continues to own the same branch and existing canon patch gate.
- `REPLACEMENT_AUDIT.json` records candidates only; it does not delete or reroute anything by itself.

- [ ] **Step 1: Write/extend workflow contract tests in `tests/test_performance_production_funnel.py` that assert the branch workflow validates the scene compiler and does not automatically commit disposable screenplay outputs.**

- [ ] **Step 2: Verify RED if workflow does not yet include the compiler validation command.**

- [ ] **Step 3: Update workflow to run deterministic compiler validation before any legacy batch apply, while preserving full tests/archive/Showcase checks.**

Required behavior:

```bash
python scripts/performance_production_funnel.py --compile-chapter 7 --output-root /tmp/performance-compiler-smoke
python scripts/performance_production_funnel.py --batch state/editorial/performance-production/batch-027-075.json
```

The workflow must not `git add` generated scene records or screenplay outputs from smoke compilation.

- [ ] **Step 4: Add a replacement audit with evidence categories, not deletions.**

Initial candidate jobs to inspect later:

```json
{
  "schema": "performance_replacement_audit/v1",
  "candidates": [
    {"surface": "performance-lab", "status": "keep_case_law", "replacement_proven": false},
    {"surface": "performance-roundtrip-five-file-archive", "status": "keep_until_structured_equivalence", "replacement_proven": false},
    {"surface": "dialogue duplicate extraction", "status": "audit_consumer_overlap", "replacement_proven": false},
    {"surface": "illustration cast/prop extraction", "status": "audit_consumer_overlap", "replacement_proven": false},
    {"surface": "large editorial continuation state", "status": "audit_reconstructible_mechanical_residue", "replacement_proven": false}
  ]
}
```

No candidate may be deleted or retired in this implementation merely because the new compiler exists.

- [ ] **Step 5: Mark the spec implemented foundation and record remaining model-runtime boundary explicitly.**

State that the repo now owns deterministic compilation, structured cache, views, and validation; semantic/PERFORMANCE/screenplay generation remains an agent operation until a model runtime is deliberately introduced.

- [ ] **Step 6: Run final verification.**

```bash
python -m unittest tests.test_performance_production_funnel -v
python -m unittest discover -s tests -p 'test_*.py'
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
git diff --check
```

Expected: all PASS with no canon chapter mutations from compiler smoke tests.

- [ ] **Step 7: Commit.**

```bash
git add .github/workflows/performance-production-funnel.yml docs/superpowers/specs/2026-09-06-universal-performance-compiler-design.md state/editorial/performance-production/REPLACEMENT_AUDIT.json tests/test_performance_production_funnel.py
git commit -m "Integrate universal PERFORMANCE compiler foundation"
```
