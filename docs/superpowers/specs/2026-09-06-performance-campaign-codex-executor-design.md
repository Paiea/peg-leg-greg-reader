# PERFORMANCE Campaign Runner + Codex Execution Mode

Date: 2026-09-06
Status: design for review
Base authority: main at 5650095c4166864df352258a605a14845ebd30cf

## Purpose

Make large Peg-Leg Greg editorial jobs feel like one instruction and one integration surface even when they require hundreds or thousands of scene-level operations.

The existing PERFORMANCE production funnel remains the compiler, validation, and canon-application authority. This design adds orchestration around that existing pipeline. It does not create a new editorial lane or a second story/compiler authority.

Target user experience:

```text
run reverse-edit campaign across canon 1:491
```

The backend should compile the scope, reuse valid cached cognition, create only the model packets that still need work, execute those packets under a bounded Codex policy, reduce hundreds of results into one compact campaign result, escalate only the few hard cases that deserve stronger judgment, and apply surviving canon patches sequentially through the existing fail-closed patch path.

The goal is not to pretend 491 chapters contain one chapter's worth of information. The goal is to make orchestration overhead approach constant for the human while information processing remains scene-granular and cacheable.

## Existing authority and non-negotiable boundaries

1. CANON PROSE remains the only story authority.
2. `scripts/performance_production_funnel.py` remains the semantic contract owner for scene compilation, provenance-aware derived state, task views, screenplay/comparison records, and canon-safe patch application.
3. Stable scene IDs and source/dependency hashes remain the unit of cache validity.
4. Existing successful PERFORMANCE archives remain historical/golden evidence until a later replacement audit proves a stronger representation can supersede them.
5. Codex execution mode is an execution policy, not a new lane.
6. Chat remains the preferred creative/design surface. Codex campaign workers are execution-biased by default.
7. Parallel workers may generate derived analysis and candidate outputs, but they do not concurrently mutate canon.
8. No mechanism may bypass subscription, authentication, quota, credit, sandbox, or permission boundaries. The runner uses only execution capacity legitimately available to the configured Codex/API environment.

## Approaches considered

### A. Let one Codex agent manage all parallelism itself

Advantages:
- minimal repo code
- easy to start

Problems:
- agent spends reasoning tokens rediscovering scheduling state
- weak resume/retry semantics
- easy scope creep
- hard to know which results are cacheable
- difficult to stop duplicate workers quickly
- the agent becomes both editor and distributed-systems scheduler

Rejected as the default.

### B. Runner-owned campaign orchestration with Codex workers

Advantages:
- deterministic scheduling and stop conditions
- one user command can fan out over the full manuscript
- exact cache checks happen before any model work
- worker prompts stay narrow and schema-bound
- bounded concurrency, retries, and escalation
- reducer can collapse hundreds of results before expensive review
- later executors can plug into the same campaign format

Recommended.

### C. API Batch-first orchestration

Advantages:
- excellent economics for very large asynchronous inference campaigns
- high request volume and simple JSONL fan-out

Problems:
- introduces separate API billing/auth immediately
- less aligned with the user's current Plus/Codex workflow
- unnecessary before the campaign contract proves itself

Deferred as a later executor adapter. The campaign schema should not prevent adding it.

## Architecture

```text
USER / CHAT
  |
  | one approved campaign instruction
  v
CAMPAIGN RUNNER
  |
  +--> authority lock / source SHA
  +--> scope resolution
  +--> compile/reuse scene records through existing PERFORMANCE funnel
  +--> rebuild/query disposable project index
  +--> determine cache hits and missing stages
  +--> build narrow worker packets
  |
  v
RUNNER-OWNED EXECUTOR
  |
  +--> deterministic-only jobs: local Python
  +--> model jobs: bounded `codex exec` workers
  +--> future optional executor: API Batch
  |
  v
READ-ONLY / DERIVED MAP RESULTS
  |
  v
REDUCER
  |
  +--> source wins disappear from review surface
  +--> duplicate/systemic findings collapse
  +--> ambiguities/conflicts group together
  +--> strong candidates ranked
  |
  v
ESCALATION GATE
  |
  +--> only genuinely difficult candidates receive stronger reasoning
  |
  v
SEQUENTIAL INTEGRATION
  |
  +--> re-check current authority
  +--> exact-anchor / stale checks
  +--> apply surviving patches through existing funnel
  +--> tests / archive earned evidence
  v
ONE CAMPAIGN RESULT / PR
```

