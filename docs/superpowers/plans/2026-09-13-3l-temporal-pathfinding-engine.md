# 3L Temporal Pathfinding Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install the smallest durable 3L temporal-development surface needed to run four independent A/B/C/D pathfinding chats across a provisional 300-Record horizon, reconcile overlaps, and promote only surviving near-future story direction before Record 011 prose resumes.

**Architecture:** Keep accepted manuscript/story authority untouched. Put all temporal work under `3l/development/temporal-pathfinding/`. One compact seed gives every worker the same Record-010 state; four independent work orders define overlapping ranges and one output schema; seam files compare overlap state; connected rehearsal builds the strongest candidate life; Story Sync explicitly promotes only what survives. `map-300.md` remains experimental evidence, never canon.

**Tech Stack:** Markdown repository authority, Git/GitHub, normal ChatGPT worker tabs. No service, database, CI workflow, or publication dependency.

**Spec:** `docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md`

## Global Constraints

- Records 001-010 remain accepted manuscript authority.
- Canon prose outranks every temporal artifact.
- Life Two is the primary lived spine. Life One is pressure/evidence, not a second equal manuscript.
- Greg voice, Ithar voice, `Young Greg owns perception. Old Greg owns selection.`, lived-activity worldbuilding, and flexible Record length remain locked.
- The 300-map is search space, not prophecy.
- A/B/C/D first passes are independent and may not consume sibling first-pass output before all four exist.
- Windows: A 011-090, B 081-170, C 161-250, D 241-300.
- True forks are preserved, never averaged.
- First-pass workers may not modify manuscript, audio, public reader files, `3l/STORY_AUTHORITY.md`, or `3l/PROMISE_LEDGER.md`.
- Story Sync is the only promotion boundary.
- No em dashes in newly authored project guidance.
- Apply `3l/WORK_RECOVERY_AUTHORITY.md`; temporal machinery never blocks readable prose or audio production.

---

### Task 1: Workspace and prose lock

**Files:**
- Create: `3l/development/temporal-pathfinding/README.md`
- Create: `3l/development/temporal-pathfinding/PROSE_LOCK.md`
- Modify: `3l/README.md`

**Produces:** one discoverable engine entrypoint and one compact immutable prose/narrative contract.

- [ ] **Create `PROSE_LOCK.md`** with these rules:

```markdown
# 3L Temporal Pathfinding Prose Lock

Status: LOCKED BASELINE FOR TEMPORAL DEVELOPMENT

Records 001-010 establish the prose baseline. Temporal development does not reopen them.

- Greg compresses. Practical, embodied, dry, materially observant. Do not rebuild him.
- Ithar expands when interested. Age appears through time, causality, history, patience, observation, and context, not archaic fantasy diction.
- Young Greg owns perception. Old Greg owns selection.
- Future-engine knowledge may shape development planning but may not leak into young Greg's perception as deterministic foreshadowing.
- Worldbuilding emerges through lived activity: work, money, tools, contracts, institutions, property, travel, family, bodies, law, maintenance, food, ranker labor, and ordinary dependence.
- Life Two is the lived spine. Life One is remembered pressure/evidence unless a First-Life scene itself earns dramatization.
- Ithar interrupts only when the examination earns it. Do not mechanically end Records in the cave.
- Record length is elastic. Optimize for life per word and meaningful change in Greg's lived position.
- Canon manuscript prose outranks every temporal map, work order, seam, rehearsal, and Story Sync note.
```

- [ ] **Create temporal `README.md`** with status `EXPERIMENTAL STORY-DEVELOPMENT EVIDENCE`, a file-purpose table, and this run order:

```text
PROSE_LOCK -> seed -> map-300 -> A/B/C/D independent passes -> seams -> rehearsal -> Story Sync -> resume Record 011 prose
```

State explicitly that temporal output never edits manuscript, audio, or public reader files.

- [ ] **Update `3l/README.md`** under Active development authority:

