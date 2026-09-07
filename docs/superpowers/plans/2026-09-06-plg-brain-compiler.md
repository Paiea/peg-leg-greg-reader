# PLG Brain Compiler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic task-aware Brain Compiler and read-only Brain Doctor that reduce PLG worker boot context to a compact trustworthy pointer set and expose both through the existing PLG AI/MCP surface.

**Architecture:** Keep all existing project-brain files in place. Add one declarative routing registry, one deterministic compiler, and one read-only doctor. The compiler emits disposable pointer packets only; the doctor validates routing health; existing campaign/scene machinery stays separate.

**Tech Stack:** Python 3.12 standard library, JSON, unittest, existing PLG AI tool surface, optional MCP v2 adapter, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-06-plg-brain-compiler-design.md` plus normative clarifications in `docs/superpowers/specs/2026-09-06-plg-brain-compiler-design-clarifications.md`

## Global Constraints

- Git files remain authority. Compiled brain output is disposable.
- No model calls are required for brain compilation or doctor checks.
- Core compilation performs no network calls and no implicit `git` calls to discover accepted authority.
- Existing PLG brain files remain in place; do not reorganize them into a generic `brain/` hierarchy.
- HOT output has a hard ceiling of 12 pointers and must fail closed rather than silently truncate.
- Doctor is read-only and must never mutate project files.
- Optional GitHub snapshot data is explicit input and never silently rewrites durable routing state.
- No chapter/manuscript prose changes are authorized by this feature.

---

### Task 1: Routing registry and deterministic compiler

**Files:**
- Create: `state/brain/ROUTING_REGISTRY.json`
- Create: `scripts/brain_compiler.py`
- Create: `tests/test_brain_compiler.py`

**Interfaces:**
- Produces: `load_registry(path: Path) -> dict[str, Any]`
- Produces: `compile_brain(task: str, repo_root: Path, registry_path: Path, authority_branch: str | None = None, authority_sha: str | None = None, github_snapshot: dict[str, Any] | None = None) -> dict[str, Any]`
- Produces: `render_packet_text(packet: dict[str, Any]) -> str`
- Produces: `canonical_json(value: Any) -> str`

- [ ] **Step 1: Write failing compiler tests**

Add tests proving dialogue, manuscript, illustration, unknown-task, cold-case-law, deterministic JSON, absent snapshot, snapshot WIP, malformed registry, and HOT ceiling behavior.

Representative assertions:

```python
packet = brain_compiler.compile_brain(
    "whole-manuscript dialogue pass",
    repo_root=root,
    registry_path=registry,
    authority_branch="main",
    authority_sha="abc123",
)
assert "state/EDITOR_STATE.md" in {row["path"] for row in packet["hot"]}
assert "state/PROSE_PLAYBOOK.md" in {row["path"] for row in packet["hot"]}
assert "state/VISUAL_BIBLE.md" not in {row["path"] for row in packet["hot"]}
assert packet["routing"]["confidence"] == "high"
```

```python
packet = brain_compiler.compile_brain(
    "mysterious thing with no known routing words",
    repo_root=root,
    registry_path=registry,
)
assert packet["routing"]["confidence"] == "low"
assert packet["routing"]["matched_tags"] == []
```

```python
first = brain_compiler.canonical_json(packet)
second = brain_compiler.canonical_json(brain_compiler.compile_brain(...))
assert first == second
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python -m unittest tests.test_brain_compiler -v
```

Expected: import failure because `scripts.brain_compiler` does not exist.

- [ ] **Step 3: Add initial PLG routing registry**

Create `state/brain/ROUTING_REGISTRY.json` with:

- schema `plg_brain_routing/v1`
- project authority metadata
- explicit `tag_aliases`
- `exclusive_task_tags`
- discovery include/ignore globs
- the high-value document set from the spec
- at least one VERIFIED workstream for the landed PERFORMANCE campaign stack
- `GENERAL_EDITOR_STATE.md` explicitly cold/case-law

Every registered document must contain: `path`, `owner`, `authority_class`, `default_temperature`, `task_tags`, `reason`. Universal documents additionally set `universal: true`. Historical documents set `case_law: true`.

- [ ] **Step 4: Implement registry validation and task matching**

Implement in `scripts/brain_compiler.py`:

```python
ALLOWED_TEMPERATURES = {"hot", "conditional", "cold"}
ALLOWED_WORKSTREAM_STATUS = {"ACTIVE", "VERIFIED", "FAILED", "SUPERSEDED", "ARCHIVAL"}
HARD_HOT_LIMIT = 12


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

`load_registry()` must reject wrong schema, duplicate document paths, unknown temperatures/statuses, missing required project keys, missing dependency targets, circular dependency graphs, and invalid dependency temperatures.

Task matching must be deterministic: lowercase, normalize punctuation/whitespace, match configured alias phrases first, then individual configured task tags as whole normalized tokens/phrases. Sort matched tags lexically before routing.

