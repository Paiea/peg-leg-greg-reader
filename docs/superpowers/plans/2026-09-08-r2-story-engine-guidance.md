# R2 Story Engine Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the Greg, Again / R2 local story engine compact durable guidance from the approved multi-year magic/rank/party rehearsals without preselecting future chapters.

**Architecture:** Keep heavy long-range material cold in the existing pressure/rehearsal files. Add one compact story-engine guide containing generative priors that local chapter search can actually inherit, then route it through the shared Greg current state and written debrief guardrails. Preserve newest chapter-frontier authority and do not modify prose.

**Tech Stack:** Markdown state / guidance files in GitHub.

**Spec:** `state/experiments/greg-again/written/LONG_RANGE_PRESSURE_MAP.md` and `state/experiments/greg-again/written/LONG_RANGE_REHEARSAL_002_MAGIC_RANK.md`

## Global Constraints

- Do not write the next chapter.
- Current selected prose remains local story authority.
- Local chapter selection begins with **WHAT SHOULD ACTUALLY HAPPEN NEXT?**
- R2 may plausibly span roughly 500 chapters across approximately 5–10 years; this is permission, not schedule.
- Only the permanent LEFT lower-leg loss with knee preserved is a hard long-range attractor.
- Keep Ranker titles authority-conferred; do not invent Crown bureaucracy before prose earns it.
- Preserve concurrent Chapter 23+ authority rather than restoring an older frontier.

---

### Task 1: Add compact story-engine priors

**Files:**
- Create: `state/experiments/greg-again/written/STORY_ENGINE_GUIDE.md`

**Interfaces:**
- Consumes: current selected story state plus the two long-range rehearsal files.
- Produces: a compact optional boot guide for local story search.

- [x] **Step 1: Write the guide**

Included durable priors for clean wins, multidimensional magic, Barrier geometry, non-Barrier magic, honest higher-rank competence, separate Ranker status, authority-granted titles, recurring field people, emergent party structure, strategic artifacts, expanded geography/time, future-history people, and ordinary life under widening fantasy scale.

- [x] **Step 2: Add explicit anti-queue rule**

The guide explicitly rejects turning `show Gold`, `unlock spell`, `find artifact`, `form party`, `meet future Ranker`, underground work, leg loss, or theatre into automatic next-chapter assignments.

- [x] **Step 3: Commit**

Implemented in `story: add compact R2 story-engine guide`.

### Task 2: Route the written engine through the compact guide

**Files:**
- Modify: `state/experiments/greg-again/CURRENT.md`
- Preserve: `state/experiments/greg-again/written/CURRENT.md`

**Interfaces:**
- Consumes: `STORY_ENGINE_GUIDE.md`.
- Produces: local writer routing that sees the counterweights without booting the full long-range files every chapter.

**Execution adjustment:** while this task was active, another story worker advanced `written/CURRENT.md` through Chapter 23. Replacing that large live frontier file would create unnecessary stale-whole-file overwrite risk. The written lane already declares `state/experiments/greg-again/CURRENT.md` as cross-lane authority and already boots `DEBRIEF_GUARDRAILS.md`, so routing was added through those safer existing paths instead. The newer Chapter 23 frontier was left untouched.

- [x] **Step 1: Re-fetch newest CURRENT**

Confirmed selected frontier had advanced through Chapter 23 and preserved it.

- [x] **Step 2: Preserve the horizon correction without stale overwrite**

The shared current routing now states the 5–10 year permission horizon, and the live written frontier already contains a newer explicit horizon-correction section that retires the one-year assumption.

- [x] **Step 3: Add story-engine guide routing**

`state/experiments/greg-again/CURRENT.md` now points local story search to `STORY_ENGINE_GUIDE.md` while keeping the heavy long-range files cold by default.

- [x] **Step 4: Correct progression bias**

The shared routing and updated debrief guardrails explicitly say clean wins may land without immediate compensating deficiency.

- [x] **Step 5: Commit**

Implemented in `story: route R2 through compact engine guide` and `story: add R2 engine counterweights`.

### Task 3: Add debrief counterweights

**Files:**
- Modify: `state/experiments/greg-again/written/DEBRIEF_GUARDRAILS.md`

**Interfaces:**
- Consumes: compact engine priors.
- Produces: book-level anti-drift checks that prevent clever nerfing and disposable social texture.

- [x] **Step 1: Add clean-win guardrail**

Future knowledge, sword work, and magic may sometimes work cleanly without compensating humiliation.

- [x] **Step 2: Add magic-width guardrail**

Low reserve remains one constraint rather than the entire magic system; the guardrail now tracks precision, timing, shape, duration, movement, concurrency, counters, integration, and other earned axes.

- [x] **Step 3: Add ceiling and party guardrails**

Higher-rank adventurers should remain impressive on their own terms, while returning field people and accumulated shorthand are preferred over endless disposable crews or forced roster assembly.

- [x] **Step 4: Commit**

Implemented in `story: add R2 engine counterweights`.

### Task 4: Verify durable routing

**Files:**
- Verify: all modified guidance files plus branch head.

- [x] **Step 1: Re-fetch the modified files**

Confirmed persisted story-engine guide, shared current routing, and debrief counterweights.

- [x] **Step 2: Re-fetch branch head**

Confirmed the guidance commits are on `experiment/plg-r2-opening` after the Chapter 23 frontier commit.

- [x] **Step 3: Requirement review**

Comparison from the pre-guidance Chapter 23 head shows only guidance/plan state files changed. No prose file changed and no Chapter 24 event was selected.