```markdown
- Temporal pathfinding design: `../docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md`
- Experimental temporal workspace: `development/temporal-pathfinding/README.md`
```

- [ ] **Verify scope**:

```bash
git diff --check
git diff --name-only main...HEAD
```

No Task-1 change may touch `3l/manuscript/`, `3l/audio/`, `3l/records/`, or generated reader HTML.

- [ ] **Commit**:

```bash
git add 3l/README.md 3l/development/temporal-pathfinding/README.md 3l/development/temporal-pathfinding/PROSE_LOCK.md
git commit -m "3L: install temporal pathfinding workspace"
```

---

### Task 2: Shared Record-010 seed

**Files:**
- Create: `3l/development/temporal-pathfinding/seed.md`

**Consumes:** `3l/STORY_AUTHORITY.md`, `3l/PROMISE_LEDGER.md`, Records 006-010, `PROSE_LOCK.md`.

**Produces:** one compact common state packet shared unchanged by A/B/C/D.

- [ ] **Frontier/time**:

```markdown
# 3L Temporal Seed

Status: COMMON INPUT FOR FIRST-PASS A/B/C/D PATHFINDING
Accepted manuscript frontier: Record 010, THE STRANGER

Life Two has burned roughly eight years since Greg skipped the First-Life route. Record 009 places the major stay/leave decision in East Four's seventh year. Record 010 follows with Bren at age 31 and the North Vey divergence already propagated.
```

Do not invent an exact Greg age if authority does not lock it; use approximately late twenties.

- [ ] **Material state** must include: years at East Four; locally established Ranker/station Ranker; far below remembered S-class; lasting shoulder damage already seeded; future but unscheduled ruined leg/bad ribs/gate-damaged fingers; East Four over forgotten Line infrastructure; Halden alive and affecting wider review; North Vey rupture absent in Life Two.

- [ ] **Relationship state** must include: Nessa survived the First-Life death event and is uniquely Life-Two; Greg and Nessa share a home by 009 and are moving toward love/family without skipping time; Bren was chosen brother in Life One but currently knows Greg only through Life Two work; Greg refused to manufacture the friendship; Dera/Halden continue independent trajectories.

- [ ] **Open obligations** group the Promise Ledger into four compact blocks:
  - body/public identity: ruined leg, Peg-Leg Greg naming, ribs, fingers, low-B present capability, king's commendation, five named contracts, three free-drink cities
  - Life One provenance: Nhal at 48-49, Ithar name/route, old Line notation, lower channels/ninth station/eastern sink, real S-class scale, Bren friendship/death
  - Life Two emotional spine: ordinary life/love/family, catastrophic loss, completed revenge, life after revenge, later climbing for accumulated reasons
  - present/ending: pre-crisis Ithar search, private Ithar motive, unlocked reset/rebeginning mechanism/cost/beneficiary/final choice

- [ ] **Protected uncertainties**: exact marriage/children shape; catastrophic loss; human culpability; revenge structure; leg loss; other injury timing; Nhal nature/encounter mechanics; reset mechanism; final action.

- [ ] **Anti-railroad**:

```markdown
- Map titles are not promises.
- Nessa is not required to die because a provisional map says so.
- Bren friendship cannot be recreated by manipulation.
- Early people/objects need not exist for late payoff.
- Preserve quiet years, ordinary life, and independent character motion.
```

- [ ] **Verify** every concrete seed fact against `STORY_AUTHORITY.md`, `PROMISE_LEDGER.md`, or Records 006-010. Remove unsupported precision.

- [ ] **Commit**:

```bash
git add 3l/development/temporal-pathfinding/seed.md
git commit -m "3L: seed temporal pathfinding from Record 010"
```

---

### Task 3: Import the 300-Record search map

**Files:**
- Create: `3l/development/temporal-pathfinding/map-300.md`

**Consumes:** the approved conversation artifact `3L_300_Record_Temporal_Map.md`.

- [ ] Copy it intact. Preserve all 300 title/sentence entries, soft seams, and forward/backward obligation passes. Do not improve individual entries during import.