- [ ] **Step 5: Implement packet compilation**

`compile_brain()` must:

1. load/validate registry
2. resolve task tags
3. promote universal docs to HOT
4. promote matching docs to HOT unless `case_law`
5. apply declared dependencies
6. leave unmatched specialists at default temperature
7. enforce 12-pointer HOT ceiling
8. merge relevant workstreams and optional GitHub snapshot evidence
9. include explicit warnings for absent authority SHA and snapshot contradictions
10. sort all output deterministically
11. embed pointers/reasons only, never source file bodies

- [ ] **Step 6: Implement text renderer and CLI**

Support:

```bash
python scripts/brain_compiler.py compile --task "continue manuscript" --format json
python scripts/brain_compiler.py compile --task "whole-manuscript dialogue pass" --format text
python scripts/brain_compiler.py compile --task "illustration reconciliation" --github-snapshot /tmp/github.json
```

Text renderer must render from the canonical packet, not independently recompute routing.

- [ ] **Step 7: Run focused tests and verify GREEN**

Run:

```bash
python -m unittest tests.test_brain_compiler -v
```

Expected: all Brain Compiler tests pass.

- [ ] **Step 8: Commit Task 1**

```bash
git add state/brain/ROUTING_REGISTRY.json scripts/brain_compiler.py tests/test_brain_compiler.py
git commit -m "feat: add deterministic PLG Brain Compiler"
```

---

### Task 2: Read-only Brain Doctor

**Files:**
- Create: `scripts/brain_doctor.py`
- Create: `tests/test_brain_doctor.py`

**Interfaces:**
- Consumes: `brain_compiler.load_registry`, `brain_compiler.compile_brain`, `brain_compiler.canonical_json`
- Produces: `run_doctor(repo_root: Path, registry_path: Path, github_snapshot: dict[str, Any] | None = None) -> dict[str, Any]`

- [ ] **Step 1: Write failing Doctor tests**

Tests must prove:

- missing registered paths are errors
- unregistered likely brain files are bounded advisories
- duplicate ACTIVE exclusive owner tags are errors
- archival/superseded docs with `NEXT_TASK` are warnings
- snapshot contradictions are warnings/errors as specified
- oversized HOT source files are advisory only
- identical inputs yield deterministic doctor output
- running doctor does not mutate files

Representative assertion:

```python
before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
report = brain_doctor.run_doctor(root, registry)
after = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
assert before == after
assert report["schema"] == "plg_brain_doctor/v1"
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests.test_brain_doctor -v
```

Expected: import failure because `scripts.brain_doctor` does not exist.

- [ ] **Step 3: Implement deterministic Doctor checks**

Doctor report shape:

```python
{
    "schema": "plg_brain_doctor/v1",
    "errors": [...],
    "warnings": [...],
    "advisories": [...],
    "counts": {"errors": 0, "warnings": 0, "advisories": 0},
}
```

Each finding contains stable `code`, `message`, and relevant `path` or `workstream_id` fields. No timestamps.

Discovery must honor registry include/ignore globs and cap unregistered advisories at 25 paths.

Known fixture tasks for HOT explosion checks:

```python
KNOWN_TASKS = [
    "continue manuscript",
    "writers room development",
    "story control plot",
    "whole-manuscript dialogue pass",
    "structural compression",
    "reverse edit performance",
    "money continuity",
    "illustration reconciliation",
    "reader UI",
    "publishing integration",
    "campaign codex execution",
]
```

- [ ] **Step 4: Add Doctor CLI**

Support:

```bash
python scripts/brain_doctor.py check
python scripts/brain_doctor.py check --github-snapshot /tmp/github.json
```

Exit code 0 when no errors, 1 when errors exist. Warnings/advisories alone do not fail the command.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python -m unittest tests.test_brain_doctor -v
python scripts/brain_doctor.py check
```

Expected: tests pass; real registry has no Doctor errors.

- [ ] **Step 6: Commit Task 2**

```bash
git add scripts/brain_doctor.py tests/test_brain_doctor.py
git commit -m "feat: add PLG Brain Doctor"
```

---

### Task 3: AI tool and MCP exposure

**Files:**
- Modify: `scripts/plg_ai_tools.py`
- Modify: `tests/test_plg_ai_tools.py`
- Modify: `tests/test_plg_mcp_server.py`

**Interfaces:**
- Produces tool: `brain_for(payload: dict[str, Any]) -> dict[str, Any]`
- Produces tool: `brain_doctor(payload: dict[str, Any]) -> dict[str, Any]`

- [ ] **Step 1: Write failing AI-tool tests**

Add assertions that:

```python
assert "brain_for" in plg_ai_tools.TOOLS
assert "brain_doctor" in plg_ai_tools.TOOLS
assert plg_ai_tools.TOOL_SPECS["brain_for"]["read_only"] is True
assert plg_ai_tools.TOOL_SPECS["brain_doctor"]["read_only"] is True
```

Call `brain_for` against a fixture repo and verify a dialogue task returns editor/prose pointers. Call `brain_doctor` and verify report schema.

MCP test must continue asserting adapter tool names equal `plg_ai_tools.TOOLS`, which now necessarily includes both new tools.

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests.test_plg_ai_tools tests.test_plg_mcp_server -v
```

