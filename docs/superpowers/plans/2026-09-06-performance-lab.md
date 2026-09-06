# PERFORMANCE Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run the smallest five-scene PERFORMANCE laboratory that can falsify the proposed `DRAMATIC SCRIPT / IR -> PERFORMANCE -> NOVEL PROSE` boundary without novelizing or modifying canon.

**Architecture:** The lab lives entirely on `experiment/performance-lab`. It snapshots five exact current-main source excerpts together with immutable provenance, consumes performance authority by exact pinned editor-branch commit/blob references rather than copying it into new authority, generates explicit performed scripts, validates format/dramatic-truth claims plus Behavioral Realization evidence, applies the existing exchange-rhythm/swap diagnostics qualitatively, and records a source-vs-performed decision report. Canonical prose, forward Manuscript Engine behavior, and novelization are out of scope.

**Tech Stack:** Markdown lab artifacts, JSON authority lock, Python 3 standard library only, existing GitHub-backed manuscript/voice authority.

**Spec:** `docs/superpowers/specs/2026-09-06-performance-layer-contract-design.md`

## Global Constraints

- Current manuscript authority is pinned current `main` commit `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40` for this lab snapshot.
- Approved PERFORMANCE guidance is pinned to `editor/voice-compression-pass` commit `53bdca55a71f4d04be35580a238fd2fe985567a7`.
- Current-main prose remains manuscript authority; experiment copies are evidence only.
- Approved WIP performance guidance may inform the experiment but must not become manuscript authority.
- Temporary performance frames are ephemeral experiment artifacts.
- Performed scripts are experimental artifacts, not canon.
- No canonical prose changes.
- No novelization.
- No forward Manuscript Engine integration.
- No permanent performance database.
- No random or quota-driven conversational imperfection.
- Ownership is locked only when ownership itself matters.
- Non-POV internal state may guide simulation but may not become `[THOUGHT]` unless Dramatic Script explicitly authorizes that POV access.
- Hard project prose rule remains NO EM DASHES for any candidate script dialogue or thought content.

---

## File Structure

Create the following experiment-only surface:

```text
state/editorial/performance-lab/
  README.md
  authority.lock.json
  scenes/
    ch002-antonius-loan/
      fixture.md
      performed.md
      report.md
    ch007-antonius-storeroom/
      fixture.md
      performed.md
      report.md
    ch013-arlo-workshop/
      fixture.md
      performed.md
      report.md
    ch016-jorren-alden-greg/
      fixture.md
      performed.md
      report.md
    ch018-hessa-beans/
      fixture.md
      performed.md
      report.md
  SUMMARY.md
scripts/
  performance_lab_check.py
  test_performance_lab_check.py
```

Responsibilities:

- `README.md`: lab workflow, artifact contract, and explicit stop boundary.
- `authority.lock.json`: immutable provenance for the source snapshot and all reused PERFORMANCE authority files.
- each `fixture.md`: exact source excerpt plus compact Dramatic Script, relevant scene state/environment, and source provenance.
- each `performed.md`: temporary character performance frames followed by explicit performed script.
- each `report.md`: dramatic-truth gate, Behavioral Realization evidence, existing exchange-rhythm/swap audit, and source comparison classification.
- `SUMMARY.md`: five-scene aggregate result and promotion/kill decision only.
- `performance_lab_check.py`: structural/provenance checker; it must not judge literary quality or mutate files.
- `test_performance_lab_check.py`: standard-library regression tests for malformed ownership, missing provenance, missing realization evidence, and accidental novelization/canon paths.

---

### Task 1: Add the Lab Contract and Structural Checker

**Files:**
- Create: `state/editorial/performance-lab/README.md`
- Create: `scripts/performance_lab_check.py`
- Create: `scripts/test_performance_lab_check.py`

**Interfaces:**
- Consumes: the approved PERFORMANCE spec.
- Produces: `check_lab(root: Path) -> list[str]`, returning zero strings on structural success; and CLI `python scripts/performance_lab_check.py --root state/editorial/performance-lab` returning 0 on success, 1 on findings.

- [ ] **Step 1: Write failing tests for the minimum artifact contract**

Create `scripts/test_performance_lab_check.py` using `unittest` and temporary directories. Cover these exact cases:

```python
class PerformanceLabCheckTests(unittest.TestCase):
    def test_missing_authority_lock_fails(self): ...
    def test_dialogue_requires_explicit_addressee(self): ...
    def test_action_requires_named_owner(self): ...
    def test_non_pov_thought_fails_without_authorization(self): ...
    def test_material_bend_requires_evidence_beat_reference(self): ...
    def test_stop_boundary_rejects_novel_prose_artifact(self): ...
    def test_minimal_valid_scene_passes(self): ...
```

The valid performed-script syntax for the lab is:

```text
## PERFORMANCE FRAMES

### GREG
STATE: interested
PERFORMED STANCE: casual confidence
ATTENTION: Antonius's decision
BASELINE BEND: none material

## PERFORMED SCRIPT

[B001] GREG -> ANTONIUS [DIALOGUE]
"How much?"

[B002] ANTONIUS [ACTION]
Counts the silver.
```

When a frame claims a material bend, use one lab-only evidence line:

```text
BASELINE BEND: materially lower patience
REALIZED BY: B004, B007
```

This evidence pointer is diagnostic scaffolding, not part of the permanent PERFORMANCE contract.

- [ ] **Step 2: Run tests and verify red state**

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
```

Expected: import/function failures because `scripts/performance_lab_check.py` does not yet exist.

- [ ] **Step 3: Implement the minimal checker**

Implement only structural checks:

```python
def check_lab(root: Path) -> list[str]:
    # require README.md and authority.lock.json
    # require exactly the five expected scene directories
    # require fixture.md, performed.md, report.md in each scene
    # reject files named novel.md, novel-prose.md, canon.patch, or anything under chapters/
    # parse performed-script beat headers with one of:
    #   [B###] OWNER [ACTION]
    #   [B###] OWNER -> ADDRESSEE [DIALOGUE]
    #   [B###] GREG [THOUGHT]
    # reject pronoun owners HE/SHE/THEY/I in beat headers
    # reject dialogue headers without addressee
    # reject non-GREG [THOUGHT] unless fixture contains an exact matching `POV AUTHORIZED: NAME` line
    # for each `BASELINE BEND:` containing `material` require a following `REALIZED BY:` and require every referenced beat ID to exist
    # require fixture source provenance fields and report verdict headings
    # do not infer literary quality
