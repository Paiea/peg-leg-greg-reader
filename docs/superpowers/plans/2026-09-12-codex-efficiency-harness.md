# Codex Efficiency Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make R2 Codex work consume less repeated context and avoid accidental agent fan-out while keeping one strong primary Codex agent autonomous inside a bounded task and preserving reusable expert method when earned.

**Architecture:** Replace the monolithic root instruction surface with a short router, strengthen the existing Codex execution policy, add a project-level spawned-agent concurrency guardrail, add a compact Mana-to-Codex task packet with expert residue, and layer R2-specific Codex efficiency rules in a small overlay instead of bloating the base audio protocol.

**Tech Stack:** Markdown repository instructions, Codex `.codex/config.toml`, existing GitHub-based project authority.

**Spec:** `docs/superpowers/specs/2026-09-12-codex-efficiency-harness-design.md`

## Global Constraints

- Preserve current project and story authority.
- Do not redesign R2 audio production.
- Default to one strong primary Codex agent.
- Do not add model routing, custom roles, Best-of-N, or a new orchestration framework.
- Keep detailed lane context cold until the task enters that lane.
- Preserve reusable method, not chain-of-thought or work diaries.

---

### Task 1: Compact the root worker router

**Files:**
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: existing lane/state documentation.
- Produces: a short repository entry point that routes workers without duplicating lane doctrine.

- [x] Replace detailed lane doctrine with universal authority rules plus a compact lane routing table.
- [x] Remove unconditional reading of `state/PROJECT_STATE.md` for every substantial task; keep it as project-wide fallback when needed.
- [x] Route Codex jobs to `state/editorial/CODEX_EXECUTION_POLICY.md` and `state/CODEX_TASK_PACKET.md`.
- [x] Route Codex R2 audio work through `r2/CODEX_AUDIO_EFFICIENCY.md`.

### Task 2: Strengthen Codex execution boundaries

**Files:**
- Modify: `state/editorial/CODEX_EXECUTION_POLICY.md`
- Create: `state/CODEX_TASK_PACKET.md`
- Create: `.codex/config.toml`

**Interfaces:**
- Consumes: bounded task selected by Chat/Mana.
- Produces: single-primary-agent-by-default execution with explicit boundaries, verification, stop condition, and compact reusable expert residue.

- [x] Add single-primary-agent default and explicit parallelism gate to the execution policy.
- [x] Preserve deterministic-tools-first, no scope widening, no Best-of-N, serialized authority writes, and stop-after-verification rules.
- [x] Add the reusable task-packet format with `PARALLELISM: NO` and `RESIDUE: COMPACT` defaults.
- [x] Add compact expert-recipe behavior and durable-playbook option when a method is genuinely reusable.
- [x] Add `[agents] max_concurrent_threads_per_session = 1` to `.codex/config.toml`.

### Task 3: Layer R2 audio efficiency without changing audio semantics

**Files:**
- Create: `r2/CODEX_AUDIO_EFFICIENCY.md`
- Preserve unchanged: `r2/AUDIO_PRODUCTION.md`

**Interfaces:**
- Consumes: existing one-chapter-per-worker and short-take factory.
- Produces: Codex-only clarification separating project-level worker concurrency, provider/take concurrency, and Codex subagent concurrency.

- [x] Add the Codex-specific overlay instead of expanding the base audio protocol.
- [x] State that independent chapter workers may be coordinated externally, but one Codex task does not spawn internal subagents by default.
- [x] Preserve provider-side take queuing and existing chapter ownership semantics.
- [x] Keep unrelated R2/manuscript/editorial context cold.

### Task 4: Verify the pilot as one coherent harness

**Files:**
- Read: `AGENTS.md`
- Read: `state/editorial/CODEX_EXECUTION_POLICY.md`
- Read: `state/CODEX_TASK_PACKET.md`
- Read: `.codex/config.toml`
- Read: `r2/CODEX_AUDIO_EFFICIENCY.md`
- Read: `docs/superpowers/specs/2026-09-12-codex-efficiency-harness-design.md`

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: a reviewable branch suitable for merging as the R2 pilot.

- [ ] Confirm all references point to files that exist.
- [ ] Confirm root `AGENTS.md` routes rather than duplicating detailed lane doctrine.
- [ ] Confirm no instruction requires broad project-state loading for a bounded R2/reader/audio task without a reason.
- [ ] Confirm subagents require explicit authorization and spawned-agent concurrency is capped.
- [ ] Confirm Codex retains autonomy inside the target boundary.
- [ ] Confirm the stop condition returns control to Chat/Mana after one bounded target.
- [ ] Confirm compact reusable expert residue is conditional and does not create documentation spam.
