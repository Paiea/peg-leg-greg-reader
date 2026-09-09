# R2 Seven Lamps + Fat Rehearsal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the approved Seven Lamps / world-iceberg architecture into durable R2 story memory, then run a third multi-year rehearsal that tests it against incompatible futures without selecting Chapter 24.

**Architecture:** Keep the full hidden magic/world model in a specialist architecture file derived from the approved spec. Keep local story search lean by adding only compact inheritance to `STORY_ENGINE_GUIDE.md`. Store the fat temporal simulation in a separate rehearsal file so future long-range reviews can use it without forcing every chapter writer to boot with it.

**Tech Stack:** Markdown story-state files in GitHub.

**Spec:** `docs/superpowers/specs/2026-09-08-r2-seven-lamps-world-design.md`

## Global Constraints

- Do not write Chapter 24 or any next-chapter prose.
- Preserve the newest selected written frontier and concurrent prose authority.
- Seven Lamps are backend magical architecture, not a public seven-school textbook.
- Human magic remains partial, cultural, practical, and sometimes theoretically wrong.
- Preserve magical beasts/ecology outside a universal adventurer-rank equivalence.
- Translate prior Hawaiian/moʻolelo-inspired quarry through causal/emotional structure, not literal Hawaiian surface markers.
- Greg may be a participant in someone else's myth rather than its protagonist.
- Preserve trade, money, ownership, salvage, appraisal, and market effects.
- Let Greg win cleanly sometimes; allow earned bad outcomes too.
- Permanent LEFT lower-leg loss with knee preserved remains the only hard future story attractor.
- Theatre remains strong but defeasible.
- Local story selection still begins with **WHAT SHOULD ACTUALLY HAPPEN NEXT?**

---

### Task 1: Build hidden magic/world architecture memory

**Files:**
- Create: `state/experiments/greg-again/written/SEVEN_LAMPS_WORLD_ICEBERG.md`

- [x] Preserve Seven Lamps backend principles from approved spec.
- [x] Separate underlying magical reality from human schools/traditions.
- [x] Preserve Greg's elite practical expertise while leaving deep theory incomplete.
- [x] Add magical ecology, beasts, shapeshifters, strange places, and non-Guild classification.
- [x] Add other-people's-myth quarry and explicit anti-cosplay translation rule.
- [x] Add trade/economy consequences and causality-in-both-directions rule.
- [x] Commit with `story: add R2 Seven Lamps world iceberg`.

### Task 2: Add compact local story-engine inheritance

**Files:**
- Modify: `state/experiments/greg-again/written/STORY_ENGINE_GUIDE.md`

- [x] Re-fetch newest file to avoid concurrent overwrite.
- [x] Add a compact `MAGIC IS AN ICEBERG` section pointing to the specialist file.
- [x] Add `OTHER PEOPLE'S MYTHS` and magical ecology pressures.
- [x] Add `CAUSALITY PAYS BOTH DIRECTIONS` to prevent both compulsive nerfing and positivity protection.
- [x] Keep explicit anti-queue language.
- [x] Preserve the exact pre-pass guide content and append the new world-iceberg priors after recovering from a write collision.

### Task 3: Run fat multi-year rehearsal 003

**Files:**
- Create: `state/experiments/greg-again/written/LONG_RANGE_REHEARSAL_003_WORLD_ICEBERG.md`
- Create companion reconciliation: `state/experiments/greg-again/written/LONG_RANGE_REHEARSAL_003_R1_RECONCILIATION.md`

- [x] Fresh-read current frontier and prior long-range maps.
- [x] Run at least six materially different 5–10 year futures; seven were retained.
- [x] Vary theatre/no theatre, leg-loss timing, warrior persistence, artifact centrality, party formation, magical ecology prominence, Seven-Lamps visibility, trade prominence, and other-people's-myth frequency.
- [x] Sample useful temporal distances around current/19, ~20, early twenties, mid-twenties, later twenties.
- [x] Reason backward from promising future states using pressures/relationships/competencies/mistakes/losses/acquisitions/absences/travel/ordinary life.
- [x] Extract HARD ATTRACTOR / STRONG GRAVITY / RECURRING POSSIBILITY / R1 QUARRY ONLY / CLEVER BUT UNGROUNDED / ACTIVELY AVOID.
- [x] Identify surprising convergences and distinguish recurrence from prompt-suggestion effects.
- [x] Reconcile the new architecture against mature R1 artifact-market, pricing, economy, progression, ecology, and setting brains without importing exact R1 state.
- [x] Do not select Chapter 24.

### Task 4: Verify and leave durable routing

**Files:**
- Verify the spec, iceberg file, engine guide, rehearsal 003, R1 reconciliation, branch head, and latest written frontier.

- [x] Confirm no prose file changed during this implementation.
- [x] Confirm current frontier was not overwritten.
- [x] Confirm engine guide points to specialist iceberg rather than turning the local boot into a Seven Lamps textbook.
- [x] Confirm rehearsal 003 does not queue future chapters.
- [x] Confirm temporary recovery files are absent from the final tree.
- [x] Record verification head before this final plan-status commit: `75441766175e7fff877fc5fdb79197792bb9b9ba`.

## Verification evidence

Comparison from pre-pass head `ef6da491efbc41146f48b33570a28a2c0650522c` through verification head `75441766175e7fff877fc5fdb79197792bb9b9ba` showed only six net files:

- this implementation plan
- the approved design spec
- `SEVEN_LAMPS_WORLD_ICEBERG.md`
- `LONG_RANGE_REHEARSAL_003_WORLD_ICEBERG.md`
- `LONG_RANGE_REHEARSAL_003_R1_RECONCILIATION.md`
- additive changes to `STORY_ENGINE_GUIDE.md`

No `state/experiments/greg-again/prose/*` file appeared in the compare.

Fresh `written/CURRENT.md` still records Chapter 23, **The Adventurer**, as the selected frontier and explicitly states that no Chapter 24 event is preselected.

Fresh `STORY_ENGINE_GUIDE.md` points deep magic to `SEVEN_LAMPS_WORLD_ICEBERG.md`, tells the local writer not to explain the hidden architecture, and includes explicit anti-queue language.

Fresh rehearsal 003 ends by returning to **WHAT SHOULD ACTUALLY HAPPEN NEXT?** and states that no future listed there is owed a chapter.

Both temporary recovery paths returned GitHub 404 after cleanup.

## Execution notes

A write-collision/recovery mistake temporarily replaced `STORY_ENGINE_GUIDE.md` during implementation. The exact pre-pass blob remained available in Git history and was fetched directly. The guide was then restored from that exact prior authority and extended with the new iceberg sections. Temporary recovery files created during that process were deleted.

The R1 comparison discovered that the mature repository already contains unusually compatible artifact-market, artifact-pricing, economy-continuity, progression, and magical-ecology doctrine. Rather than bloat the main rehearsal further, the surviving systems learning was stored in the companion `LONG_RANGE_REHEARSAL_003_R1_RECONCILIATION.md`.

Status: **IMPLEMENTED AND VERIFIED.**