## Campaign contract

A campaign is disposable execution control, not story state.

Conceptual schema:

```json
{
  "schema": "performance_campaign/v1",
  "campaign_id": "reverse-edit-001-491-<source-short-sha>",
  "task": "reverse_edit",
  "source_authority": "<git-sha>",
  "scope": {
    "chapters": {"start": 1, "end": 491},
    "canon_not_showcase": true
  },
  "execution": {
    "profile": "eco",
    "executor": "codex",
    "creative_authority": false,
    "canon_write_parallelism": 0,
    "max_worker_retries": 1,
    "stop_on_authority_drift": true
  },
  "stages": [
    "compile",
    "semantic",
    "performance",
    "screenplay",
    "compare",
    "reduce",
    "escalate",
    "integrate"
  ]
}
```

The runner resolves the campaign into scene packets after deterministic compilation. Packet identity includes source hash, compiler/pass version, task view, and dependencies. If an identical valid result already exists, the worker is never launched.

## Codex execution policy

Codex campaign mode is deliberately execution-biased.

Default policy:

1. Execute the approved campaign. Do not redesign the project.
2. Prefer deterministic repo tools before model reasoning.
3. Reuse valid cached results before launching work.
4. Do not invent new editorial doctrine, systems, lanes, or cleanup projects.
5. Do not widen chapter/task scope unless the campaign contract explicitly allows it.
6. Fix a blocking implementation defect only when necessary to complete the campaign and when the fix stays inside the approved architecture.
7. When a design/authority conflict is material, stop that packet and return a structured escalation instead of improvising.
8. Do not perform adjacent research/web work unless the packet explicitly requires it.
9. Do not use Best-of-N or duplicate model attempts by default.
10. One retry maximum for ordinary worker failure. Retry only when the failure class is transient or structurally correctable.
11. Return schema-bound output, not a long prose recap.
12. Halt when the requested durable boundary is verified. Do not continue into adjacent optimization or cleanup.

The durable policy may live in a compact project file referenced by `AGENTS.md`, while the campaign runner injects the critical packet-specific constraints directly into each non-interactive worker prompt. This avoids bloating mandatory root context.

## Runner-owned concurrency

Parallelism is an execution property of the runner, never a judgment left to each worker.

Key rules:

- Deterministic compilation/indexing may use ordinary local process/thread concurrency where safe.
- Model workers operate on independent source-addressed scene packets.
- Model map workers are read-only with respect to canon.
- Worker outputs are written only to campaign-local derived storage.
- Canon mutation concurrency is always zero. Surviving patches are applied sequentially after reduction.
- A packet is not scheduled when its required derived layer is cache-valid.
- Failed packets do not cause the entire campaign to restart.
- No unbounded retry loops.
- Concurrency must be configurable and conservative by default because more simultaneous Codex workers increase rate/usage pressure without reducing total cognition.

Recommended initial profiles:

```text
eco      model_workers=2   retries=1   no duplicate attempts
standard model_workers=4   retries=1   no duplicate attempts
burst    explicit-only; higher concurrency for speed, not lower usage
```

The exact worker count is configuration, not story authority. `eco` is the default.

## Codex worker invocation

Initial Codex executor target: non-interactive Codex CLI.

Conceptually:

```text
codex exec --ephemeral <schema-bound packet prompt>
```

The implementation should use structured output/schema support when available rather than scraping narrative terminal prose.

Each worker receives only:

- campaign/packet ID
- exact source authority and scene pointer
- the narrow compiler view required for its stage
- exact source prose only when the stage genuinely needs it
- immutable relevant constraints
- output schema
- stop conditions

Workers should not receive giant batch manifests, unrelated chapters, or broad project files merely because they exist.

Model name/reasoning tier must remain configuration. Do not hardcode a model that will become stale. The runner may support a cheap/default tier and an explicit escalation tier, but executor capabilities determine the actual model names.

## Rebuildable project index