```

CLI:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the test suite and verify green state**

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

The unit tests must pass. The lab CLI may still fail before Tasks 2-3 because scene artifacts are not yet present; that failure is expected and should name missing files rather than crash.

- [ ] **Step 5: Commit Task 1**

```bash
git add scripts/performance_lab_check.py scripts/test_performance_lab_check.py state/editorial/performance-lab/README.md
git commit -m "Add PERFORMANCE lab contract and checker"
```

---

### Task 2: Pin Authority and Build Five Current-Main Fixtures

**Files:**
- Create: `state/editorial/performance-lab/authority.lock.json`
- Create: the five `scenes/*/fixture.md` files.

**Interfaces:**
- Consumes: current-main chapter prose at commit `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`; PERFORMANCE authority at commit `53bdca55a71f4d04be35580a238fd2fe985567a7`.
- Produces: self-contained source/Dramatic Script fixtures with exact provenance and no prose mutation authority.

- [ ] **Step 1: Resolve and record exact authority blobs**

Create `authority.lock.json` with this shape:

```json
{
  "manuscript": {
    "ref": "35055180a116cf7a0dfd4a1fa94704c2c5b0bd40",
    "files": {
      "chapters/002.html": "<resolved blob sha>",
      "chapters/007.html": "<resolved blob sha>",
      "chapters/013.html": "<resolved blob sha>",
      "chapters/016.html": "<resolved blob sha>",
      "chapters/018.html": "<resolved blob sha>"
    }
  },
  "performance_authority": {
    "ref": "53bdca55a71f4d04be35580a238fd2fe985567a7",
    "files": {
      "state/DIALOGUE_VARIANCE_PERFORMANCE_LAYER.md": "<resolved blob sha>",
      "state/voices/EARLY_BOOK_I_PERFORMANCE_MATRIX.md": "<resolved blob sha>",
      "state/voices/GREG.md": "<resolved blob sha>",
      "state/voices/ANTONIUS.md": "<resolved blob sha>",
      "state/voices/ARLO.md": "<resolved blob sha>",
      "state/voices/JORREN.md": "<resolved blob sha>",
      "state/voices/ALDEN.md": "<resolved blob sha>",
      "state/voices/HESSA.md": "<resolved blob sha>",
      "state/editorial/dialogue-variance-pass/EXCHANGE_RHYTHM_GATE.md": "<resolved blob sha>",
      "state/editorial/dialogue-variance-pass/PERFORMANCE_CALIBRATION_VISIBLE_001_020.md": "<resolved blob sha>"
    }
  }
}
```

Fetch by exact commit, never by moving branch name while executing the lab.

- [ ] **Step 2: Extract exact source scenes from pinned current-main prose**

Use these five canonical source files corresponding to displayed Chapters 2, 5, 9, 12, and 14:

- `chapters/002.html`: Antonius loan negotiation beginning at `"Have we met?" Antonius asked.` and ending after Greg exits the loan scene, before the Sella encounter.
- `chapters/007.html`: Antonius storeroom scene, including cleanup, collateral/ownership discussion, trash sorting, Tere gauge discovery, and resulting price negotiation; stop before any later unrelated scene.
- `chapters/013.html`: Arlo workshop/process-control exchange centered on regulator/process work and Greg's interpretation of repeatability/process control.
- `chapters/016.html`: Jorren + Alden + Greg training exchange where Greg's advice about not spending the first advantage is taught, tested, overused, and physically corrected.
- `chapters/018.html`: Hessa bean exercise exchange where Greg is forced to solve the bounded problem rather than the whole spell and the scene uses procedure/stopping behavior.

Copy the exact selected prose excerpt into each fixture under `## SOURCE EXCERPT`. The excerpt is evidence only and must include:

```text
SOURCE REF: 35055180a116cf7a0dfd4a1fa94704c2c5b0bd40
SOURCE PATH: chapters/NNN.html
SOURCE BLOB: <sha>
```

- [ ] **Step 3: Write compact Dramatic Script blocks**

Each fixture must contain:

```text
## DRAMATIC SCRIPT

### LOCKED
- only ownership/results whose identity genuinely matters

### REQUIRED
- outcome/information requirements without unnecessarily locking delivery route

### MUST NOT DRIFT
- knowledge ceilings, money/magic/body/object/relationship/canon constraints

### STATE IN
- materially relevant state only

### STATE OUT
- only required persistent change

### ENVIRONMENT
- current task, objects, participants, social/physical pressure
```

Do not copy dialogue into `LOCKED` unless the exact speaker/delivery mechanism is dramatically required.

- [ ] **Step 4: Validate provenance and fixture structure**

Run:

```bash
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

Expected at this stage: only missing `performed.md` / `report.md` findings are allowed. There must be no authority-lock, source-provenance, or fixture-format findings.

- [ ] **Step 5: Commit Task 2**

```bash
git add state/editorial/performance-lab/authority.lock.json state/editorial/performance-lab/scenes/*/fixture.md
git commit -m "Add pinned PERFORMANCE lab fixtures"
```

---

### Task 3: Generate Five Performed Scripts and Run Local Gates

**Files:**
- Create: the five `scenes/*/performed.md` files.
- Create: the five `scenes/*/report.md` files.

**Interfaces:**
- Consumes: each scene's exact fixture plus only the pinned authority relevant to its active characters.
- Produces: explicit performed scripts and inspection evidence. No novel prose.

- [ ] **Step 1: Generate temporary performance frames**

For each materially active character, synthesize only:

```text
STATE:
PERFORMED STANCE:
ATTENTION:
BASELINE BEND:
SHIFT TRIGGER: [only if materially useful]
```

If `BASELINE BEND` claims a material effect, add `REALIZED BY:` after the performed script exists and point it to exact beat IDs. If no material bend is claimed, say `BASELINE BEND: none material` or describe a non-material tendency without a realization requirement.

Do not persist newly inferred character rules outside the scene artifact.

- [ ] **Step 2: Generate the explicit performed script**

Use only these beat forms:

```text
[B001] NAME [ACTION]
Content.

[B002] NAME -> NAME [DIALOGUE]
"Content."

[B003] GREG [THOUGHT]
Content.

PERFORMANCE SHIFT:
Short reason for a material envelope change.
```

Rules:

- every action has one explicit named actor;
- every dialogue line has one explicit named speaker and addressee;
- `[THOUGHT]` is Greg-only in this lab unless fixture explicitly authorizes otherwise;
- preserve all locked dramatic truth;
- allow clean exchanges when earned;
- allow imperfect routes only when causal;
- do not add scene-external consequences;
- do not novelize.

- [ ] **Step 3: Run the structural checker after each scene**

Run:

```bash
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

Fix structural findings before evaluating literary value.

- [ ] **Step 4: Record Behavioral Realization evidence in each report**

Each `report.md` must include:

