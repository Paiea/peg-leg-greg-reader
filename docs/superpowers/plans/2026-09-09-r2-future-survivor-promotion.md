# R2 Future Survivor Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the smallest durable R2 routing contract that lets forward writers discover and use surviving speculative future material as rehearsal evidence without treating it as story authority or lowering final listening-prose quality.

**Architecture:** Doctrine lives on `main`; live speculative A/B/C/D state remains on experiment branches. A new focused R2 protocol defines confidence zones, survivor classifications, promotion, re-performance, and discovery. Existing written-production and worker-router docs only point workers into that protocol and preserve the current normal publication route.

**Tech Stack:** Markdown repository doctrine, Git/GitHub branch workflow, existing R2 verification (`python -m unittest tests.test_r2_site -v`).

**Spec:** `docs/superpowers/specs/2026-09-09-r2-future-survivor-promotion-design.md`

## Global Constraints

- `main` owns doctrine and accepted output; live future backlog remains experimental by default.
- Speculative future evidence is never story authority merely because it survived an experiment.
- **Fidelity follows confidence. Future work earns detail by surviving.**
- Promotion raises confidence and required fidelity; it does not automatically canonize facts or prose.
- Material approaching A should normally be re-performed fresh against newest accepted authority rather than mechanically expanded or polished.
- Old speculative prose is challenger/rehearsal evidence, not fossilized draft authority.
- Final listening prose must be judged against strong recent R2, not against the speculative source it inherited.
- Missing, stale, conflicting, or inaccessible survivor evidence must never block normal forward writing.
- Do not add databases, scripts, queue managers, automatic promotion, or a new root lane.
- Do not make reader, registry, audio, or image surfaces depend directly on experiment-branch paths.
- Current accepted Chapters 49–86 on `main` are not future backlog material; this protocol applies to unaccepted territory beyond the current accepted frontier.

---

### Task 1: Add the focused future-survivor protocol

**Files:**
- Create: `r2/FUTURE_SURVIVOR_PROTOCOL.md`
- Reference: `docs/superpowers/specs/2026-09-09-r2-future-survivor-promotion-design.md`

**Interfaces:**
- Consumes: current R2 authority model from `r2/PIPELINE.md`, normal written publication route from `r2/WRITTEN_PRODUCTION.md`, and the approved design spec.
- Produces: one authoritative doctrine document that later routing docs can point to. It defines `A / B / C / D`, `SOURCE WIN / REPERFORM / FORK / DISCOVERY ONLY / KILL`, the promotion ladder, re-performance rule, experiment-branch ownership, and discovery behavior.

- [ ] **Step 1: Confirm the protocol does not already exist on newest authority**

Run:

```bash
git fetch origin main
git show origin/main:r2/FUTURE_SURVIVOR_PROTOCOL.md
```

Expected: command fails because the file does not yet exist. If it exists, stop and reconcile instead of creating a duplicate.

- [ ] **Step 2: Create `r2/FUTURE_SURVIVOR_PROTOCOL.md` with the approved doctrine**

Use this structure and wording as the minimum content:

```markdown
# R2 Future Survivor Protocol

Status: **ACTIVE FORWARD DEVELOPMENT DOCTRINE**

> **Fidelity follows confidence. Future work earns detail by surviving.**

## Authority boundary

Accepted Story State and selected written prose on current `main` remain authority.
Live speculative future material stays experimental by default.
Survival in an experiment does not make an event, chapter number, scene, or wording canonical.

Current accepted chapters are not backlog material. Only unaccepted future territory is governed as speculative survivor state.

## Confidence zones

### A — Commit Zone
Full Shared Greg Surface / listening-first prose. Freshly reconciled against newest authority. Publication candidate only after normal selection and verification.

### B — Hot Speculation
Full or near-full embodied prose with a strong continuity burden. High-confidence but still replaceable. When promoted toward A, normally re-perform against current authority rather than merely polish the old wording.

### C — Warm Speculation
Scene-complete or compressed chapter cores. Preserve causal motion, decisions, obligations, relationships, money, work, objects, geography, magic, and consequences. Spend prose only where embodiment improves judgment.

### D — Cold Speculation
Cheap far-future reconnaissance: pressures, possibilities, consequential scene sketches, character/world motion, backward obligations, and explicit uncertainty. Prefer robust shapes over brittle exact facts.

## Rolling promotion

WRITE / RE-PERFORM A
WRITE B HARD
EXECUTE C SPECULATIVELY
SCOUT D CHEAPLY
RECONCILE
PUBLISH THE CONTIGUOUS A-SIDE WIN
B -> A
SURVIVING C -> B
SURVIVING D -> C
RE-PERFORM PROMOTED MATERIAL AT ITS NEW FIDELITY
INVALIDATE CONTRADICTED FUTURES
SPAWN NEW D AT THE FAR EDGE
CONTINUE

Promotion raises confidence and required fidelity. It never automatically promotes speculative facts into story authority.

## Survivor classifications

- `SOURCE WIN` — existing speculative rendering still wins after current rehearsal.
- `REPERFORM` — causal/experiential core survives but the current scene or prose should be freshly rendered.
- `FORK` — materially different viable trajectories remain.
- `DISCOVERY ONLY` — exact event/prose dies but useful pressure, constraint, relationship motion, object consequence, or other discovery remains.
- `KILL` — no useful residue remains.

No sunk-cost protection.

## Re-performance contract

When future material approaches accepted authority, provide:

1. newest accepted Story State and exact recent prose
2. surviving future discovery / scene truth
3. old speculative prose only as challenger evidence
4. later discoveries that remain relevant

Then ask `WHAT SHOULD ACTUALLY HAPPEN NEXT?` and run the normal R2 path through Shared Greg Surface, Written Finish, connected rehearsal, selection, verification, and publication.

Do not simply make an old speculative chapter longer. Old wording survives only where it still wins.

## Discovery contract

Before substantial forward writing near a speculative frontier:

1. read newest accepted R2 authority
2. discover active temporal-survivor experiment branches using normal branch/WIP discovery
3. inspect only survivor/reconciliation material relevant to the immediate horizon
4. treat it as challenger/rehearsal evidence, not outline or story truth
5. write from current authority
6. preserve current SOURCE when speculative material loses

Missing, stale, conflicting, or inaccessible survivor evidence never blocks ordinary forward writing.

## Storage boundary

- doctrine may graduate to `main`
- live A/B/C/D backlog remains experimental by default
- accepted chapter prose reaches `main` only through normal R2 written production
- no reader, registry, audio, or image surface should depend directly on experimental future paths

## Prose-quality contract

A deep future backlog is not permission to lower publication quality.
As material approaches A, spend the saved creative effort on listening clarity, rhythmic variation, physical/social embodiment, dialogue ownership, emotional messiness, human irrationality, removal of redundant evaluative fragments, and deletion of principles the scene already proved.

Final chapters compete with strong recent R2, not with the quality of their speculative ancestors.
```

