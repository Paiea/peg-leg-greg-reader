# Codex Efficiency Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make R2 Codex work consume less repeated context and avoid accidental agent fan-out while keeping one strong primary Codex agent autonomous inside a bounded task.

**Architecture:** Replace the monolithic root instruction surface with a short router, strengthen the existing Codex execution policy, add a project-level subagent concurrency guardrail, add a compact Mana-to-Codex task packet, and clarify that R2 audio production parallelism is not Codex subagent fan-out.

**Tech Stack:** Markdown repository instructions, Codex `.codex/config.toml`, existing GitHub-based project authority.

**Spec:** `docs/superpowers/specs/2026-09-12-codex-efficiency-harness-design.md`

## Global Constraints

- Preserve current project and story authority.
- Do not redesign R2 audio production.
- Default to one strong primary Codex agent.
- Do not add model routing, custom roles, Best-of-N, or a new orchestration framework.
- Keep detailed lane context cold until the task enters that lane.

---

### Task 1: Compact the root worker router

**Files:**
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: existing lane/state documentation.
- Produces: a short repository entry point that routes workers without duplicating lane doctrine.

- [ ] Replace detailed lane doctrine with universal authority rules plus a compact lane routing table.
- [ ] Remove unconditional reading of `state/PROJECT_STATE.md` for every substantial task; keep it as project-wide fallback when needed.
- [ ] Route Codex jobs to `state/editorial/CODEX_EXECUTION_POLICY.md` and `state/CODEX_TASK_PACKET.md`.
- [ ] Re-read the file and verify it behaves as a map rather than a manual.

### Task 2: Strengthen Codex execution boundaries

**Files:**
- Modify: `state/editorial/CODEX_EXECUTION_POLICY.md`
- Create: `state/CODEX_TASK_PACKET.md`
- Create: `.codex/config.toml`

**Interfaces:**
- Consumes: bounded task selected by Chat/Mana.
- Produces: one-agent-by-default execution with explicit boundaries, verification, and stop condition.

- [ ] Add single-primary-agent default and explicit parallelism gate to the execution policy.
- [ ] Preserve deterministic-tools-first, no scope widening, no Best-of-N, serialized authority writes, and stop-after-verification rules.
- [ ] Add the reusable task-packet format with `PARALLELISM: NO` as the default.
- [ ] Add `[agents] max_concurrent_threads_per_session = 1` to `.codex/config.toml`.
- [ ] Re-read all three files and verify they agree.

### Task 3: Clarify R2 audio parallelism

**Files:**
- Modify: `r2/AUDIO_PRODUCTION.md`

**Interfaces:**
- Consumes: existing one-chapter-per-worker and short-take factory.
- Produces: clear separation between audio/provider concurrency and Codex subagent concurrency.

- [ ] Add a Codex-specific efficiency note near default worker behavior.
- [ ] State that independent chapter workers may be coordinated externally, but one Codex task does not spawn internal subagents by default.
- [ ] Preserve provider-side take queuing and existing chapter ownership semantics.
- [ ] Re-read the affected section to confirm no audio-production behavior was unintentionally changed.

### Task 4: Verify the pilot as one coherent harness

**Files:**
- Read: `AGENTS.md`
- Read: `state/editorial/CODEX_EXECUTION_POLICY.md`
- Read: `state/CODEX_TASK_PACKET.md`
- Read: `.codex/config.toml`
- Read: `r2/AUDIO_PRODUCTION.md`

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: a reviewable branch suitable for merging as the R2 pilot.

- [ ] Confirm all references point to files that exist.
- [ ] Confirm no instruction requires broad project-state loading for a bounded R2/reader/audio task without a reason.
- [ ] Confirm subagents require explicit authorization and concurrency is capped.
- [ ] Confirm Codex retains autonomy inside the target boundary.
- [ ] Confirm the stop condition returns control to Chat/Mana after one bounded target.
