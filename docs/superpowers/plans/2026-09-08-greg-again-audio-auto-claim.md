# Greg, Again Audio Auto-Claim Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make fresh Greg, Again audio chats auto-claim the next available non-overlapping chapter batch from GitHub authority without requiring manually assigned ranges.

**Architecture:** Use GitHub branch creation as the durable claim operation rather than a shared mutable queue file. Route fresh workers through one audio production protocol that derives completed chapters, live WIP, written frontier, and the next claim from current GitHub state, while preserving existing per-chapter audio branches during transition.

**Tech Stack:** GitHub repository state, Markdown operating protocols, existing Greg, Again audio manifest and branch/PR workflow.

**Spec:** `docs/superpowers/specs/2026-09-08-greg-again-audio-auto-claim-design.md`

## Global Constraints

- Default new batch size is 3 chapters.
- New protocol-native claims use `audio/greg-again-batch-NNN-MMM`.
- Existing per-chapter audio branches remain valid WIP and reserve their exact chapter.
- Never claim beyond the current written frontier.
- Never steal or force-update another worker's claim.
- Current GitHub authority outranks stale prompts and branch copies.
- Preserve current narrator, Shared Greg Surface, processing-space, pronunciation, assembly, and verification doctrine.
- Do not add a queue database, scheduler, daemon, or new application subsystem.

---

### Task 1: Add durable audio production protocol

**Files:**
- Create: `state/experiments/greg-again/audio/PRODUCTION.md`

**Interfaces:**
- Consumes: `greg-again/audio/manifest.json`, current written Greg, Again authority, active audio branches/PRs, `state/experiments/greg-again/audio/narrator.md`, `state/experiments/greg-again/audio/pronunciation.json`
- Produces: deterministic auto-claim and production rules for fresh audio workers

- [ ] **Step 1:** Write `PRODUCTION.md` with authority inputs, availability algorithm, branch-as-claim naming, transition handling, provider queueing, shared-file reconciliation, verification, completion, and minimal restart prompt.
- [ ] **Step 2:** Fetch the file back and verify the default batch size, branch naming, existing-branch compatibility, no-steal rule, and current audio doctrine references are present.
- [ ] **Step 3:** Commit as part of the implementation branch history.

### Task 2: Route fresh workers from root AGENTS

**Files:**
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `state/experiments/greg-again/audio/PRODUCTION.md`
- Produces: a stable Greg, Again Audio lane entry for fresh repository-aware workers

- [ ] **Step 1:** Add a compact `Greg, Again Audio` lane section that points workers to the production protocol and requires auto-claim before synthesis when no explicit range is assigned.
- [ ] **Step 2:** Preserve all existing lane/router content verbatim outside the new localized section.
- [ ] **Step 3:** Fetch the updated file and verify the new route appears exactly once.

### Task 3: Add minimal audio handshake

**Files:**
- Modify: `state/HANDSHAKE_PROTOCOL.md`

**Interfaces:**
- Consumes: audio production protocol
- Produces: human-light starter prompt for disposable parallel audio workers

- [ ] **Step 1:** Add a `Greg, Again audio re-prompt` section containing the compact auto-claim starter.
- [ ] **Step 2:** Preserve existing handshake semantics and all other lane prompts.
- [ ] **Step 3:** Fetch the updated file and verify the starter appears exactly once.

### Task 4: Verify integration against current main

**Files:**
- Verify only: implementation branch vs `main`

**Interfaces:**
- Consumes: completed Tasks 1-3
- Produces: evidence that only intended routing/protocol files changed and no live audio worker branch was touched

- [ ] **Step 1:** Compare implementation branch with current `main`.
- [ ] **Step 2:** Confirm changed files are limited to `AGENTS.md`, `state/HANDSHAKE_PROTOCOL.md`, and `state/experiments/greg-again/audio/PRODUCTION.md` plus approved spec/plan docs if intentionally carried.
- [ ] **Step 3:** Re-scan active `audio/greg-again-*` branches and confirm existing Chapter 8/9 WIP remains untouched.
- [ ] **Step 4:** Open a PR to `main` with a compact migration note explaining that pre-protocol workers continue normally and new workers auto-claim.
