# PLG Brain Compiler Design

## Status

Approved architectural design for a deterministic PLG brain-routing compiler and read-only doctor.

## Problem

Peg-Leg Greg has accumulated a durable project brain with strong authority rules, specialist state, workflow playbooks, active workstreams, case law, and generated execution infrastructure. The repository is now good at preserving knowledge, but fresh workers still spend too much effort discovering which subset of that knowledge matters for a given job.

The current root router already says workers should keep unrelated specialist state cold. The missing primitive is a deterministic compiler that turns that doctrine into a small task-specific routing surface.

The target user experience is:

```text
AGENTS.md
  -> brain_for(task)
  -> exact authority and state pointers
  -> work
```

rather than:

```text
AGENTS.md
  -> PROJECT_STATE.md
  -> inspect state/
  -> inspect active WIP
  -> guess which specialist files matter
```

A worker asking "What do I need for this job?" should normally receive roughly 5-15 pointers, not a large directory listing.

## Architectural rule

The Brain Compiler is not a new intelligence layer and is not project authority.

It is a mostly deterministic routing compiler over existing authority.

**Git files remain authority. Compiled brain output is disposable.**

Deleting every compiled output must not destroy any project fact, decision, canon state, or workstream authority.

## Goals

1. Compile a tiny model-facing task packet from the existing project brain.
2. Encode HOT / CONDITIONAL / COLD loading behavior explicitly.
3. Surface active, verified, superseded, failed, and archival workstreams without making old work look current.
4. Preserve domain-specific PLG brain files in place rather than reorganizing them into a generic folder hierarchy.
5. Make routing deterministic and inspectable.
6. Add a read-only doctor that detects brain-routing drift and contradictions.
7. Expose the compiler through the existing PLG AI tool surface and optional MCP adapter.
8. Keep live GitHub metadata optional and explicit rather than introducing a hidden network dependency.

## Non-goals

- no vector database
- no embeddings requirement
- no autonomous story judgment
- no automatic rewriting of state files
- no replacement for `AGENTS.md`
- no new canon source
- no generic cross-project framework extraction
- no automatic deletion of historical brain material
- no background daemon
- no requirement that every existing state file be eagerly annotated by hand before the compiler is useful

## Core mental model

The repository remains wide at rest and narrow in context.

The compiler produces five sections:

```text
PROJECT
HOT FOR THIS TASK
CONDITIONAL
ACTIVE WIP
COLD / CASE LAW
```

Example:

```text
PROJECT
  authority: main
  canon: manuscript prose
  current engines: 01 / 02 / 03 / 04
  current manuscript owner: state/MANUSCRIPT_STATE.md

HOT FOR THIS TASK
  state/EDITOR_STATE.md
  state/PROSE_PLAYBOOK.md
  state/editorial/CODEX_EXECUTION_POLICY.md

CONDITIONAL
  state/CHARACTER_BIBLE.md [load if character continuity matters]
  state/ECONOMY_CONTINUITY.md [load if money/value changes]
  state/VISUAL_BIBLE.md [load if visual consequences matter]

ACTIVE WIP
  performance-campaign: VERIFIED [source: durable declaration or supplied GitHub snapshot]
  dialogue-owner: ACTIVE [...]

COLD / CASE LAW
  state/GENERAL_EDITOR_STATE.md [completed case law]
  historical audits [...]
```

The compiler returns pointers plus short deterministic reasons. It does not duplicate the full contents of those files.

## Inputs

### 1. Stable routing registry

Add a compact declarative registry at:

`state/brain/ROUTING_REGISTRY.json`

The registry describes routing metadata, not story truth.

Initial schema:

```json
{
  "schema": "plg_brain_routing/v1",
  "project": {
    "authority": "main",
    "canon": "manuscript prose",
    "root_router": "AGENTS.md",
    "project_state": "state/PROJECT_STATE.md",
    "manuscript_owner": "state/MANUSCRIPT_STATE.md",
    "engines": ["01", "02", "03", "04"]
  },
  "documents": [
    {
      "path": "state/EDITOR_STATE.md",
      "owner": "04",
      "authority_class": "editorial_state",
      "default_temperature": "conditional",
      "task_tags": ["editorial", "dialogue", "compression", "performance", "prose"],
      "reason": "Current editorial routing and durable editor state."
    }
  ],
  "workstreams": []
}
```