The implementation may tighten wording for clarity, but must not weaken any Global Constraint above.

- [ ] **Step 3: Verify the protocol contains all required invariants**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path('r2/FUTURE_SURVIVOR_PROTOCOL.md').read_text()
required = [
    'Fidelity follows confidence',
    'A — Commit Zone',
    'B — Hot Speculation',
    'C — Warm Speculation',
    'D — Cold Speculation',
    'SOURCE WIN',
    'REPERFORM',
    'FORK',
    'DISCOVERY ONLY',
    'KILL',
    'WHAT SHOULD ACTUALLY HAPPEN NEXT?',
    'Missing, stale, conflicting, or inaccessible survivor evidence never blocks',
    'no reader, registry, audio, or image surface should depend directly on experimental future paths',
]
missing = [s for s in required if s not in p]
assert not missing, missing
print('future survivor protocol invariants: OK')
PY
```

Expected: `future survivor protocol invariants: OK`.

- [ ] **Step 4: Commit the focused protocol**

```bash
git add r2/FUTURE_SURVIVOR_PROTOCOL.md
git commit -m "docs: add R2 future survivor protocol"
```

---

### Task 2: Route written production through survivor evidence without changing publication authority

**Files:**
- Modify: `r2/WRITTEN_PRODUCTION.md`
- Reference: `r2/FUTURE_SURVIVOR_PROTOCOL.md`

**Interfaces:**
- Consumes: survivor doctrine from Task 1.
- Produces: a small ingress rule in the existing written-production policy. It tells a forward writer when to inspect survivor evidence while preserving `CURRENT STORY AUTHORITY -> WHAT SHOULD ACTUALLY HAPPEN NEXT?` and the existing selected/verified publication transaction.

- [ ] **Step 1: Add a compact `Future survivor evidence` section after the default forward route / local story-freedom doctrine**

Add wording equivalent to:

```markdown
## Future survivor evidence

When unaccepted temporal-survivor material exists near the current written frontier, consult `r2/FUTURE_SURVIVOR_PROTOCOL.md` before inventing the next run cold.

Future survivor material is rehearsal/challenger evidence, not story authority and not a publication queue. Read newest accepted authority first, inspect only the relevant survivor/reconciliation evidence, then still ask:

> **WHAT SHOULD ACTUALLY HAPPEN NEXT?**

When a speculative unit approaches publication territory, prefer fresh re-performance against current Story State and recent exact prose. Preserve old wording only where it still wins. A missing, stale, conflicting, or inaccessible survivor experiment never blocks normal forward production.
```

Do **not** change the current publication transaction, exact-prose rule, chapter identity rule, or `SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT` behavior.

- [ ] **Step 2: Verify written production preserves both old and new invariants**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path('r2/WRITTEN_PRODUCTION.md').read_text()
required = [
    'SELECTED + VERIFIED WRITTEN CHAPTERS PUBLISH TO THE R2 SITE BY DEFAULT.',
    'WHAT SHOULD ACTUALLY HAPPEN NEXT?',
    'r2/FUTURE_SURVIVOR_PROTOCOL.md',
    'rehearsal/challenger evidence',
    'not story authority',
    'never blocks normal forward production',
]
missing = [s for s in required if s not in p]
assert not missing, missing
print('written production routing invariants: OK')
PY
```