```markdown
## Dramatic Truth Gate
PASS / FAIL
Evidence: locked/required items checked against performed beat IDs.

## Behavioral Realization Gate
PASS / FAIL
- Character: claimed material bend -> B###, B###
- Character: no material bend claimed

## Exchange Rhythm Gate
- initiator:
- extender:
- cleanest final button:
- exit modes:
- compact-counter collision present: YES/NO
- specialist-domain exit available/used:

## Swap / Confusability Check
- pair(s) tested:
- would swapping several turns preserve social texture: YES/NO/MIXED
- note intentional Greg/Alden overlap where relevant
```

A report may pass with no misunderstanding, interruption, failed joke, or silence if the route is character-plausible.

- [ ] **Step 5: Record source-vs-performed comparison**

Each report also includes:

```markdown
## Source Comparison
Character-specific handling: stronger / same / weaker
Exchange asymmetry: stronger / same / weaker
Human route quality: stronger / same / weaker
Mundane/domain texture preserved: yes / partial / no
Greg interiority preserved at script level: yes / partial / no

## Scene Verdict
CLEARLY STRONGER / PROMISING BUT MIXED / NO MATERIAL GAIN / WORSE / FLATTENED

## Why
2-8 concise bullets tied to specific source moments and performed beat IDs.
```

This is the primary falsification evidence. Do not score by numeric quotas.

- [ ] **Step 6: Run full lab checker and unit tests**

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

Expected: all unit tests pass and checker returns 0.

- [ ] **Step 7: Commit Task 3**

```bash
git add state/editorial/performance-lab/scenes/*/performed.md state/editorial/performance-lab/scenes/*/report.md
git commit -m "Run five-scene PERFORMANCE lab"
```

---

### Task 4: Aggregate the Falsification Result and Stop

**Files:**
- Create: `state/editorial/performance-lab/SUMMARY.md`

**Interfaces:**
- Consumes: five scene reports.
- Produces: one promotion/revise/kill decision. Produces no prose and no integration changes.

- [ ] **Step 1: Summarize the five verdicts**

`SUMMARY.md` must record:

```markdown
# PERFORMANCE Lab Summary

Source manuscript ref: 35055180a116cf7a0dfd4a1fa94704c2c5b0bd40
Performance authority ref: 53bdca55a71f4d04be35580a238fd2fe985567a7

| Scene | Dramatic truth | Behavioral realization | Scene verdict |
| --- | --- | --- | --- |
| Ch 2 Antonius loan | ... | ... | ... |
| Ch 5 Antonius storeroom | ... | ... | ... |
| Ch 9 Arlo workshop | ... | ... | ... |
| Ch 12 Jorren/Alden/Greg | ... | ... | ... |
| Ch 14 Hessa beans | ... | ... | ... |
```

- [ ] **Step 2: Apply the spec's promotion threshold**

Promotion to a *separate future novelization experiment* requires:

- zero dramatic-truth failures;
- at least three `CLEARLY STRONGER` scenes;
- no more than one `WORSE / FLATTENED` scene;
- no systematic loss of Greg interiority, mundane texture, or domain-specific behavior.

Record exactly one decision:

- `PROMOTE TO NOVELIZATION DESIGN`
- `REVISE PERFORMANCE CONTRACT`
- `STOP / NO MATERIAL VALUE`

Even `PROMOTE` does not authorize novelization in this execution.

- [ ] **Step 3: Verify hard stop boundaries**

Run:

```bash
git diff --name-only $(git merge-base HEAD 35055180a116cf7a0dfd4a1fa94704c2c5b0bd40)..HEAD
```

Inspect the list and confirm there are no changes under:

```text
chapters/
state/manuscript/
state/MANUSCRIPT_ENGINE_PLAYBOOK.md
state/MANUSCRIPT_WORKFLOW.md
```

Also confirm no artifact named `novel*.md`, `prose*.md`, or `canon.patch` exists under the lab directory.

- [ ] **Step 4: Run final verification**

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

Expected: zero failures and zero structural findings.

- [ ] **Step 5: Commit the summary**

```bash
git add state/editorial/performance-lab/SUMMARY.md
git commit -m "Record PERFORMANCE lab decision"
```

- [ ] **Step 6: STOP**

Do not:

- novelize any scene;
- patch canonical prose;
- open an integration PR to `main` for manuscript changes;
- wire PERFORMANCE into forward generation;
- promote temporary frames into stable voice authority.

The next action, only if the lab meets promotion criteria, is a separately approved novelization-comparison design.