- [ ] Ensure the header says Records 001-010 are canon references and 011-300 are disposable hypotheses.

- [ ] Validate exact coverage:

```bash
python - <<'PY'
from pathlib import Path
import re
text = Path('3l/development/temporal-pathfinding/map-300.md').read_text(encoding='utf-8')
nums = [int(x) for x in re.findall(r'^### (\d{3})\s+[—-]', text, flags=re.M)]
assert nums == list(range(1, 301)), (len(nums), nums[:5], nums[-5:])
print('map-300: 300 unique ordered Records')
PY
```

- [ ] **Commit**:

```bash
git add 3l/development/temporal-pathfinding/map-300.md
git commit -m "3L: import provisional 300-record temporal map"
```

---

### Task 4: A/B/C/D work orders

**Files:**
- Create: `3l/development/temporal-pathfinding/windows/a.md`
- Create: `3l/development/temporal-pathfinding/windows/b.md`
- Create: `3l/development/temporal-pathfinding/windows/c.md`
- Create: `3l/development/temporal-pathfinding/windows/d.md`

**Produces:** four executable, independent first-pass work orders.

- [ ] Put this common contract in all four:

```markdown
Read current authority on branch `3l/temporal-pathfinding-engine`:
1. `PROSE_LOCK.md`
2. `seed.md`
3. `map-300.md`
4. this window work order
5. `3l/STORY_AUTHORITY.md`
6. `3l/PROMISE_LEDGER.md`

Do not write manuscript prose.
Do not edit canon, audio, reader files, Story Authority, or Promise Ledger.
Do not read completed sibling first-pass outputs before your own first pass is durable.
Treat map entries as proposals to attack, not instructions to preserve.
Preserve genuine forks.
```

- [ ] Require this common output schema:

```markdown
# WINDOW X FIRST PASS
## STATE IN
- age/time
- body/rank/skill
- work/money/property
- relationships
- geography/social range
- Line/world position
- First-Life pressure
- unresolved obligations

## RECORD PATH
### NNN - TITLE
One sentence describing the primary lived change, pressure, choice, or consequence.
Age/time: optional when useful.

## STATE OUT
[same categories]

## OBLIGATIONS PUSHED FORWARD
## OBLIGATIONS PUSHED BACKWARD
## PROTECTED UNCERTAINTIES / FORKS
## MAP CHANGES
- KEEP
- MOVE
- MERGE
- SPLIT
- REPLACE
- KILL
```

One sentence per Record is a hard first-pass constraint; no speculative chapter prose.

- [ ] **A**: 011-090, HIGH speculative confidence, forward consequence from 010. Ask how Nessa, East Four, family, Bren, Halden, work, money, property, and Line knowledge move independently; what ordinary roles widen Greg's obligations without restarting S-class optimization; what early conditions make later love/family/institutional stakes worthwhile even if tragedy changes.

- [ ] **B**: 081-170, MODERATE confidence, accumulation/middle negotiation. Ask what becomes durable enough to constrain later Greg; how marriage/family/business/training/property/institutions widen setting contact; how Nessa and recurring characters own independent lives; what continuity machinery, incentives, standards, insurance, maintenance, law, and politics can later produce harm without cartoon villainy.

- [ ] **C**: 161-250, LOW confidence, loss/revenge/consequence/rebuilding. Ask what loss grows causally from established life; what revenge Greg actually completes; what revenge costs/reveals/fails to restore; where body obligations may fit without checklist plotting; how revenge exposes deeper Line failure. Explicitly preserve non-Nessa-loss alternatives.

- [ ] **D**: 241-300, RECONNAISSANCE/BACKWARD OBLIGATION. Ask what fifty-nine-year-old Greg must know/own/regret/have lost/still owe; why Ithar is a credible last source; what the Line collapse requires earlier decades to demonstrate; what private reason caused pre-crisis Ithar research; what emotional conditions make reset/rebeginning meaningful. D must distinguish backward **requirements** from backward **events**.