Allowed `default_temperature` values:

- `hot`
- `conditional`
- `cold`

Allowed workstream statuses:

- `ACTIVE`
- `VERIFIED`
- `FAILED`
- `SUPERSEDED`
- `ARCHIVAL`

The registry should start small and cover high-value durable brains first. The doctor reports unregistered likely brain files so coverage can improve incrementally.

### 2. Repository files

The compiler reads the registry plus exact repository paths it references. It may also inspect deterministic structural signals such as:

- whether a registered file exists
- `NEXT_TASK` headings
- file size
- known root state/playbook filenames
- branch-local source authority supplied by the caller

It must not infer project facts from filenames alone beyond routing metadata.

### 3. Optional GitHub snapshot

Live branch / PR status is useful but must not become a hidden runtime dependency.

The compiler accepts an optional JSON snapshot supplied by a caller that already has GitHub visibility.

Conceptual schema:

```json
{
  "schema": "plg_brain_github_snapshot/v1",
  "authority_sha": "...",
  "branches": [
    {"name": "editor/dialogue-pass", "sha": "..."}
  ],
  "pull_requests": [
    {
      "number": 147,
      "head": "architecture/performance-campaign-codex-mode",
      "head_sha": "...",
      "state": "closed",
      "merged": true,
      "merge_commit_sha": "..."
    }
  ]
}
```

If no snapshot is supplied, compilation remains fully functional from durable repo state. The output records `github_snapshot: absent` rather than pretending live WIP was checked.

The core compiler performs no network calls.

## Task classification

The first version uses deterministic tag matching rather than model classification.

`brain_for(task)` normalizes the task string and matches configured task tags and aliases.

Initial task families should include at least:

- manuscript / forward production
- writers room / development
- story control / plot
- editorial / prose
- dialogue / attribution
- compression
- performance / reverse edit
- continuity
- economy / money
- illustration / visual production
- reader / UI
- publishing / integration
- campaign / Codex execution

The registry can define aliases such as:

```json
{
  "tag_aliases": {
    "reverse edit": ["performance", "editorial"],
    "whole-manuscript dialogue": ["dialogue", "editorial"],
    "continue manuscript": ["manuscript"],
    "images": ["illustration"]
  }
}
```

Unknown task wording must fail soft: include root project/routing pointers and report low routing confidence rather than inventing a specialty.

## Temperature compilation

For each registered document, compute an effective temperature for the task.

Rules:

1. Root routing / project authority documents explicitly marked universal remain HOT.
2. A document whose `task_tags` match the requested task becomes HOT unless explicitly cold-only.
3. A registered dependency of a HOT document becomes HOT or CONDITIONAL according to its registry relation.
4. Nonmatching specialist brains remain CONDITIONAL or COLD according to their defaults.
5. Historical / case-law documents never become HOT merely because their filename resembles the task; they require an explicit registry rule.
6. The compiler caps HOT output by pointer count and reports an error if registry rules would exceed the configured maximum rather than silently flooding context.

Default limits:

- HOT: 12 pointers maximum
- CONDITIONAL: 12 pointers maximum
- ACTIVE WIP: 12 entries maximum
- COLD / CASE LAW: 12 entries maximum

A caller may request lower display limits but not raise the hard HOT ceiling without an explicit CLI flag.

## Output contract

Machine-readable output:

```json
{
  "schema": "plg_brain_packet/v1",
  "task": "whole-manuscript dialogue pass",
  "authority": {
    "branch": "main",
    "sha": "...",
    "canon": "manuscript prose"
  },
  "routing": {
    "matched_tags": ["dialogue", "editorial"],
    "confidence": "high",
    "github_snapshot": "present"
  },
  "project": [...],
  "hot": [...],
  "conditional": [...],
  "active_wip": [...],
  "cold_case_law": [...],
  "warnings": []
}
```

Each pointer entry should contain only compact routing metadata:

```json
{
  "path": "state/PROSE_PLAYBOOK.md",
  "owner": "04",
  "reason": "Craft authority for prose/editorial work.",
  "source": "registry"
}
```

The CLI also supports a compact human-readable render of the same packet.

No full state-file body is embedded in the packet.

## Workstream model

Workstreams are routing status, not canon.

A durable workstream entry may include:

```json
{
  "id": "performance-campaign",
  "status": "VERIFIED",
  "task_tags": ["performance", "campaign"],
  "owner_path": "docs/superpowers/specs/2026-09-06-performance-campaign-codex-executor-design.md",
  "branch": "architecture/performance-campaign-codex-mode",
  "accepted_commit": "0dee2032e8112f206a4dbef1eee2dfa24108119e",
  "reason": "Campaign runner and AI tool surface accepted on main."
}
```

Rules:

- `ACTIVE` appears in ACTIVE WIP.
- `VERIFIED` appears only when relevant, as accepted machinery/current capability rather than unresolved work.
- `SUPERSEDED`, `FAILED`, and `ARCHIVAL` are COLD / CASE LAW unless explicitly requested.
- A supplied GitHub snapshot may confirm or contradict a durable workstream declaration.
- Contradictions become warnings and doctor findings. Live snapshot data does not silently rewrite the registry.

## Brain Doctor

Add a read-only doctor that validates compiler inputs and routing health.

Doctor checks should include:

1. registered document path missing
2. duplicate registry entries for one path
3. unknown temperature/status values
4. HOT rule explosion beyond the hard ceiling for known task fixtures
5. likely durable brain files under `state/` that are unregistered
6. multiple ACTIVE workstreams claiming the same exclusive owner tag when the registry marks that tag exclusive
7. stale branch / PR pointers when a GitHub snapshot proves they are gone or merged
8. durable workstream status contradicting supplied live snapshot
9. `NEXT_TASK` present in a document marked archival/superseded
10. project owner pointer missing
11. oversized registered HOT documents, reported as advisory rather than automatically demoted
12. output determinism: identical inputs produce byte-equivalent canonical JSON

Doctor severity levels:

- `error`: routing cannot be trusted
- `warning`: likely drift or ambiguity
- `advisory`: maintainability issue, not routing failure

The doctor never edits files.

## File boundaries

Create focused implementation units:

### `scripts/brain_compiler.py`

Owns:

- registry loading/validation
- task normalization/tag matching
- effective temperature calculation
- packet compilation
- compact text rendering
- optional GitHub snapshot merge
- CLI `compile`

It does not perform doctor policy beyond schema validation required for safe compilation.

### `scripts/brain_doctor.py`

Owns:

- repository/registry health checks
- optional GitHub snapshot consistency checks
- deterministic report generation
- CLI `check`

It imports public registry/compilation helpers from `brain_compiler.py` rather than duplicating parsing logic.

### `state/brain/ROUTING_REGISTRY.json`

Owns stable PLG-specific routing metadata.

### Existing AI tool surface

Extend `scripts/plg_ai_tools.py` with:

- `brain_for`
- `brain_doctor`

Extend `scripts/plg_mcp_server.py` automatically through the existing shared tool map, preserving optional MCP behavior.

`brain_for` is read-only with respect to project authority. It may create no durable state.

`brain_doctor` is read-only.

## CLI

Initial commands:

```text
python scripts/brain_compiler.py compile --task "whole-manuscript dialogue pass" --format text
python scripts/brain_compiler.py compile --task "continue manuscript" --format json
python scripts/brain_compiler.py compile --task "illustration reconciliation" --github-snapshot /tmp/github.json

python scripts/brain_doctor.py check
python scripts/brain_doctor.py check --github-snapshot /tmp/github.json
```

AI tool calls:

```text
brain_for({"task": "whole-manuscript dialogue pass"})
brain_doctor({})
```

## Integration with AGENTS.md

Do not replace the root worker router.

Add one compact routing instruction:

> For substantial work, prefer the Brain Compiler task packet when available. Use it to select relevant brain pointers, then read the exact referenced authority. Compiled brain output is disposable routing and never outranks repository source files.

This should reduce boot-time discovery without turning the compiler into mandatory story authority.

## Integration with campaign tools

The Brain Compiler is upstream of the existing campaign/index tools.

A campaign-oriented worker may use:

```text
brain_for(task)
  -> relevant project/campaign/editorial pointers
  -> compile_range / query_scenes / run_campaign
```

The Brain Compiler does not absorb scene indexing, campaign planning, reducer logic, or model routing.

## Caching

Compilation is cheap. The first version does not require a persistent cache.