Expected: `written production routing invariants: OK`.

- [ ] **Step 3: Commit the written-production routing change**

```bash
git add r2/WRITTEN_PRODUCTION.md
git commit -m "docs: route R2 writing through future survivors"
```

---

### Task 3: Teach fresh workers how to discover survivor evidence, then verify no runtime surface changed

**Files:**
- Modify: `AGENTS.md`
- Verify: `r2/FUTURE_SURVIVOR_PROTOCOL.md`
- Verify: `r2/WRITTEN_PRODUCTION.md`
- Test: `tests/test_r2_site.py` via existing suite; do not modify unless a real unrelated failure is discovered and separately authorized.

**Interfaces:**
- Consumes: the protocol and written-production ingress from Tasks 1–2.
- Produces: one worker-router pointer that makes the doctrine discoverable in fresh chats without making survivor state mandatory boot context or a new lane.

- [ ] **Step 1: Add a short R2 narrative-worker routing note to `AGENTS.md`**

Place it with the R2 / narrative routing material, using wording equivalent to:

```markdown
For forward R2 narrative work, `r2/FUTURE_SURVIVOR_PROTOCOL.md` defines how to discover and use surviving temporal experiment material when it exists. Treat survivor branches as optional challenger/rehearsal evidence, never accepted story authority or a mandatory outline. Read current `main` first. If relevant survivor evidence is missing, stale, conflicting, or inaccessible, continue normal R2 production from accepted authority.
```

Do not create a new root lane, mandatory every-task boot file, or automatic branch dependency.

- [ ] **Step 2: Verify fresh-worker discoverability and authority language**

Run:

```bash
python - <<'PY'
from pathlib import Path
agents = Path('AGENTS.md').read_text()
protocol = Path('r2/FUTURE_SURVIVOR_PROTOCOL.md').read_text()
written = Path('r2/WRITTEN_PRODUCTION.md').read_text()
assert 'r2/FUTURE_SURVIVOR_PROTOCOL.md' in agents
assert 'challenger/rehearsal evidence' in agents
assert 'current `main` first' in agents
assert 'mandatory outline' in agents
assert 'Fidelity follows confidence' in protocol
assert 'r2/FUTURE_SURVIVOR_PROTOCOL.md' in written
print('fresh worker routing: OK')
PY
```

Expected: `fresh worker routing: OK`.

- [ ] **Step 3: Run the existing R2 site verification suite**

Run:

```bash
python -m unittest tests.test_r2_site -v
```

Expected: all existing R2 site tests pass. Because this implementation is doctrine-only, any failure should be investigated as branch drift or an unrelated current-main issue before changing production code.

- [ ] **Step 4: Inspect the final diff for accidental scope growth**

Run:

```bash
git diff origin/main...HEAD -- AGENTS.md r2/WRITTEN_PRODUCTION.md r2/FUTURE_SURVIVOR_PROTOCOL.md
```

Confirm the diff contains only:

- one new focused survivor protocol
- one written-production ingress rule
- one worker-router discovery note

Reject any addition of scripts, backlog databases, automatic promotion, public reader dependencies, or speculative chapter copies.

- [ ] **Step 5: Commit the worker-router note**

```bash
git add AGENTS.md
git commit -m "docs: route R2 workers to future survivor evidence"
```

- [ ] **Step 6: Rebase/reconcile against newest `main` before integration**

Run:

```bash
git fetch origin main
git log --oneline --decorate -5 origin/main
```

If `main` moved, re-read changed R2 authority and reconcile these three documentation files in favor of newer authority. Do not restore stale whole-file copies.

- [ ] **Step 7: Re-run final verification after reconciliation**

Run:

```bash
python -m unittest tests.test_r2_site -v
python - <<'PY'
from pathlib import Path
assert 'r2/FUTURE_SURVIVOR_PROTOCOL.md' in Path('AGENTS.md').read_text()
assert 'r2/FUTURE_SURVIVOR_PROTOCOL.md' in Path('r2/WRITTEN_PRODUCTION.md').read_text()
assert 'Fidelity follows confidence' in Path('r2/FUTURE_SURVIVOR_PROTOCOL.md').read_text()
print('R2 future survivor doctrine: VERIFIED')
PY
```

Expected: suite passes and `R2 future survivor doctrine: VERIFIED` prints.

## Integration result

After these tasks, a fresh R2 writer should be able to reconstruct this rule from accepted repository doctrine without a giant chat prompt:

```text
CURRENT MAIN IS AUTHORITY
SURVIVING FUTURE MATERIAL MAY EXIST OFF-MAIN
DISCOVER ONLY WHAT IS RELEVANT
USE IT AS CHALLENGER / REHEARSAL EVIDENCE
FIDELITY FOLLOWS CONFIDENCE
RE-PERFORM AS MATERIAL APPROACHES A
PUBLISH ONLY THROUGH NORMAL SELECT + VERIFY ROUTE
```

No live speculative queue is copied to `main`, and normal forward writing remains valid when no temporal experiment exists.