- [ ] Verify:

```bash
python - <<'PY'
from pathlib import Path
expected = {'a.md':('011','090'),'b.md':('081','170'),'c.md':('161','250'),'d.md':('241','300')}
root = Path('3l/development/temporal-pathfinding/windows')
for name, bounds in expected.items():
    text = (root/name).read_text(encoding='utf-8')
    assert all(x in text for x in bounds), name
    assert 'Do not write manuscript prose' in text, name
    assert 'Do not read completed sibling' in text, name
    assert 'STATE IN' in text and 'STATE OUT' in text, name
print('window work orders: valid')
PY
```

- [ ] **Commit**:

```bash
git add 3l/development/temporal-pathfinding/windows
git commit -m "3L: add A B C D temporal work orders"
```

---

### Task 5: Seam, rehearsal, Story Sync, receipt

**Files:**
- Create: `3l/development/temporal-pathfinding/seams/a-b.md`
- Create: `3l/development/temporal-pathfinding/seams/b-c.md`
- Create: `3l/development/temporal-pathfinding/seams/c-d.md`
- Create: `3l/development/temporal-pathfinding/rehearsal.md`
- Create: `3l/development/temporal-pathfinding/story-sync.md`
- Create: `3l/development/temporal-pathfinding/receipt.md`

- [ ] Seam overlaps are exact: A/B 081-090, B/C 161-170, C/D 241-250.

- [ ] Every seam compares: chronology; body/disability; rank/skill; work/money/property; relationships; independent character motion; geography; reputation; objects/resources; Line/world condition; First-Life pressure; emotional state.

- [ ] Every seam ends with one classification only:

```markdown
## CLASSIFICATION
CONVERGED | MINOR DIVERGENCE | MAJOR DIVERGENCE | FORK

## WHY
## SURVIVING PRESSURES
## REJECTED ASSUMPTIONS
## OPEN FORKS
```

- [ ] `rehearsal.md` instructs the coordinator to preserve original first passes and build the strongest connected 011-300 candidate while checking causal continuity, actual years burned, money/property/work, body progression, skill/rank, public identity, independent character lives, love/family, loss causality, completed revenge and aftermath, rebuilding, Line movement, Life-One provenance, Ithar private/public motive, repeated Record grammar, protagonist gravity, generic escalation, deterministic foreshadowing, ordinary life reduced to setup, and overly mechanical ending setup.

- [ ] Rehearsal marks each Record/short run `STRONG`, `SOFT`, `FORK`, or `REPLACE`.

- [ ] `story-sync.md` starts empty:

```markdown
# 3L Temporal Story Sync

Status: NO TEMPORAL DEVELOPMENT IS ACCEPTED UNTIL LISTED HERE

## Current manuscript frontier
Record 010

## Promoted near-future runway
None yet.

## Promoted pressures
None yet.

## Promoted relationship directions
None yet.

## Promoted institutions/world mechanisms
None yet.

## Promoted temporal obligations
None yet.

## Explicitly unpromoted forks
None yet.

## Rule
Manuscript prose may later overturn this development material. When it does, prose wins and affected temporal assumptions are recomputed.
```

- [ ] `receipt.md` tracks source branch, accepted frontier, A/B/C/D completion, three seams, rehearsal, Story Sync, promoted runway length, forks preserved, unexpected causal discoveries, killed map assumptions, prose drift, and readiness to resume 011.

- [ ] Verify empty promotion state:

```bash
python - <<'PY'
from pathlib import Path
p = Path('3l/development/temporal-pathfinding/story-sync.md').read_text(encoding='utf-8')
assert '## Promoted near-future runway\nNone yet.' in p
assert '## Current manuscript frontier\nRecord 010' in p
print('story-sync starts empty')
PY
```

- [ ] **Commit**:

```bash
git add 3l/development/temporal-pathfinding/seams 3l/development/temporal-pathfinding/rehearsal.md 3l/development/temporal-pathfinding/story-sync.md 3l/development/temporal-pathfinding/receipt.md
git commit -m "3L: add temporal reconciliation surfaces"
```

