# Single-Chat Manuscript Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make normal 01 forward manuscript production a per-chapter GitHub transaction that can resume from any chat using a tiny starter prompt.

**Architecture:** Keep exact prose in the permanent running manuscript, current position and next trailhead in `MANUSCRIPT_STATE.md`, and method/workflow rules in the existing engine docs. Remove the contradictory 3-5 chapter default, add an explicit recovery rule for chat/GitHub mismatches, and make large chat handoffs optional when the next edge is already durable.

**Tech Stack:** Markdown repository state and workflow files, GitHub commits.

**Spec:** `docs/superpowers/specs/2026-09-01-single-chat-manuscript-engine-design.md`

## Global Constraints

- GitHub `main` remains accepted authority.
- Exact manuscript prose outranks summaries and chat residue.
- Do not create a parallel manuscript or new per-chapter state-file family.
- Normal forward production writes one complete chapter at a time and commits it before advancing.
- Broad/risky work still uses branches.

---

### Task 1: Align Manuscript Engine Method

**Files:**
- Modify: `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`

**Interfaces:**
- Consumes: existing 01 authority hierarchy and verification rules.
- Produces: explicit single-chat reconstruction, per-chapter completion boundary, mismatch recovery, compact receipt behavior.

- [x] **Step 1: Add the chat-independence rule**
- [x] **Step 2: Make one chapter the default durable transaction**
- [x] **Step 3: Add mismatch recovery**
- [x] **Step 4: Tighten completion receipt**
- [x] **Step 5: Review the file for contradiction**

### Task 2: Align Workflow and Project Routing

**Files:**
- Modify: `state/MANUSCRIPT_WORKFLOW.md`
- Modify: `state/PROJECT_STATE.md`
- Modify: `AGENTS.md`
- Modify: `state/HANDSHAKE_PROTOCOL.md`

**Interfaces:**
- Consumes: Task 1's completion model.
- Produces: one consistent repo-wide route into the Manuscript Engine.

- [x] **Step 1: Replace the 3-5 chapter shipping default**
- [x] **Step 2: Update forward-production routing**
- [x] **Step 3: Update root Manuscript lane guidance**
- [x] **Step 4: Simplify handshake expectations for 01**
- [x] **Step 5: Validate fresh-chat success path**

### Task 3: Commit and Verify Architecture

**Files:**
- Create: `docs/superpowers/specs/2026-09-01-single-chat-manuscript-engine-design.md`
- Create: `docs/superpowers/plans/2026-09-01-single-chat-manuscript-engine.md`
- Modify: the five routing/method files above.

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces: durable accepted process on `main`.

- [x] **Step 1: Commit the complete documentation transaction**
- [ ] **Step 2: Re-read current main**
- [ ] **Step 3: Report the new operating command**
