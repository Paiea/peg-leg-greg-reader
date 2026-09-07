# PLG Six-Tool AI Operating Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the shipped PERFORMANCE scene compiler into a whole-manuscript AI operating surface with rebuildable retrieval, campaign orchestration, compute routing, reduction, AI-native tools, and effectiveness telemetry.

**Architecture:** Keep `performance_production_funnel.py` as the scene/compiler/canon-apply primitive. Add a disposable SQLite/FTS index and a campaign runner around it; expose the same Python functions through a thin JSON tool API and optional MCP stdio adapter. All parallel model work is derived/read-only, while canon integration is one sequential fail-closed path.

**Tech Stack:** Python 3.12 stdlib (`sqlite3`, `concurrent.futures`, `subprocess`, `json`, `pathlib`, `time`), existing unittest suite, optional official MCP Python SDK v2.

**Specs:**
- `docs/superpowers/specs/2026-09-06-performance-campaign-codex-executor-design.md`
- `docs/superpowers/specs/2026-09-06-performance-ai-tools-telemetry-design.md`

## Global Constraints

- CANON PROSE remains sole story authority.
- No parallel canon writers. All map workers are derived/read-only.
- `.cache/` contains disposable/rebuildable execution state and must be ignored by Git.
- No model call for deterministic work or valid cache hits.
- Default Codex mode is execution-biased and non-creative unless explicitly authorized.
- No quota scraping, account-limit bypass, auto-downloaded local models, Best-of-N, or unbounded retries.
- MCP is optional. Core compiler/index/campaign code works without MCP installed.
- The existing exact-anchor/no-em-dash canon patch path remains the final mutation gate.

---

### Task 1: Rebuildable project resolver/index

**Files:**
- Create: `scripts/performance_index.py`
- Create: `tests/test_performance_index.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces `rebuild_index(compiled_root: Path, db_path: Path) -> dict`
- Produces `query_scenes(db_path: Path, *, query: str | None = None, scene_id: str | None = None, chapter_start: int | None = None, chapter_end: int | None = None, token: str | None = None, money: str | None = None, verdict: str | None = None, limit: int = 50) -> list[dict]`

- [ ] Write tests proving exact scene lookup, FTS lookup, chapter/token/money filters, and delete/rebuild equivalence.
- [ ] Run `python -m unittest tests.test_performance_index -v` and verify RED on missing module/functions.
- [ ] Implement SQLite schema + FTS from compiled scene JSON. Store pointers/metrics/selected derived text only; DB is never authority.
- [ ] Add `.cache/` to `.gitignore`.
- [ ] Re-run focused tests and commit.

### Task 2: Campaign lifecycle, packets, cache planning, reducer

**Files:**
- Create: `scripts/performance_campaign.py`
- Create: `tests/test_performance_campaign.py`

**Interfaces:**
- Produces `plan_campaign(...) -> dict`
- Produces `run_campaign(...) -> dict`
- Produces `reduce_campaign(campaign_root: Path) -> dict`
- Produces `get_campaign_result(campaign_root: Path) -> dict`
- Produces `integrate_campaign(campaign_root: Path, chapter_root: Path, current_authority: str) -> dict`

- [ ] Write RED tests for range compilation, packet IDs, cache-hit suppression, deterministic reducer, resume, and authority-drift integration blocking.
- [ ] Implement chapter-range compilation into `.cache/plg/compiler`, campaign-local JSON/JSONL state, packet planner, and deterministic reducer.
- [ ] Ensure SOURCE WIN records stay lightweight and completed packets are skipped on resume.
- [ ] Re-run focused tests and commit.

### Task 3: Compute router, Codex executor, bounded concurrency, telemetry

**Files:**
- Modify: `scripts/performance_campaign.py`
- Create: `tests/test_performance_campaign_execution.py`
- Create: `state/editorial/CODEX_EXECUTION_POLICY.md`

**Interfaces:**
- Add executor adapters `deterministic`, `codex`, and optional configured `local` command.
- Add append-only `telemetry.jsonl` and deterministic aggregate metrics.

- [ ] Write RED tests using fake executors to prove cache hits launch no worker, concurrency is bounded, retries stop at configured maximum, and missing token usage remains null.
- [ ] Implement execution profiles (`eco=2`, `standard=4`, `burst` explicit), router ordering, `codex exec --ephemeral` adapter, optional local-command adapter, event telemetry, and aggregate metrics.
- [ ] Make model/reasoning names configuration, not hardcoded story state.
- [ ] Add compact Codex execution policy documenting stop/scope rules.
- [ ] Re-run tests and commit.

### Task 4: Sequential integration over existing canon patch machinery

**Files:**
- Modify: `scripts/performance_campaign.py`
- Modify: `tests/test_performance_campaign.py`

- [ ] Write RED tests proving parallel worker outputs cannot mutate canon and stale/overlapping survivors are rejected before integration.
- [ ] Implement sequential survivor collection that builds/validates a `performance_production_batch/v1` and delegates mutation to `performance_production_funnel.apply_batch_to_root` only after current-authority and source checks.
- [ ] Record survivor/rejection telemetry.
- [ ] Re-run campaign + existing PERFORMANCE tests and commit.

### Task 5: Stable AI-native Python/JSON tool interface

**Files:**
- Create: `scripts/plg_ai_tools.py`
- Create: `tests/test_plg_ai_tools.py`

**Interfaces:**
- `compile_range`
- `get_scene_view`
- `query_scenes`
- `plan_campaign`
- `run_campaign`
- `get_campaign_result`
- `reduce_campaign`
- `apply_survivors`

- [ ] Write RED tests proving tool functions delegate to compiler/index/campaign primitives and read tools do not mutate canon.
- [ ] Implement structured JSON-compatible functions plus a CLI `call <tool> --json <payload>` surface.
- [ ] Keep all editorial logic out of the adapter.
- [ ] Re-run focused tests and commit.

### Task 6: Optional real MCP stdio adapter

**Files:**
- Create: `scripts/plg_mcp_server.py`
- Create: `requirements-mcp.txt`
- Create: `tests/test_plg_mcp_server.py`

- [ ] Write tests that inspect MCP tool definitions without requiring the MCP dependency for core tests.
- [ ] Implement an optional official MCP Python SDK v2 stdio server exposing the eight `plg_ai_tools` operations.
- [ ] Mark `apply_survivors` as write/destructive when supported; keep all others read-only where applicable.
- [ ] If MCP is absent, fail with a concise install instruction rather than breaking imports of core PLG modules.
- [ ] Re-run tests and commit.

### Task 7: Routing/workflow integration and full verification

**Files:**
- Modify: `AGENTS.md`
- Modify: `.github/workflows/performance-production-funnel.yml`
- Modify: `README.md` only if a suitable tools section already exists; otherwise do not add general README churn.

- [ ] Add a compact AGENTS routing rule: Chat is creative/design authority; Codex campaign mode executes approved bounded campaigns, uses tools/cache first, and halts at the verified boundary.
- [ ] Expand workflow paths/focused tests to cover campaign/index/AI-tool modules without installing optional MCP for core validation.
- [ ] Run full `python -m unittest discover -s tests -p 'test_*.py' -v` in CI.
- [ ] Run existing PERFORMANCE archive checks and Showcase validation.
- [ ] Verify `git diff --check` and clean validation path.
- [ ] Review changed-file surface: no canon chapter changes in the infrastructure PR.
- [ ] Update PR description with the six-tool implementation and verification evidence.
