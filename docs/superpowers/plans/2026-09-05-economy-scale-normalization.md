# Economy Scale Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair economic scale drift across Peg-Leg Greg while preserving story beats, relationships, and scene structure wherever a number-only correction is sufficient.

**Architecture:** Use `state/editorial/ECONOMY_SCALE_NORMALIZATION.md` as the design authority. Build a chapter-range audit from exact prose, identify money-driving scenes, normalize amounts/arithmetic/reaction language in bounded batches, and keep a running ledger of anchors so later chapters cannot regress to copper-scale emotional logic after Greg has already become silver-active.

**Tech Stack:** GitHub repository text/HTML/Markdown authority, manuscript exact checkpoints, reader chapter HTML, editorial state files.

**Spec:** `state/editorial/ECONOMY_SCALE_NORMALIZATION.md`

## Global Constraints

- Preserve canon, causality, character voice, relationships, jokes, scene purpose, and chapter structure unless arithmetic makes that impossible.
- Change nominal amounts before changing prose structure.
- Do not invent an exact copper/silver/gold/platinum exchange rate without exact prose authority.
- Do not globally multiply all prices by one factor.
- Early Greg remains silver-active, cash-poor, volatile, overconfident, and bad at capital discipline.
- Later earning power must ratchet upward in both objective scale and emotional reaction.
- The Tere gauge remains a 40g+ right-buyer-value claim with 5s seller financing unless exact later authority explicitly revises it.
- Vale must resolve to one coherent historical ledger and one genuine closure, not multiple contradictory debts.
- Small jobs may remain for social/access/texture reasons, but small pay should not repeatedly read as major financial progression after Greg outgrows that tier.

---

### Task 1: Build the early Vale / silver ledger

**Files:**
- Read: `chapters/001.html` through at least `chapters/020.html`
- Create: `state/editorial/economy-normalization/EARLY_VALE_LEDGER.md`

**Interfaces:**
- Consumes: exact reader prose and the normalization spec.
- Produces: chronological Vale principal/advance/payment/labor-credit/gauge-financing ledger with citations by chapter and unresolved transitions explicitly marked.

- [ ] Read Chapters 1-20 exactly, extracting every Greg/Vale money movement and every explicit silver/gold anchor.
- [ ] Record original loan, interest terms, later advances, labor credits, repayments, and the 5s Tere gauge seller financing.
- [ ] Identify the first exact chapter where the original Vale obligations are fully settled, rolled forward, refinanced, or become ambiguous.
- [ ] Do not infer a conversion rate.
- [ ] Commit the ledger as an audit artifact before changing manuscript prose.

### Task 2: Build the whole-book earning / spending ladder

**Files:**
- Create: `state/editorial/economy-normalization/EARNING_SCALE_AUDIT.md`
- Read: representative exact chapters across all major eras, expanding only around money-driving scenes.

**Interfaces:**
- Consumes: early ledger plus exact manuscript money scenes.
- Produces: era-by-era anchors for earnings, purchases, debt, liquidity, assets, and Greg's emotional response.

- [ ] Sample each manuscript era for meaningful wages, gambling outcomes, investments, gear, travel, artifact bids, commissions, and contracts.
- [ ] Flag only scenes where money materially drives behavior or where emotional reaction contradicts established scale.
- [ ] Classify each era as survival scraps / silver-active volatility / recurring competent income / leverage income / capital deployment / mature wealth trajectory.
- [ ] Mark accidental scarcity resets separately from intentional downturns.
- [ ] Commit the audit before numeric patching begins.

### Task 3: Normalize early and middle money numbers in bounded batches

**Files:**
- Modify: only exact manuscript/reader surfaces containing approved flagged money scenes.
- Update: `state/editorial/economy-normalization/EARNING_SCALE_AUDIT.md`

**Interfaces:**
- Consumes: approved audit flags.
- Produces: coherent numeric scale with preserved scenes.

- [ ] Work in bounded chapter batches.
- [ ] For each flagged scene, attempt a number-only correction first.
- [ ] Recalculate surrounding arithmetic exactly.
- [ ] Adjust reaction language only if the corrected amount makes the old reaction false.
- [ ] Preserve Greg's early waste, leverage, gambling volatility, speculative spending, and old-life miscalibration.
- [ ] Verify no unrelated prose changed.
- [ ] Commit each bounded batch independently.

### Task 4: Reconcile Vale and recent closure chapters

**Files:**
- Read/modify as needed: Chapters 487, 490, 491 exact checkpoints and corresponding published surfaces.
- Update: `state/MANUSCRIPT_STATE.md`
- Update: `state/editorial/economy-normalization/EARLY_VALE_LEDGER.md`

**Interfaces:**
- Consumes: final historical Vale ledger.
- Produces: one coherent Vale balance history ending in the already-established social closure.

- [ ] Determine whether the recent nominal 23c account is a separate later liability or a drifted continuation of early silver obligations.
- [ ] Preserve Ch487's structural beat: verify obligations, make a meaningful payment, preserve reserve.
- [ ] Preserve Ch490's structural beat: improved earning power makes the remaining Vale balance casually closable after a better-paying day.
- [ ] Preserve Ch491's structural beat: Greg can invite Antonius drinking because no debt remains underneath the relationship.
- [ ] Change nominal balances, earnings, reserves, and related arithmetic as required.
- [ ] Change only the minimum reaction/debrief wording needed to fit corrected scale.
- [ ] Mark Vale CLOSED only after the reconciled ledger proves it.

### Task 5: Harden forward economic production

**Files:**
- Modify: `state/ECONOMY_CONTINUITY.md`
- Modify: `state/PROGRESSION_ENGINE.md`
- Modify: `state/MANUSCRIPT_STATE.md`

**Interfaces:**
- Consumes: normalized audit results.
- Produces: durable forward rules preventing economic regression.

- [ ] Record current era earning tier and representative anchors.
- [ ] Require new paid opportunities to be calibrated against Greg's current earning capacity, not only purse balance.
- [ ] Encode that later Greg may accept trivial-pay work for non-financial reasons without treating the pay as progression.
- [ ] Encode that silver-scale operating money is expected before gold-scale ownership/capital becomes common.
- [ ] Preserve large-value low-liquidity distinctions for artifacts and business assets.
- [ ] Verify future trailheads do not use tiny copper balances as automatic poverty shorthand.
- [ ] Commit state/engine updates after all corrected anchors are verified.

## Verification Gate

Before calling the normalization complete:

- [ ] Every changed money scene has exact before/after arithmetic recorded in the audit.
- [ ] Vale has one traceable ledger and one closure.
- [ ] No exact conversion rate was invented accidentally.
- [ ] Tere gauge price/value distinction remains coherent.
- [ ] Early Greg still wastes meaningful money.
- [ ] Later Greg's earning scale and emotional reaction show an upward ratchet.
- [ ] Small-pay social scenes remain possible without being mislabeled as financial milestones.
- [ ] Current manuscript state reflects normalized rather than provisional amounts.
