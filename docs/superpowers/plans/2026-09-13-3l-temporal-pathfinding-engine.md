# 3L Temporal Pathfinding Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install the smallest durable 3L temporal-development surface needed to run four independent A/B/C/D pathfinding chats across a provisional 300-Record horizon, reconcile their overlaps, and promote only surviving near-future story direction before Record 011 prose resumes.

**Architecture:** Keep accepted manuscript/story authority untouched and place all new temporal work under `3l/development/temporal-pathfinding/`. One compact seed gives all workers the same Record-010 state; four independent markdown work orders define overlapping temporal ranges and a common output schema; seam files compare overlap state; connected rehearsal builds the strongest 011-300 candidate life; Story Sync explicitly promotes only what survives. The existing 300-Record map is imported as experimental evidence, never as canon.

**Tech Stack:** Markdown repository authority, Git/GitHub, normal ChatGPT worker tabs. No new runtime service, database, CI workflow, or publication dependency.

**Spec:** `docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md`

## Global Constraints

- Records 001-010 remain accepted manuscript authority and are not rewritten by this implementation.
- Canon prose remains higher authority than temporal development material.
- Life Two remains the primary on-page spine; Life One is pressure/evidence, not a second equal manuscript.
- Greg voice, Ithar voice, `Young Greg owns perception. Old Greg owns selection.`, lived-activity worldbuilding, and flexible Record length remain locked.
- The provisional 300-Record map is search space, not prophecy.
- A/B/C/D first passes are independent and must not consume one another's completed output before all four exist.
- A/B/C/D overlap intentionally: A 011-090, B 081-170, C 161-250, D 241-300.
- Seam conflicts are explained and classified; true forks are never averaged.
- Temporal workers may not modify `3l/manuscript/`, audio, public reader files, `3l/STORY_AUTHORITY.md`, or `3l/PROMISE_LEDGER.md` during first-pass pathfinding.
- Story Sync is the only promotion boundary from temporal evidence into accepted development direction.
- No em dashes in newly authored project prose/guidance.
- Apply `3l/WORK_RECOVERY_AUTHORITY.md`: do not let engine/tooling work block readable canon prose or audio catch-up.

---

### Task 1: Install the temporal workspace and prose lock

**Files:**
- Create: `3l/development/temporal-pathfinding/README.md`
- Create: `3l/development/temporal-pathfinding/PROSE_LOCK.md`
- Modify: `3l/README.md`

**Interfaces:**
- Consumes: `3l/STORY_AUTHORITY.md`, `3l/VOICE_PERFORMANCE_AUTHORITY.md`, `3l/WORK_RECOVERY_AUTHORITY.md`, Records 001-010, approved engine spec.
- Produces: one discoverable entrypoint for the temporal engine and one compact immutable prose/narrative contract every worker must read.

- [ ] **Step 1: Create `PROSE_LOCK.md`**

Write a compact authority containing exactly these durable rules:

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

- [ ] **Step 2: Create the temporal `README.md`**

It must state:

```markdown
# 3L Temporal Pathfinding

Status: EXPERIMENTAL STORY-DEVELOPMENT EVIDENCE

Accepted canon stops at the manuscript frontier on `main`. This folder cannot directly advance canon.

Run order:
1. read `PROSE_LOCK.md`
2. read `seed.md`
3. read `map-300.md` as disposable search space
4. run A/B/C/D independently from `windows/*.md`
5. preserve first-pass window outputs
6. reconcile `seams/*.md`
7. run `rehearsal.md`
8. promote only explicit survivors through `story-sync.md`
9. resume normal prose from Record 011 only after a near-future runway survives
```

Include a file-purpose table for every file created by this plan and an explicit warning that temporal output never edits manuscript/audio/public reader files.

- [ ] **Step 3: Add the development entrypoint to `3l/README.md`**

Under Active development authority, add:

```markdown
- Temporal pathfinding design: `../docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md`
- Experimental temporal workspace: `development/temporal-pathfinding/README.md`
```

Do not change the existing canon/audio/readability hierarchy.

- [ ] **Step 4: Verify the authority boundary**

Run:

```bash
git diff --check
git diff --name-only main...HEAD
```

Expected: no files under `3l/manuscript/`, `3l/audio/`, `3l/records/`, or public generated HTML are modified by Task 1.

- [ ] **Step 5: Commit**

```bash
git add 3l/README.md 3l/development/temporal-pathfinding/README.md 3l/development/temporal-pathfinding/PROSE_LOCK.md
git commit -m "3L: install temporal pathfinding workspace"
```

---

### Task 2: Build the shared Record-010 seed

**Files:**
- Create: `3l/development/temporal-pathfinding/seed.md`

**Interfaces:**
- Consumes: `3l/STORY_AUTHORITY.md`, `3l/PROMISE_LEDGER.md`, `3l/manuscript/record-006.md` through `record-010.md`, `PROSE_LOCK.md`.
- Produces: one compact source-state packet shared unchanged by A/B/C/D.

- [ ] **Step 1: Populate exact accepted frontier and time position**

Start the seed with:

```markdown
# 3L Temporal Seed

Status: COMMON INPUT FOR FIRST-PASS A/B/C/D PATHFINDING
Accepted manuscript frontier: Record 010, THE STRANGER

Life Two has burned approximately eight years since Greg skipped the First-Life route. Record 009 places the major stay/leave decision in East Four's seventh year. Record 010 follows with Bren at age 31 and the North Vey divergence already propagated.
```

Where exact Greg age is not explicitly locked, describe the position as approximately late twenties rather than inventing a false exact birthday.

- [ ] **Step 2: Add current material state**

Capture only supported current facts:

```markdown
## Material position
- Greg has spent years at East Four and is locally established rather than transient.
- He is a Ranker/station Ranker but remains far below remembered S-class capability.
- His Life-Two shoulder has already suffered lasting damage in the East Four transfer disaster.
- Present-frame future body obligations include ruined leg, bad ribs, gate-damaged right fingers, and later low-B-class public career, but those future injuries/events are not yet fixed in Life-Two chronology.
- East Four sits above forgotten older Line infrastructure.
- Halden survived and has already changed wider Line review.
- North Vey did not rupture in Life Two.
```

Do not silently convert present-frame future body facts into near-term scheduled events.

- [ ] **Step 3: Add relationship and independent-character state**

Include:

```markdown
## Relationship state
- Nessa Vale survived a disaster that killed her in Life One and is Greg's central uniquely Life-Two relationship in development authority.
- Greg and Nessa share a home by Record 009 and are moving toward love/family, but marriage/children remain unwritten and must burn time.
- Bren Calder was Greg's chosen brother in Life One. In Life Two he currently knows Greg only as a capable East Four worker/Ranker.
- Greg has explicitly refused to manufacture the old friendship. Any later Bren bond must be chosen in Life Two.
- Foreman Dera and Halden have independent professional trajectories and must not freeze while Greg advances.
```

- [ ] **Step 4: Add open obligations and protected uncertainties from `PROMISE_LEDGER.md`**

Group rather than dump the entire ledger. Required categories:

```markdown
## Open long-range obligations
### Body/public identity
ruined leg; Peg-Leg Greg naming; bad ribs; gate-damaged fingers; low-B present capability; king's commendation; five named contracts; three cities where Greg can drink free

### Life One provenance
Nhal beneath salt flats north of Vey around 48-49; Ithar name/route; old Line notation; western lower-channel/ninth-station/eastern-sink failure; real S-class-scale experience; Bren friendship/death

### Life Two emotional spine
ordinary life/love/family; catastrophic loss; completed revenge; life after revenge; later climbing for accumulated reasons

### Present/ending
Greg searched for Ithar before public Line crisis; private reason for Ithar; reset/rebeginning artifact/mechanism remains unlocked; final beneficiary/cost/choice remain open
```

- [ ] **Step 5: Add active anti-railroad constraints**

Include:

```markdown
## Protected uncertainties
- exact marriage/children shape
- exact catastrophic loss
- exact human culpability behind loss
- exact revenge method/target structure
- exact leg-loss event
- exact timing/provenance of other injuries
- exact Nhal nature and encounter mechanics
- exact reset/rebeginning mechanism and ending action

## Anti-railroad
- Do not make current 300-map titles promises.
- Do not require Nessa to die merely because one provisional map does.
- Do not recreate Bren friendship by manipulation.
- Do not make every early object/person exist for a late payoff.
- Preserve years of ordinary life and independent character motion.
```

- [ ] **Step 6: Verify seed claims against authority**

Run a manual three-source review against:

```text
3l/STORY_AUTHORITY.md
3l/PROMISE_LEDGER.md
3l/manuscript/record-010.md
```

Every concrete fact in `seed.md` must be directly supported by one of those or Records 006-009. Remove unsupported precision rather than filling gaps.

- [ ] **Step 7: Commit**

```bash
git add 3l/development/temporal-pathfinding/seed.md
git commit -m "3L: seed temporal pathfinding from Record 010"
```

---

### Task 3: Import the 300-Record search map as experimental evidence

**Files:**
- Create: `3l/development/temporal-pathfinding/map-300.md`

**Interfaces:**
- Consumes: the current conversation artifact `3L_300_Record_Temporal_Map.md` exactly as the starting search surface.
- Produces: one durable provisional map A/B/C/D may freely challenge.

- [ ] **Step 1: Copy the complete existing 300-map into `map-300.md`**

Preserve all 300 title/sentence entries, the forward/backward obligation pass, and its existing warning that 011-300 are hypotheses.

Do not rewrite the map while importing it. First-pass evidence must have a stable source.

- [ ] **Step 2: Add only a repository provenance header if needed**

If the source does not already contain equivalent status language, prepend:

```markdown
> Repository status: EXPERIMENTAL EVIDENCE. Imported as the first 300-Record search surface after approval on 2026-09-13. Records 001-010 are canon references; 011-300 are disposable hypotheses.
```

Do not alter individual future entries during import.

- [ ] **Step 3: Validate record coverage and uniqueness**

Run:

```bash
python - <<'PY'
from pathlib import Path
import re
p = Path('3l/development/temporal-pathfinding/map-300.md')
text = p.read_text(encoding='utf-8')
nums = [int(x) for x in re.findall(r'^### (\d{3})\s+[—-]', text, flags=re.M)]
assert len(nums) == 300, len(nums)
assert nums == list(range(1, 301)), (nums[:10], nums[-10:])
print('map-300: 300 unique ordered Records')
PY
```

Expected: `map-300: 300 unique ordered Records`.

- [ ] **Step 4: Commit**

```bash
git add 3l/development/temporal-pathfinding/map-300.md
git commit -m "3L: import provisional 300-record temporal map"
```

---

### Task 4: Create four independent temporal worker work orders

**Files:**
- Create: `3l/development/temporal-pathfinding/windows/a.md`
- Create: `3l/development/temporal-pathfinding/windows/b.md`
- Create: `3l/development/temporal-pathfinding/windows/c.md`
- Create: `3l/development/temporal-pathfinding/windows/d.md`

**Interfaces:**
- Consumes: `PROSE_LOCK.md`, `seed.md`, `map-300.md`, `3l/STORY_AUTHORITY.md`, `3l/PROMISE_LEDGER.md`.
- Produces: four executable first-pass work orders that can be pasted into independent normal ChatGPT tabs.
- Each worker writes only its own window output file on the temporal branch and does not read completed sibling outputs before its first pass is durable.

- [ ] **Step 1: Give every work order the same common contract**

Each file must include:

```markdown
## Common contract

You are one independent temporal pathfinding worker for 3L / The Third Leg.

Read current GitHub authority from branch `3l/temporal-pathfinding-engine`:
1. `3l/development/temporal-pathfinding/PROSE_LOCK.md`
2. `3l/development/temporal-pathfinding/seed.md`
3. `3l/development/temporal-pathfinding/map-300.md`
4. `3l/STORY_AUTHORITY.md`
5. `3l/PROMISE_LEDGER.md`

Do not write manuscript prose.
Do not edit canon, audio, reader files, Story Authority, or Promise Ledger.
Do not read completed sibling window outputs before your first pass is written.
Treat the existing map as proposals to attack, not instructions to preserve.
Preserve genuine forks instead of forcing convergence.
```

- [ ] **Step 2: Define the shared output schema**

Every work order must require:

```markdown
# WINDOW X FIRST PASS

## STATE IN
- age/time position
- body/rank/skill
- work/money/property
- relationships
- geography/social range
- Line/world position
- First-Life pressure
- unresolved obligations

## RECORD PATH
### 011 - TITLE
One sentence describing the primary lived change, pressure, choice, or consequence.
Age/time: optional when useful.

[continue through the assigned range]

## STATE OUT
[same state categories as STATE IN]

## OBLIGATIONS PUSHED FORWARD
- ...

## OBLIGATIONS PUSHED BACKWARD
- ...

## PROTECTED UNCERTAINTIES / FORKS
- ...

## MAP CHANGES
- KEEP: ...
- MOVE: ...
- MERGE: ...
- SPLIT: ...
- REPLACE: ...
- KILL: ...
```

One sentence under each Record is a constraint. Workers may not expand into full prose.

- [ ] **Step 3: Configure Window A**

`a.md` must specify:

```markdown
Range: Records 011-090
Confidence: HIGH SPECULATIVE CONFIDENCE
Primary direction: forward consequence from Record 010
Primary questions:
- What does Greg do now that he finally calls Life Two "my life"?
- How do Nessa, East Four, family, Bren, Halden, work, money, property, and Line knowledge move independently?
- Which ordinary roles plausibly turn Greg from station worker into a person with wider obligations without restarting an S-class optimization run?
- What early conditions create later love/family/institutional stakes while remaining worthwhile even if later tragedy changes?
```

Require A to be especially conservative about inventing distant catastrophe.

- [ ] **Step 4: Configure Window B**

`b.md` must specify:

```markdown
Range: Records 081-170
Confidence: MODERATE SPECULATIVE CONFIDENCE
Primary direction: accumulation and middle negotiation
Projected entry: Greg plausibly has broader work/reputation/property/relationship obligations, but exact route remains open.
Primary questions:
- What becomes durable enough to constrain Greg later?
- How do marriage/family/business/training/property/institutions widen setting contact if they survive?
- How can Nessa and other recurring characters own independent trajectories?
- What continuity machinery, incentives, records, law, standards, insurance, maintenance, or political structures could later produce serious harm without becoming cartoon villainy?
```

- [ ] **Step 5: Configure Window C**

`c.md` must specify:

```markdown
Range: Records 161-250
Confidence: LOW SPECULATIVE CONFIDENCE
Primary direction: loss, revenge, consequence, life after revenge, rebuilding
Projected entry: Greg plausibly has decades of accumulated people/institutions/reputation and therefore something specific to lose.
Primary questions:
- What catastrophic loss can grow from the world already established rather than arriving from nowhere?
- What revenge can Greg actually complete?
- What does completed revenge cost, reveal, fail to restore, and force him to live after?
- Where could leg loss and other present-body obligations fit without treating injuries like checklist payoffs?
- How can revenge reveal deeper Line/system failure rather than replace it?
```

C must preserve alternatives where the current provisional Nessa-loss path fails.

- [ ] **Step 6: Configure Window D**

`d.md` must specify:

```markdown
Range: Records 241-300
Confidence: RECONNAISSANCE / BACKWARD OBLIGATION
Primary direction: rebuilding, later climb, Line collapse, Ithar convergence, known ending pressure
Projected entry: older Greg is accomplished but diminished, with decades of ordinary social/institutional leverage and unresolved private interest in Ithar/reset possibility.
Primary questions:
- What must fifty-nine-year-old Greg plausibly know, own, regret, have lost, and still be responsible for when he reaches Ithar?
- Why is a dragon a credible last source rather than a late fantasy solution?
- What does the Line crisis require the earlier decades to have demonstrated?
- What private reason made Greg search for Ithar before the public crisis?
- What backward obligations make the reset/rebeginning choice emotionally earned without locking exact mechanics?
```

Require D to distinguish backward **requirements** from backward **events**.

- [ ] **Step 7: Verify ranges and independence language**

Run:

```bash
python - <<'PY'
from pathlib import Path
expected = {
    'a.md': ('011', '090'),
    'b.md': ('081', '170'),
    'c.md': ('161', '250'),
    'd.md': ('241', '300'),
}
root = Path('3l/development/temporal-pathfinding/windows')
for name, bounds in expected.items():
    text = (root / name).read_text(encoding='utf-8')
    assert bounds[0] in text and bounds[1] in text, name
    assert 'Do not read completed sibling window outputs' in text, name
    assert 'Do not write manuscript prose' in text, name
    assert 'STATE IN' in text and 'STATE OUT' in text, name
print('window work orders: valid')
PY
```

- [ ] **Step 8: Commit**

```bash
git add 3l/development/temporal-pathfinding/windows
git commit -m "3L: add A B C D temporal work orders"
```

---

### Task 5: Install seam, rehearsal, Story Sync, and run receipt surfaces

**Files:**
- Create: `3l/development/temporal-pathfinding/seams/a-b.md`
- Create: `3l/development/temporal-pathfinding/seams/b-c.md`
- Create: `3l/development/temporal-pathfinding/seams/c-d.md`
- Create: `3l/development/temporal-pathfinding/rehearsal.md`
- Create: `3l/development/temporal-pathfinding/story-sync.md`
- Create: `3l/development/temporal-pathfinding/receipt.md`

**Interfaces:**
- Consumes: completed immutable first-pass A/B/C/D outputs.
- Produces: explicit overlap classification, one connected candidate life, explicit promoted near-future direction, and a compact experiment receipt.

- [ ] **Step 1: Create identical seam templates with correct overlap ranges**

Each seam file begins with its overlap:

```text
a-b: Records 081-090
b-c: Records 161-170
c-d: Records 241-250
```

Then require this table:

```markdown
| Dimension | Left window | Right window | Result |
| --- | --- | --- | --- |
| chronology | | | |
| body/disability | | | |
| rank/skill | | | |
| work/money/property | | | |
| relationships | | | |
| independent character motion | | | |
| geography | | | |
| reputation | | | |
| objects/resources | | | |
| Line/world condition | | | |
| First-Life pressure | | | |
| emotional state | | | |
```

End with exactly one classification:

```markdown
## CLASSIFICATION
CONVERGED | MINOR DIVERGENCE | MAJOR DIVERGENCE | FORK

## WHY

## SURVIVING PRESSURES

## REJECTED ASSUMPTIONS

## OPEN FORKS
```

- [ ] **Step 2: Create `rehearsal.md` as the full-life reconciliation authority**

It must instruct the rehearsal chat to read all four original first passes and all seam files, preserve originals, then construct the strongest connected 011-300 path while explicitly checking:

```markdown
- causal continuity
- chronology and actual years burned
- money/property/work changes
- body and disability progression
- rank/skill progression
- reputation/public identity progression
- independent character lives
- love/family accumulation
- loss causality
- revenge completion and aftermath
- rebuilding
- Line knowledge/system movement
- Life-One provenance obligations
- Ithar private/public motive
- repeated Record grammar
- protagonist gravity
- generic escalation
- deterministic foreshadowing
- ordinary life being reduced to setup
- ending obligations being planted too mechanically
```

Require the rehearsal to output a candidate 011-300 list, but to mark each Record/short run as `STRONG`, `SOFT`, `FORK`, or `REPLACE` rather than pretending equal confidence.

- [ ] **Step 3: Create `story-sync.md` as a blank promotion ledger**

Use this structure:

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

Do not pre-promote material from the first 300-map before the engine run.

- [ ] **Step 4: Create `receipt.md`**

Use a compact checklist:

```markdown
# 3L Temporal Pathfinding Run Receipt

- source branch:
- accepted frontier at dispatch:
- A first pass:
- B first pass:
- C first pass:
- D first pass:
- seam A/B:
- seam B/C:
- seam C/D:
- connected rehearsal:
- Story Sync completed:
- near-future runway length promoted:
- meaningful forks preserved:
- strongest unexpected causal discoveries:
- map assumptions killed:
- prose drift observed: yes/no
- ready to resume Record 011 prose: yes/no
```

- [ ] **Step 5: Verify no speculative promotion exists before first run**

Run:

```bash
python - <<'PY'
from pathlib import Path
p = Path('3l/development/temporal-pathfinding/story-sync.md').read_text(encoding='utf-8')
assert 'Promoted near-future runway\nNone yet.' in p
assert 'Current manuscript frontier\nRecord 010' in p
print('story-sync starts empty')
PY
```

- [ ] **Step 6: Commit**

```bash
git add 3l/development/temporal-pathfinding/seams 3l/development/temporal-pathfinding/rehearsal.md 3l/development/temporal-pathfinding/story-sync.md 3l/development/temporal-pathfinding/receipt.md
git commit -m "3L: add temporal reconciliation surfaces"
```

---

### Task 6: Make the engine one-command-to-understand and four-tabs-to-run

**Files:**
- Modify: `3l/development/temporal-pathfinding/README.md`

**Interfaces:**
- Consumes: Tasks 1-5.
- Produces: four copy-paste startup prompts plus one seam/rehearsal coordinator prompt, with no need for lost-chat memory.

- [ ] **Step 1: Add four worker startup prompts**

Add one fenced prompt for each worker. Window A example:

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

Write only the completed Window A first pass back to:
3l/development/temporal-pathfinding/windows/a-first-pass.md

Do not modify canon, audio, reader files, Story Authority, Promise Ledger, seams, rehearsal, or Story Sync.
```

Create corresponding B/C/D prompts with their exact work-order/output paths.

- [ ] **Step 2: Add the reconciliation prompt**

```text
Continue 3L temporal pathfinding in Paiea/peg-leg-greg-reader on branch 3l/temporal-pathfinding-engine.

Do not begin until all four files exist:
- windows/a-first-pass.md
- windows/b-first-pass.md
- windows/c-first-pass.md
- windows/d-first-pass.md

Preserve those files unchanged. Reconcile the three overlaps using the seam templates, then perform the connected rehearsal in rehearsal.md. Do not modify canon prose. Do not average genuine forks. When the connected life is coherent enough, update story-sync.md only with pressures/directions/short runs that genuinely survive. Leave uncertain material explicitly unpromoted.
```

- [ ] **Step 3: Add a stall rule**

README must say:

```markdown
If any one window stalls, do not restart completed siblings. Retry that window once. On the second same-class failure, preserve the other first passes and rerun only the missing window from its frozen work order. Temporal pathfinding never blocks prose readability or audio production.
```

This mirrors `WORK_RECOVERY_AUTHORITY.md` rather than creating new recovery logic.

- [ ] **Step 4: Verify four prompts reference four distinct output files**

Run:

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

- [ ] **Step 5: Commit**

```bash
git add 3l/development/temporal-pathfinding/README.md
git commit -m "3L: add temporal engine startup prompts"
```

---

### Task 7: Final verification before dispatch

**Files:**
- Verify all files created/modified above.
- Do not create additional infrastructure unless verification proves a concrete gap.

**Interfaces:**
- Consumes: Tasks 1-6.
- Produces: SOURCE READY temporal engine suitable for four independent worker chats.

- [ ] **Step 1: Verify complete workspace shape**

Run:

```bash
python - <<'PY'
from pathlib import Path
root = Path('3l/development/temporal-pathfinding')
required = [
    'README.md', 'PROSE_LOCK.md', 'seed.md', 'map-300.md',
    'windows/a.md', 'windows/b.md', 'windows/c.md', 'windows/d.md',
    'seams/a-b.md', 'seams/b-c.md', 'seams/c-d.md',
    'rehearsal.md', 'story-sync.md', 'receipt.md',
]
missing = [p for p in required if not (root / p).exists()]
assert not missing, missing
print('temporal workspace: complete')
PY
```

- [ ] **Step 2: Verify map and work-order coverage**

Run the Task 3 300-Record validator and Task 4 window validator again.

- [ ] **Step 3: Verify canon/audio/public isolation**

Run:

```bash
git diff --name-only main...HEAD
```

Review every changed path. Implementation changes must be limited to:

```text
docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-design.md
docs/superpowers/specs/2026-09-13-3l-temporal-pathfinding-engine-review.md
docs/superpowers/plans/2026-09-13-3l-temporal-pathfinding-engine.md
3l/README.md
3l/development/temporal-pathfinding/**
```

No manuscript, audio, generated reader, or existing story/promise authority file may be modified.

- [ ] **Step 4: Verify formatting**

Run:

```bash
git diff --check
```

Expected: clean.

- [ ] **Step 5: Re-read the worker prompts as a lost-chat test**

Pretend a fresh chat knows only the pasted Window A prompt. Confirm it can discover:

1. repository and branch
2. exact source files
3. exact range
4. exact output schema
5. exact output path
6. forbidden edits
7. independence requirement
8. map's non-canon status

Repeat for B/C/D.

- [ ] **Step 6: Update PR #355 summary**

Add a PR comment recording:

```markdown
Temporal engine infrastructure is SOURCE READY when all verification steps pass. This PR does not itself advance manuscript canon. First engine run is four independent A/B/C/D first passes followed by seam analysis, connected rehearsal, and Story Sync.
```

- [ ] **Step 7: Stop at dispatch boundary**

Do not write Record 011 as part of infrastructure implementation.

The next action after verification is to dispatch the four temporal worker prompts concurrently. Once their outputs exist, run seam/rehearsal/Story Sync. Only then resume normal 3L manuscript prose from Record 011.
