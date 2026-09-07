# PERFORMANCE AI Tool Surface + Campaign Telemetry

Date: 2026-09-06
Status: approved extension
Parent spec: `docs/superpowers/specs/2026-09-06-performance-campaign-codex-executor-design.md`

## Purpose

Complete the six-tool PLG operating stack without creating another editorial subsystem. The existing PERFORMANCE compiler remains authority for scene compilation and canon-safe application. The campaign runner remains orchestration authority. This extension adds only a stable AI-facing interface over those operations and evidence-based cost/effectiveness telemetry.

## AI-native interface

Expose the stable repo operations as both importable Python functions and a thin MCP stdio server. The MCP server is an adapter, not a second implementation.

Initial tool names:

- `compile_range`
- `get_scene_view`
- `query_scenes`
- `plan_campaign`
- `run_campaign`
- `get_campaign_result`
- `reduce_campaign`
- `apply_survivors`

All tools return structured JSON-compatible objects. They must call the same Python functions used by the CLI. No tool may contain independent story/editorial logic.

Read operations are model-safe by default. `apply_survivors` is the only canon-writing AI tool and must remain fail-closed: sequential integration only, exact source/anchor validation, current-authority recheck, and existing repository validation. The adapter must identify it as destructive/write-capable in metadata where the host supports annotations.

Use the official current MCP Python SDK v2 through an optional tools dependency. Core compiler/campaign functionality must not require MCP to be installed.

## Resolver/query contract

The project index should let an agent resolve work without knowing paths. Queries support:

- exact scene ID
- free-text FTS search over source + selected derived text
- chapter range
- character/entity-like token
- money mention
- stage/cache status
- comparison verdict/conflict status

`query_scenes` returns compact scene pointers first. Exact source prose or task views are fetched separately. This preserves the wide-at-rest / narrow-in-context rule.

## Telemetry

Every campaign maintains append-only local telemetry at:

`.cache/plg/campaigns/<campaign-id>/telemetry.jsonl`

and a rebuildable aggregate in `summary.json`.

Record events for:

- campaign planned/started/completed
- packet cache hit/miss
- worker launch/completion/failure/retry
- executor + configured model/reasoning tier
- elapsed milliseconds
- reported input/output/cached tokens when the executor exposes them
- source win / performance candidate / ambiguous result
- escalation
- surviving patch
- integration rejection/staleness

Never invent token counts. Unknown usage remains null.

Derived campaign metrics include:

- scenes considered
- cache hit rate
- workers launched
- retry/failure rate
- source win rate
- candidate rate
- escalation rate
- survivor rate
- elapsed worker time
- reported tokens/cost when available
- useful-survivor-per-worker ratio

The first version does not scrape ChatGPT/Codex account quota or attempt to infer hidden subscription consumption.

## Compute routing

Routing is configuration, not story authority.

Default order:

1. deterministic local code
2. valid cache
3. optional configured local executor for low-risk stages
4. Codex default executor
5. explicit stronger/escalation executor only for unresolved hard cases

If no local executor is configured, skip it. Do not install or download models automatically.

## Replacement evidence

Telemetry exists partly to support later cleanup. A duplicate older mechanism may only be retired after campaign evidence shows the shared primitive has equal or better coverage/quality and preserves unique residue. This design does not authorize deletion by itself.

## Testing

Prove:

1. MCP and CLI call the same underlying functions.
2. The core campaign runner works without the MCP dependency installed.
3. Read tools never mutate canon.
4. `apply_survivors` delegates to the sequential integration gate.
5. Query results are reproducible after deleting/rebuilding SQLite.
6. Telemetry is append-only and aggregate metrics are deterministic.
7. Missing executor usage fields remain null rather than guessed.
8. Cache hits are counted and do not launch workers.
9. A campaign summary can compare executor effectiveness without loading every raw result.

## Success criterion

A future Chat/Codex worker should be able to operate PLG through a handful of stable tool calls rather than discover file layout manually, while the user can judge campaign cost/effectiveness from one compact result.