A caller may write packet JSON under `.cache/plg/brain/`, but generated packets are ignored and disposable.

The doctor must not depend on cached packets.

## Determinism

Given identical:

- registry bytes
- repository file tree/signals
- authority inputs
- optional GitHub snapshot
- task string

canonical JSON packet output must be deterministic.

Sort all lists by explicit ranking key then stable path/id.

Human-readable text is rendered from the canonical packet rather than compiled independently.

## Failure behavior

Fail closed on malformed registry or missing project/root authority pointers.

Fail soft on:

- unknown task wording
- absent optional GitHub snapshot
- unregistered specialist files
- stale optional WIP metadata

Warnings must be explicit in output.

The compiler must never invent a path to satisfy a missing category.

## Initial registry strategy

Do not attempt to perfectly classify every historical state file in version one.

Register the high-value durable routing set first, including at least:

- `AGENTS.md`
- `state/PROJECT_STATE.md`
- `state/HANDSHAKE_PROTOCOL.md`
- `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
- `state/MANUSCRIPT_WORKFLOW.md`
- `state/MANUSCRIPT_STATE.md`
- `state/OPEN_THREADS.md`
- `state/STORY_NORTH_STAR.md`
- `state/DEVELOPMENT_CYCLE.md`
- `state/WRITERS_ROOM_STATE.md`
- `state/STORY_CONTROL_STATE.md`
- `state/PLOT_CONTROL.md`
- `state/PROSE_PLAYBOOK.md`
- `state/EDITOR_STATE.md`
- `state/GENERAL_EDITOR_STATE.md`
- `state/CHARACTER_BIBLE.md`
- `state/SETTING_BIBLE.md`
- `state/ECONOMY_CONTINUITY.md`
- `state/RESEARCH_LEDGER.md`
- `state/VISUAL_BIBLE.md`
- `state/IMAGE_PRODUCTION.md`
- `state/READER_DESIGN_LAB.md`
- `state/editorial/CODEX_EXECUTION_POLICY.md`

The doctor then supplies an incremental queue of likely unregistered brain files rather than requiring a giant migration.

## Testing requirements

The implementation must prove at least:

1. dialogue/editorial tasks select editor/prose state as HOT without loading visual/economy brains HOT
2. manuscript tasks select manuscript engine/state/open threads plus story direction
3. illustration tasks select visual/image production and exact manuscript-routing pointers
4. unknown tasks return universal routing with low confidence and no invented specialty
5. historical case law remains cold unless explicitly requested
6. packet output contains pointers/reasons but not full source bodies
7. identical inputs generate deterministic JSON
8. missing optional GitHub snapshot does not break compilation
9. supplied snapshot can surface relevant ACTIVE WIP
10. contradictory live/durable workstream state produces a warning
11. malformed registry fails closed
12. missing registered path is caught by doctor
13. unregistered likely state files are reported but do not make compilation fail
14. HOT pointer ceiling is enforced
15. doctor does not mutate repository files
16. `brain_for` and `brain_doctor` are exposed through `plg_ai_tools.py`
17. optional MCP adapter lists the two new tools when the SDK is installed
18. existing PERFORMANCE/campaign tests remain green
19. normal validation leaves the repository clean
20. no manuscript/chapter prose is modified by this feature

## Workflow / CI

Extend the existing PERFORMANCE/campaign validation workflow or add a small focused brain validation workflow if that keeps ownership clearer.

Preferred first implementation: extend the existing AI-tool validation workflow because `plg_ai_tools.py` and MCP are already verified there, while keeping brain tests in separate test modules.

The gate must run:

- focused Brain Compiler tests
- focused Brain Doctor tests
- PLG AI tool tests
- MCP adapter test when optional SDK is installed
- full repository unit suite
- Showcase/archive checks already required by the existing workflow
- clean-worktree validation

## Success criteria

The feature succeeds when a fresh worker can ask for a task packet and receive a compact trustworthy routing surface that:

- points to the right current authority
- keeps unrelated specialist brains cold
- surfaces relevant active WIP without pretending stale work is current
- can be regenerated from repo state
- requires no model call
- requires no network call in the deterministic core
- can be checked by a read-only doctor
- plugs into the existing PLG AI/MCP tool surface
- does not create a new source of story truth

The qualitative target is:

**wide brain at rest, narrow brain in context.**