Expected: failures because the two tools are absent.

- [ ] **Step 3: Implement tool wrappers**

Add imports:

```python
from scripts import brain_compiler
from scripts import brain_doctor as brain_doctor_module
```

Implement wrappers using payload paths/defaults:

```python
def brain_for(payload):
    snapshot = _optional_json_input(payload, "github_snapshot", "github_snapshot_path")
    return brain_compiler.compile_brain(
        task=str(payload["task"]),
        repo_root=_path(payload, "repo_root", "."),
        registry_path=_path(payload, "registry_path", "state/brain/ROUTING_REGISTRY.json"),
        authority_branch=payload.get("authority_branch"),
        authority_sha=payload.get("authority_sha"),
        github_snapshot=snapshot,
    )
```

`brain_doctor` delegates to `run_doctor` with the same explicit optional snapshot behavior.

Do not write compiled packets to disk in the tool wrappers.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python -m unittest tests.test_plg_ai_tools tests.test_plg_mcp_server -v
```

Expected: all pass when MCP is absent; MCP-specific listing test may skip until SDK install in CI.

- [ ] **Step 5: Commit Task 3**

```bash
git add scripts/plg_ai_tools.py tests/test_plg_ai_tools.py tests/test_plg_mcp_server.py
git commit -m "feat: expose Brain Compiler through PLG AI tools"
```

---

### Task 4: Worker routing and CI gate

**Files:**
- Modify: `AGENTS.md`
- Modify: `.github/workflows/performance-production-funnel.yml`
- Test: `tests/test_brain_compiler.py`
- Test: `tests/test_brain_doctor.py`

**Interfaces:**
- No new Python interface. This task makes the feature discoverable and continuously verified.

- [ ] **Step 1: Add compact AGENTS routing rule**

Near universal worker routing, add exactly the semantic rule:

```text
For substantial work, prefer the PLG Brain Compiler task packet when available. Use it to select relevant brain pointers, then read the exact referenced authority. Compiled brain output is disposable routing and never outranks repository source files.
```

Also mention that unknown-task/low-confidence packets require falling back to `PROJECT_STATE.md` and ordinary router discovery rather than inventing a specialty.

- [ ] **Step 2: Extend workflow path filters and focused test command**

Add brain files to the workflow paths:

```yaml
- 'state/brain/**'
- 'scripts/brain_compiler.py'
- 'scripts/brain_doctor.py'
- 'tests/test_brain_compiler.py'
- 'tests/test_brain_doctor.py'
```

Add the two focused test modules to the existing focused compiler/campaign command before full-suite execution.

Add a real registry Doctor step:

```yaml
- name: Validate PLG Brain routing
  run: python scripts/brain_doctor.py check
```

Keep optional MCP v2 installation/verification after the full core suite.

- [ ] **Step 3: Run complete verification locally/CI-equivalent**

Run:

```bash
python -m unittest tests.test_brain_compiler tests.test_brain_doctor tests.test_performance_production_funnel tests.test_performance_production_ir tests.test_performance_production_workflow tests.test_performance_index tests.test_performance_campaign tests.test_performance_campaign_execution tests.test_plg_ai_tools tests.test_plg_mcp_server -v
python scripts/brain_doctor.py check
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/performance_roundtrip_references.py --check
python scripts/project_check.py showcase
git diff --check
```

Expected: all pass; no chapter/manuscript files changed.

- [ ] **Step 4: Commit Task 4**

```bash
git add AGENTS.md .github/workflows/performance-production-funnel.yml
git commit -m "ci: route workers through PLG Brain Compiler"
```

---

### Task 5: Final authority and integration audit

**Files:**
- No feature files added in this task unless verification finds a bug.

**Interfaces:**
- Final branch is ready for PR only when exact head passes verification.

- [ ] **Step 1: Compare branch against current main**

Verify branch is based on the intended accepted authority or reconcile safely if `main` moved.

- [ ] **Step 2: Audit changed files**

Require:

- no `chapters/*.html`
- no manuscript prose/checkpoint files
- only brain infrastructure/spec/plan/tests/router/CI changes

- [ ] **Step 3: Verify exact branch head CI**

Use GitHub Actions result for the exact final head. Do not rely on an earlier green commit after later fixes.

- [ ] **Step 4: Open PR and merge only if mergeable/green**

PR body must state:

- deterministic/no-model/no-network core
- disposable packet authority boundary
- Doctor is read-only
- AI/MCP exposure
- exact verification evidence
- zero prose changes

- [ ] **Step 5: Verify main after merge**

Confirm `main` points to the merge result and post-merge workflows start cleanly. Report exact accepted commit SHA.
