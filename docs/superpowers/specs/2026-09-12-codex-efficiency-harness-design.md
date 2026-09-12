# Codex Efficiency Harness Design

## Goal

Reduce Codex allowance burn without reducing the quality or autonomy of the primary coding agent.

The system should spend broad reasoning in Chat/Mana, compile that reasoning into one bounded implementation target, let one strong Codex agent own that target, verify the result, then return control to Chat before expanding scope.

## Problem

The repository accumulated a large root `AGENTS.md`, lane-specific instructions, campaign rules, and production protocols. This made the project highly reconstructible, but it also increased the amount of context a fresh coding agent could load before doing useful work.

R2 audio also intentionally evolved toward parallel production. That is useful for independent chapter production, but the wording can be misread as permission for one Codex session to spawn an internal agent army. On a scarce Plus allowance, that is the wrong default.

The repository already contains most of the right ideas in `state/editorial/CODEX_EXECUTION_POLICY.md`: bounded jobs, deterministic tools first, no Best-of-N by default, narrow authority, and stop after verification. The fix is to make those rules easier to reach and harder to accidentally override.

## Architecture

Use layered context instead of one monolithic brain.

A Codex task should normally compose only these layers:

1. **Root router** - universal authority and where to look next.
2. **Lane layer** - only the docs for the current subsystem.
3. **Task packet** - one bounded target, boundaries, reuse requirements, and verification.
4. **Verification layer** - tests/build/checks proving the target works.

This is intentionally compositional. Do not load every durable project fact merely because it exists.

## Root router

`AGENTS.md` becomes a short map, not project memory.

It should contain:

- current-GitHub-first authority
- exact-source-over-summary rule
- preserve newer work
- branch/main posture
- cold-context rule
- lane routing table
- Codex execution pointer
- compact handoff rule

It should not repeat the detailed operating doctrine of every lane.

`state/PROJECT_STATE.md` remains durable project state, but bounded tasks should not be forced to read it when their lane has enough authority locally.

## Codex execution policy

The existing Codex policy is strengthened around one principle:

> One strong primary agent by default. Parallel agents are an explicit exception.

Subagents may be used only when the task packet explicitly authorizes parallelism and the work is genuinely independent. Tightly coupled work, architecture decisions, and one coherent investigation stay with the primary agent.

The primary agent is not micromanaged. Inside the approved boundary it may inspect, edit multiple files, debug, test, and iterate as needed.

## Project Codex configuration

Add `.codex/config.toml` with a conservative subagent concurrency cap:

```toml
[agents]
max_concurrent_threads_per_session = 1
```

This is a guardrail, not the main policy. The instruction layer still says not to spawn a subagent unless explicitly authorized. The cap merely prevents a single project session from fanning out into several concurrent child threads by accident.

Do not add model routing, custom roles, Best-of-N, or a new orchestration framework in this pilot.

## Task packet

Add one compact reusable task-packet specification for Chat/Mana to hand to Codex.

Required fields:

- TARGET
- WHY THIS TARGET
- AUTHORITY
- REUSE
- BOUNDARY
- IMPLEMENT
- VERIFY
- STOP

Optional field:

- PARALLELISM, default `NO`

The packet should explicitly permit the primary agent to do whatever is technically necessary inside the boundary while preventing adjacent redesign.

## R2 audio clarification

R2 audio's one-chapter-per-worker model remains valid for externally coordinated production.

Clarify that "many parallel workers" does not mean one Codex task should spawn many subagents. A Codex session handling one chapter or one pipeline improvement should remain single-agent unless the task packet explicitly authorizes independent sidecars.

Provider-side take concurrency remains separate from Codex-agent concurrency. Independent voice-generation requests may still be queued aggressively when the provider permits it.

## Verification

This pilot changes instructions/configuration, not product behavior.

Verify by:

- re-reading the branch versions of all changed files
- confirming root `AGENTS.md` is materially smaller and routes rather than duplicates
- confirming `.codex/config.toml` is valid TOML and uses the documented `[agents].max_concurrent_threads_per_session` key
- confirming the Codex policy says single-agent by default and explicit parallel authorization only
- confirming R2 audio distinguishes provider/task parallelism from Codex subagent fan-out
- confirming the task packet has a hard STOP condition

## Out of scope

- redesigning R2 audio production
- changing story doctrine
- changing current audio manifests or assets
- custom model-selection infrastructure
- disabling Codex autonomy inside a bounded target
- optimizing Chat/Mana context storage in this repository
- applying the pattern automatically to every other repository

The R2 pilot should prove the pattern first.