Add a disposable SQLite index over compiler/project state. It is a retrieval accelerator, never authority.

Suggested local path:

```text
.cache/plg/project-index.sqlite
```

It must be ignored by Git and fully rebuildable from current repo authority.

Initial indexed fields should include only proven useful retrieval keys:

- scene_id
- canonical chapter
- source hash
- paragraph span / anchors
- compiler/cache status
- capitalized/entity-like tokens
- dialogue metrics
- money mentions
- semantic character/location/object fields when available
- performance/comparison status
- conflict/escalation status
- illustration/reference status only when a reliable join already exists

SQLite FTS may index exact scene prose and selected derived text for fast local retrieval. Do not add embeddings/vector infrastructure until structured queries + FTS prove insufficient.

The index exists so an AI worker can ask for a narrow set of scene IDs/records instead of scanning hundreds of files. Deleting it must never destroy project knowledge.

## Campaign-local storage

Do not commit thousands of disposable screenplay or worker-output files to the repository.

Default local layout:

```text
.cache/plg/campaigns/<campaign-id>/
  campaign.json
  packets.jsonl
  results.jsonl
  reducer.json
  failures.jsonl
  summary.json
```

This storage is disposable and resumable within the execution workspace.

Durable promotion rules:

- SOURCE WIN: no durable heavy artifact by default.
- ordinary generated screenplay: disposable.
- accepted canon patch: normal Git diff + validation.
- successful PERFORMANCE roundtrip that earns lasting prose change: preserve evidence using the existing roundtrip/archive authority until a future replacement audit changes that contract.
- systemic lesson/new doctrine: never auto-promote from a campaign; require explicit design/editorial judgment.

A future GitHub Actions-artifact adapter may preserve large disposable campaign outputs across machines without committing them to Git. That is not required for the first implementation.

## Worker packet model

Each packet is independently retryable and addressable.

Conceptual packet:

```json
{
  "packet_id": "214.s020:performance:<dependency-hash>",
  "scene_id": "214.s020",
  "stage": "performance",
  "source_hash": "...",
  "dependency_hash": "...",
  "view": "performance",
  "creative_authority": false,
  "write_authority": "derived_only",
  "output_schema": "performance_claims/v1"
}
```

The prompt compiler may expand this with the exact narrow view and required source slice. Packet files should not duplicate giant source text when the runner can materialize it just-in-time.

## Reducer

The reducer is a first-class stage because the human/strong-model interface should not be 1,000 worker reports.

For a reverse-edit campaign it should emit compact aggregate state such as:

```json
{
  "scenes_considered": 1086,
  "cache_hits": 742,
  "workers_launched": 344,
  "source_wins": 287,
  "performance_candidates": 46,
  "ambiguous": 11,
  "systemic_clusters": 5,
  "escalated": 23,
  "surviving_patches": 8,
  "failures": 2
}
```

It should also provide the exact scene IDs and bounded evidence for candidates/failures.

The reducer may cluster repeated issues by deterministic keys or cheap classification, but it must not silently convert repeated observations into new editorial doctrine.

## Escalation

A worker should escalate instead of improvising when:

- current authority no longer matches campaign source SHA
- exact scene/source anchors are stale
- semantic provenance conflicts materially affect the task
- a requested change would alter plot/canon/character intent outside approved editorial authority
- two candidate patches overlap incompatibly
- a systemic issue appears to require a new rule or architecture
- a worker cannot satisfy its schema after the bounded retry

Escalated items are grouped for one stronger review pass rather than starting independent conversations.

## Authority drift and resumability

The campaign locks the source authority SHA at planning time.

If `main` moves during read-only map work, existing packet results remain historical derived results keyed to their source hashes. Before integration, the runner recompiles/revalidates affected scenes against current authority.

If a scene hash is unchanged, the result may still be reusable.
If a scene hash changed, stale derived results are not applied.

The entire campaign must not be thrown away merely because unrelated `main` files changed.

## One-command UX

Initial CLI should optimize for the user's desired interaction:

```text
python scripts/performance_campaign.py run \
  --task reverse-edit \
  --chapters 1:491 \
  --profile eco \
  --executor codex
```

Also useful:

```text
... plan              # compile/index and show expected work without model calls
... run --resume ID   # continue incomplete campaign-local work
... status ID         # one compact campaign summary
... reduce ID         # recompute summary from existing results without model work
... integrate ID      # sequentially validate/apply only authorized survivors
```

`plan` must be cheap and should show the number of scenes, cache hits, model packets, and estimated job count before model execution begins.

## Usage discipline

Usage efficiency is a design requirement, not a prompt preference.

The runner should make waste structurally difficult:

1. no model call for deterministic extraction
2. no model call for a cache hit
3. no duplicate worker attempts by default
4. no giant full-book prompt when scene packets suffice
5. no parallel canon writers
6. no automatic adjacent cleanup
7. no automatic Best-of-N
8. bounded retries
9. narrow structured outputs
10. reducer before strong-model review
11. halt at verified campaign boundary

The first implementation does not need to know the user's live Codex subscription quota. It controls *work count and duplication*, which are repo-level facts. If a future supported usage API exists, it can become an optional budget signal; do not scrape or bypass account limits.

## Relationship to Chat

Preferred split:

### Chat
- taste
- invention
- story direction
- architecture
- deciding what campaign should run
- reviewing systemic findings
- approving risky canon or doctrine changes

### Codex campaign mode
- compile
- query
- execute approved transforms
- test
- validate
- fan out bounded work
- reduce results
- fix execution-blocking defects inside approved scope
- stop

Creative Codex work is allowed only when explicitly requested by the task. It is not the campaign default.

## Relationship to other PLG systems

The campaign runner should become shared execution plumbing only when another existing PLG task can consume the same compiler/index/query primitives without losing domain-specific authority.

Examples:

- dialogue audit campaign can request dialogue views
- continuity campaign can request continuity views
- illustration reconciliation can query scene/cast/object state where the join is reliable
- compression/performance campaigns can reuse semantic/performance cache

Do not centralize project-specific judgment merely because orchestration is shared.

Replacement remains evidence-first:

```text
prove new primitive -> reroute consumer -> verify parity/improvement -> preserve unique residue -> retire duplicate mechanism
```

No deletion is authorized by this design alone.

## Testing requirements

The implementation must prove at least:

1. planning a 1:491 campaign does not mutate canon
2. unchanged scenes become cache hits and do not launch workers
3. changing one scene invalidates only dependent packets for that scene
4. runner concurrency never permits concurrent canon writes
5. worker failures are bounded and individually retryable
6. stale source authority blocks integration, not read-only historical result retention
7. reducer output is deterministic given identical result inputs
8. resume does not rerun successful cache-valid packets
9. SQLite index can be deleted/rebuilt with equivalent query results
10. Codex worker prompts are narrow, scope-locked, and schema-bound
11. SOURCE WIN results remain lightweight
12. successful survivors still pass existing exact-anchor / no-em-dash / repository validation gates
13. normal campaign validation leaves the repository clean

## First implementation boundary

Implement enough to make a real local Codex campaign possible without introducing new external services:

1. campaign schema + plan/resume/status/reduce lifecycle
2. compile-range support using the existing PERFORMANCE scene compiler
3. rebuildable SQLite/FTS index
4. packet planner with cache-aware scheduling
5. runner-owned bounded concurrency
6. non-interactive Codex executor adapter with structured result contract
7. read-only parallel map stage
8. deterministic reducer
9. sequential integration gate that delegates to the existing canon patch machinery
10. compact Codex execution policy referenced by project routing
11. tests proving usage/authority boundaries

Defer:

- OpenAI API Batch executor
- vector database
- automatic model-budget/credit scraping
- generic cross-project framework extraction
- autonomous doctrine creation
- background daemon/scheduler
- automatic deletion of older systems

## Success criteria

This design succeeds when the user can give one approved whole-manuscript instruction and the system:

- expands it to scene-level work without human micromanagement
- spends zero model work on deterministic/cache-valid operations
- uses bounded Codex workers only for missing cognition
- keeps parallel work derived/read-only
- reduces the campaign to a compact decision surface
- applies accepted changes sequentially and fail-closed
- leaves one understandable result instead of hundreds of chat-sized jobs
- stops when finished

The qualitative target is: **one instruction, many cheap packets, one reduced result, one safe integration path.**