---

### Task 6: Four-tabs-to-run startup prompts

**Files:**
- Modify: `3l/development/temporal-pathfinding/README.md`

- [ ] Add four copy-paste worker prompts. Window A form:

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

You are TEMPORAL WINDOW A.

Read and obey:
- 3l/development/temporal-pathfinding/PROSE_LOCK.md
- 3l/development/temporal-pathfinding/seed.md
- 3l/development/temporal-pathfinding/map-300.md
- 3l/development/temporal-pathfinding/windows/a.md
- 3l/STORY_AUTHORITY.md
- 3l/PROMISE_LEDGER.md

Execute Window A exactly as a first-pass pathfinding worker. Do not write manuscript prose. Do not read completed B/C/D outputs before your first pass is durable. Treat the 300-map as disposable hypotheses. Preserve forks.

Write only the completed Window A first pass to:
3l/development/temporal-pathfinding/windows/a-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, or Story Sync.
```

Create B/C/D equivalents with exact work-order and first-pass output paths.

- [ ] Add reconciliation prompt:

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

Do not begin until all four files exist:
- windows/a-first-pass.md
- windows/b-first-pass.md
- windows/c-first-pass.md
- windows/d-first-pass.md

Preserve those files unchanged. Reconcile the three overlaps using the seam templates, then perform the connected rehearsal in rehearsal.md. Do not modify canon prose. Do not average genuine forks. Update story-sync.md only with pressures/directions/short runs that genuinely survive. Leave uncertain material explicitly unpromoted.
```

- [ ] Add recovery rule: retry a stalled window once; on the second same-class failure rerun only that missing window from its frozen work order. Never restart completed siblings. Temporal work never blocks prose readability or audio production.

- [ ] Verify four distinct routes:

```bash
python - <<'PY'
from pathlib import Path
text = Path('3l/development/temporal-pathfinding/README.md').read_text(encoding='utf-8')
for x in 'abcd':
    assert f'windows/{x}.md' in text
    assert f'windows/{x}-first-pass.md' in text
print('README contains four independent startup routes')
PY
```

- [ ] **Commit**:

```bash
git add 3l/development/temporal-pathfinding/README.md
git commit -m "3L: add temporal engine startup prompts"
```

---

### Task 7: Final verification and dispatch boundary

**Files:** all files above only.

- [ ] Verify workspace shape:

```bash
python - <<'PY'
from pathlib import Path
root = Path('3l/development/temporal-pathfinding')
required = [
    'README.md','PROSE_LOCK.md','seed.md','map-300.md',
    'windows/a.md','windows/b.md','windows/c.md','windows/d.md',
    'seams/a-b.md','seams/b-c.md','seams/c-d.md',
    'rehearsal.md','story-sync.md','receipt.md',
]
missing = [x for x in required if not (root/x).exists()]
assert not missing, missing
print('temporal workspace: complete')
PY
```

- [ ] Rerun map coverage, window coverage, empty Story Sync, and startup-route checks.

- [ ] Verify allowed changed paths only:

```bash
git diff --name-only main...HEAD
```

Allowed implementation scope:

```text
docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md
docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-review.md
docs/superpowers/plans/2026-09-13-3l-temporal-pathfinding-engine.md
3l/README.md
3l/development/temporal-pathfinding/**
```

No manuscript, audio, reader output, Story Authority, or Promise Ledger edits.

- [ ] Run `git diff --check`.

- [ ] Lost-chat test each worker prompt. A fresh chat given only the prompt must be able to discover repository/branch, sources, range, schema, output path, forbidden edits, independence rule, and map's non-canon status.

- [ ] Add a PR #355 comment stating the engine is `SOURCE READY` only after these checks pass and that the first actual engine run is four independent window passes followed by seams, rehearsal, and Story Sync.

- [ ] Stop. Do not write Record 011 as infrastructure work. Next action is dispatch A/B/C/D concurrently.
