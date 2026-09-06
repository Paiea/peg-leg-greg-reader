# Manuscript Compression Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a durable, map-first structural compression mode for Peg-Leg Greg that is ready to run after the current editor pass finishes.

**Architecture:** Keep structural compression separate from ordinary drafting and prose editing. A dedicated compression rules file defines what may be compressed, a workflow file defines map-first execution and safety gates, and a reusable prompt file provides the human-facing invocation. Existing engine/prose docs receive only small pointer sections so they do not duplicate the subsystem.

**Tech Stack:** Markdown repository state, GitHub durable authority, existing PLG manuscript/editor workflows.

**Spec:** `docs/superpowers/specs/2026-09-05-manuscript-compression-engine-design.md`

## Global Constraints

- Structural compression must not run on a manuscript range still being actively rewritten by the dialogue/voice editor.
- Default compression strength is MODERATE.
- Optimize for fewer repeated dramatic functions, not fewer chapters or words.
- Preserve mundane novelty, social accumulation, relationship memory, money/material continuity, disability/body continuity, magic evidence, object provenance, humor, and later callbacks.
- Mapping and dependency review happen before prose rewriting.
- No chapter deletion, merge execution, or renumbering before author approval of the structural map.
- NO EM DASHES in manuscript prose; editorial Markdown may use normal punctuation but should avoid introducing conflicting manuscript guidance.

---

### Task 1: Durable Compression Rules

**Files:**
- Create: `state/COMPRESSION_ENGINE.md`

**Interfaces:**
- Consumes: compression design spec and existing `state/PROSE_PLAYBOOK.md` principles.
- Produces: canonical editorial classifications KEEP / TIGHTEN / SUMMARIZE-IN-SCENE / MERGE / CUT, strength levels, preservation rules, and failure modes.

- [ ] **Step 1:** Create the rules file with purpose, core principle, classification definitions, functional-value test, repetition targets, protected material, anti-summary rule, scene-survival hierarchy, compression strengths, and success/failure tests.
- [ ] **Step 2:** Read the created file back and verify the five classifications and three strength levels are present.
- [ ] **Step 3:** Verify the file explicitly says quietness alone is not a cut reason and that later dependencies must be protected.
- [ ] **Step 4:** Commit the file.

### Task 2: Structural Compression Workflow

**Files:**
- Create: `state/STRUCTURAL_COMPRESSION_WORKFLOW.md`

**Interfaces:**
- Consumes: `state/COMPRESSION_ENGINE.md`, manuscript authority rules, chapter index/state, exact prose.
- Produces: bounded batch mapping workflow, dependency search requirements, author approval gate, execution procedure, and renumber safety rules.

- [ ] **Step 1:** Create the workflow file with preflight, recommended 10-25 chapter batches, boundary reads, dependency searches, map schema, stop-after-map gate, execution rules, QA, and renumber requirements.
- [ ] **Step 2:** Read back and verify prose rewriting is forbidden in Phase 1.
- [ ] **Step 3:** Verify CUT/MERGE requires downstream dependency review and that renumbering is deferred until the structural map is frozen and approved.
- [ ] **Step 4:** Commit the file.

### Task 3: Reusable Compression Prompt

**Files:**
- Create: `prompts/MANUSCRIPT_COMPRESSION_PASS.md`

**Interfaces:**
- Consumes: range `[START]-[END]`, optional strength, current GitHub authority, compression/workflow rules.
- Produces: map-only first pass and an author-facing proposed compressed sequence.

- [ ] **Step 1:** Create a full reusable prompt with placeholders for range and strength.
- [ ] **Step 2:** Include shorthand: `Run PLG compression map for Chapters [START]-[END] at [STRENGTH] strength from current GitHub authority.`
- [ ] **Step 3:** Require map fields: chapter/title, primary function, unique value, redundant function, downstream dependencies, classification, destination of surviving beats, risk/confidence.
- [ ] **Step 4:** Require the worker to stop after mapping and present expected gains and high-risk decisions for author approval.
- [ ] **Step 5:** Commit the prompt file.

### Task 4: Integrate with Manuscript Engine

**Files:**
- Modify: `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`

**Interfaces:**
- Consumes: dedicated compression subsystem.
- Produces: explicit separation between ordinary forward drafting/light-heavy prose editing and authorized structural compression.

- [ ] **Step 1:** Add a short `Structural compression mode` section pointing to `COMPRESSION_ENGINE.md`, `STRUCTURAL_COMPRESSION_WORKFLOW.md`, and the reusable prompt.
- [ ] **Step 2:** State that ordinary drafting/editing cannot casually merge/delete/renumber chapters.
- [ ] **Step 3:** State that structural compression waits for a frozen/current editor checkpoint and begins map-only.
- [ ] **Step 4:** Read back the modified section and surrounding rules for contradictions.
- [ ] **Step 5:** Commit the integration edit.

### Task 5: Integrate with Prose Playbook and Verify

**Files:**
- Modify: `state/PROSE_PLAYBOOK.md`

**Interfaces:**
- Consumes: existing structural compression section and dedicated subsystem.
- Produces: pointer from prose-level compression guidance to the dedicated structural workflow without duplicating its full rules.

- [ ] **Step 1:** Add a short pointer under/near structural compression saying broad merge/cut/renumber work must use the dedicated compression engine and map-first workflow.
- [ ] **Step 2:** Preserve existing rule `Cut repetition, not quietness` and heavy-pass boundaries.
- [ ] **Step 3:** Verify all five files exist on `editor/voice-compression-pass` and references use exact paths.
- [ ] **Step 4:** Verify the reusable prompt defaults to MODERATE and stops after map creation.
- [ ] **Step 5:** Commit the final integration edit and re-read the branch files as the completion check.
