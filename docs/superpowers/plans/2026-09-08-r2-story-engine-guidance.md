# R2 Story Engine Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the Greg, Again / R2 local story engine compact durable guidance from the approved multi-year magic/rank/party rehearsals without preselecting future chapters.

**Architecture:** Keep heavy long-range material cold in the existing pressure/rehearsal files. Add one compact story-engine guide containing generative priors that local chapter search can actually inherit, then point `written/CURRENT.md` and the debrief guardrails at it. Preserve newest chapter-frontier authority and do not modify prose.

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

- [ ] **Step 1: Write the guide**

Include the following durable priors in compact form: let Greg win cleanly sometimes; magic growth is multidimensional; Barrier is force geometry rather than only wall size; allow non-Barrier magic when earned; show higher rank competence without humiliating it; keep ordinary Guild ladder separate from Rankers; authority grants Ranker titles; repeat field people before inventing disposable companions; let party structure accumulate through work; keep artifacts strategic rather than stat-linear; permit geography/time to expand; future-history people may precede their later titles; ordinary life continues under fantasy expansion.

- [ ] **Step 2: Add explicit anti-queue rule**

State that the guide does not mean `show Gold`, `unlock spell`, `find artifact`, `form party`, or `meet future legend` next. It only widens what may naturally win a bounded story search.

- [ ] **Step 3: Commit**

Commit message: `story: add compact R2 story-engine guide`

### Task 2: Route the written engine through the compact guide

**Files:**
- Modify: `state/experiments/greg-again/written/CURRENT.md`

**Interfaces:**
- Consumes: `STORY_ENGINE_GUIDE.md`.
- Produces: local writer routing that sees the counterweights without booting the full long-range files every chapter.

- [ ] **Step 1: Re-fetch newest CURRENT**

Confirm selected frontier and preserve all newer chapter state.

- [ ] **Step 2: Replace stale one-year language near the top**

Describe the Chapter 1 ledger as long-delay promise memory under the 5–10 year permission horizon.

- [ ] **Step 3: Add story-engine guide routing**

Point local chapter search to `STORY_ENGINE_GUIDE.md` as compact positive guidance. Keep long-range maps cold unless a real long-range uncertainty is present.

- [ ] **Step 4: Correct progression bias**

Keep `PROGRESSION OPENS THE NEXT CONSTRAINT`, but explicitly state that some wins may simply land and remain wins; the engine must not append a deficiency to every successful beat.

- [ ] **Step 5: Commit**

Commit message: `story: route R2 writer through engine priors`

### Task 3: Add debrief counterweights

**Files:**
- Modify: `state/experiments/greg-again/written/DEBRIEF_GUARDRAILS.md`

**Interfaces:**
- Consumes: compact engine priors.
- Produces: book-level anti-drift checks that prevent clever nerfing and disposable social texture.

- [ ] **Step 1: Add clean-win guardrail**

Future knowledge, sword work, and magic must sometimes work cleanly without a compensating humiliation.

- [ ] **Step 2: Add magic-width guardrail**

Low reserve is one constraint, not the whole magic system. Look for precision, timing, shape, duration, movement, concurrency, counters, integration, and other earned axes.

- [ ] **Step 3: Add ceiling and party guardrails**

Show competent higher-rank adventurers on their own terms. Prefer returning field people and accumulated shorthand over endless disposable crews or forced game-roster assembly.

- [ ] **Step 4: Commit**

Commit message: `story: add R2 engine counterweights`

### Task 4: Verify durable routing

**Files:**
- Verify: all three files above plus branch head.

- [ ] **Step 1: Re-fetch the modified files**

Confirm exact persisted text and pointers.

- [ ] **Step 2: Re-fetch branch head**

Confirm all commits are on `experiment/plg-r2-opening` and no newer story frontier was overwritten.

- [ ] **Step 3: Requirement review**

Verify that no Chapter 24 event was selected, no prose file was modified, and the engine can inherit the nudges without mandatory long-range boot.
