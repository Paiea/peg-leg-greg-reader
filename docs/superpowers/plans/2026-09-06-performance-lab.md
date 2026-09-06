# PERFORMANCE Lab Implementation Plan

> **For agentic workers:** Execute task by task. Use TDD for the structural checker. Stop before novelization or canon mutation.

**Goal:** Build and run the smallest five-scene PERFORMANCE laboratory that can falsify the proposed `DRAMATIC SCRIPT / IR -> PERFORMANCE -> NOVEL PROSE` boundary without novelizing or modifying canon.

**Architecture:** The lab lives entirely on `experiment/performance-lab`. It snapshots five exact current-main source excerpts together with immutable provenance, consumes approved PERFORMANCE authority by exact pinned commit/blob references rather than copying it into manuscript authority, generates explicit performed scripts, validates structure and Behavioral Realization evidence, applies the existing exchange-rhythm/swap diagnostics qualitatively, and records a source-vs-performed decision report.

**Spec:** `docs/superpowers/specs/2026-09-06-performance-layer-contract-design.md`

## Immutable authority pins

### Manuscript source

Commit: `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`

- `chapters/002.html`: `0db288df4459bae2da3edd8a169602799abba94d`
- `chapters/007.html`: `70f79b2b11940cbadeb970c1e8cf39c7294fdb66`
- `chapters/013.html`: `181a2b52326c3b190aa5ae6f9ee8967e4d206715`
- `chapters/016.html`: `819ce699336e89cb69efe19094b7bf52bfec4d3a`
- `chapters/018.html`: `30538e320c31db744212e4c22922b0f0fe860975`

Current-main prose is manuscript authority. Fixture copies are evidence only.

### Approved PERFORMANCE guidance

Commit: `53bdca55a71f4d04be35580a238fd2fe985567a7`

- `state/DIALOGUE_VARIANCE_ENGINE.md`: `03b22f5376538de2998f5f97610f99cb0f79cbb1`
- `state/DIALOGUE_VARIANCE_PERFORMANCE_LAYER.md`: `363d244718f64511d43a43ae0e26226f8a7f6029`
- `state/voices/EARLY_BOOK_I_PERFORMANCE_MATRIX.md`: `319f8887eb46d8dfc3bf1dbf223480cfa1d24286`
- `state/voices/GREG.md`: `81cf04a3bdb0514872590abe7d6136e4c951c19f`
- `state/voices/ANTONIUS.md`: `1a4b49660cd8c96e38704c2c0f2f08e4db6d9f07`
- `state/voices/ARLO.md`: `d2e7624590b74f3c92122df737d94e973e3371b9`
- `state/voices/JORREN.md`: `2b14c0506f5b459b08a409fa85a3116340097453`
- `state/voices/ALDEN.md`: `a0a5968584490db6708b1bd48bce1b319da31e99`
- `state/voices/HESSA.md`: `5b16bbcdedd076218cde25d9d37bc611047d6e26`
- `state/editorial/dialogue-variance-pass/EXCHANGE_RHYTHM_GATE.md`: `f00d439c1e5218318efcff5a8614ec7c758f22bc`
- `state/editorial/dialogue-variance-pass/PERFORMANCE_CALIBRATION_VISIBLE_001_020.md`: `3bf17896ebcf9cb3116b63967fdd7142aa2d712b`

These files inform the experiment only. They do not silently become manuscript authority.

## Hard boundaries

- Temporary performance frames are ephemeral experiment artifacts.
- Performed scripts are experimental artifacts, not canon.
- No changes under `chapters/`.
- No novel prose artifact.
- No forward Manuscript Engine integration.
- No permanent performance database.
- No random or quota-driven conversational imperfection.
- Ownership is locked only when ownership itself matters.
- Non-POV internal state may guide simulation but may not become `[THOUGHT]` unless Dramatic Script explicitly authorizes that POV access.
- Candidate dialogue/thought text must contain no em dashes.

## Experiment files

```text
state/editorial/performance-lab/
  README.md
  authority.lock.json
  scenes/
    ch002-antonius-loan/{fixture.md,performed.md,report.md}
    ch007-antonius-storeroom/{fixture.md,performed.md,report.md}
    ch013-arlo-workshop/{fixture.md,performed.md,report.md}
    ch016-jorren-alden-greg/{fixture.md,performed.md,report.md}
    ch018-hessa-beans/{fixture.md,performed.md,report.md}
  SUMMARY.md
scripts/
  performance_lab_check.py
  test_performance_lab_check.py
```

## Task 1: Structural checker, TDD first

### 1A. Write red tests

Create `scripts/test_performance_lab_check.py` with `unittest` coverage for:

- missing authority lock;
- dialogue without explicit addressee;
- action without explicit named owner;
- pronoun owner in a beat header;
- non-Greg `[THOUGHT]` without explicit fixture POV authorization;
- a material `BASELINE BEND` without `REALIZED BY` beat references;
- `REALIZED BY` references to missing beats;
- forbidden `novel*.md`, `prose*.md`, or `canon.patch` artifacts;
- a minimal valid scene.

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
```

Expected before implementation: red because the checker does not exist.

### 1B. Implement only structural checking

Create `scripts/performance_lab_check.py` with:

```python
def check_lab(root: Path) -> list[str]: ...
```

Accepted performed beat headers:

```text
[B001] NAME [ACTION]
[B002] NAME -> NAME [DIALOGUE]
[B003] GREG [THOUGHT]
```

Rules:

- named owners only;
- dialogue requires addressee;
- non-Greg thought requires exact `POV AUTHORIZED: NAME` in fixture;
- any `BASELINE BEND:` containing `material` requires `REALIZED BY:` with existing beat IDs;
- fixture must record SOURCE REF, SOURCE PATH, SOURCE BLOB;
- each report must contain Dramatic Truth Gate, Behavioral Realization Gate, Exchange Rhythm Gate, Swap / Confusability Check, Source Comparison, and Scene Verdict;
- checker never judges prose quality and never mutates files.

Re-run tests. Unit tests must be green.

## Task 2: Authority lock and five source fixtures

Create `authority.lock.json` using exactly the pins above.

Each `fixture.md` contains:

```text
SOURCE REF:
SOURCE PATH:
SOURCE BLOB:

## SOURCE EXCERPT
Exact current-main prose for the bounded exchange under test.

## DRAMATIC SCRIPT
### LOCKED
### REQUIRED
### MUST NOT DRIFT
### STATE IN
### STATE OUT
### ENVIRONMENT
```

Source excerpts are bounded to the exchange needed to test the PERFORMANCE behavior, not whole-chapter migrations.

Lab exchange targets:

1. `chapters/002.html`: Antonius loan negotiation from first direct meeting through the end of the loan exchange, stopping before Sella.
2. `chapters/007.html`: storeroom work plus the Tere-gauge attention/valuation shift, bounded to the smallest continuous excerpt that preserves that shift.
3. `chapters/013.html`: Arlo process-control/workshop exchange where the physical process, not generic epistemic banter, should govern his exits.
4. `chapters/016.html`: Jorren/Alden/Greg training exchange where advice is learned, overused, and physically corrected.
5. `chapters/018.html`: Hessa bean exercise where procedure, concern, bounded problem size, and stopping behavior interact.

Do not lock who delivers a required informational result unless delivery ownership itself matters.

## Task 3: Generate five performed scripts

Each `performed.md` begins with compact temporary frames for materially active characters only:

```text
## PERFORMANCE FRAMES

### NAME
STATE:
PERFORMED STANCE:
ATTENTION:
BASELINE BEND:
SHIFT TRIGGER:   # optional
REALIZED BY:     # required only for a claimed material bend
```

Then:

```text
## PERFORMED SCRIPT

[B001] NAME [ACTION]
Content.

[B002] NAME -> NAME [DIALOGUE]
"Content."

[B003] GREG [THOUGHT]
Content.
```

PERFORMANCE may change unlocked local topology, wording, timing, silence, interruption, partial answers, explanation depth, physical-vs-verbal response, joke engagement, delayed response, or a fingerprint strength overfiring/underfiring.

PERFORMANCE may not change locked truth, knowledge ceilings, money/magic/body/object continuity, relationship state, persistent consequences, specialist knowledge ownership, or explicitly locked ownership.

Run the checker after each scene and repair structural findings before evaluating value.

## Task 4: Scene reports

Each `report.md` records:

```markdown
## Dramatic Truth Gate
PASS / FAIL
Evidence tied to beat IDs.

## Behavioral Realization Gate
PASS / FAIL
Claimed material bends tied to exact beat IDs, or explicit note that no material bend was claimed.

## Exchange Rhythm Gate
- initiator
- extender
- cleanest final button
- exit modes
- compact-counter collision: YES/NO
- specialist-domain exit available/used

## Swap / Confusability Check
- pair(s) tested
- would swapping several turns preserve social texture: YES/NO/MIXED
- intentional Greg/Alden overlap noted where relevant

## Source Comparison
Character-specific handling: stronger / same / weaker
Exchange asymmetry: stronger / same / weaker
Human route quality: stronger / same / weaker
Mundane/domain texture preserved: yes / partial / no
Greg interiority preserved at script level: yes / partial / no

## Scene Verdict
CLEARLY STRONGER / PROMISING BUT MIXED / NO MATERIAL GAIN / WORSE / FLATTENED

## Why
Concise evidence tied to source moments and performed beat IDs.
```

No imperfection is required. The question is whether the route is more plausibly produced by these people in this state/environment than the default optimized route.

## Task 5: Aggregate falsification result

Create `SUMMARY.md` with all five verdicts and one decision:

- `PROMOTE TO NOVELIZATION DESIGN`
- `REVISE PERFORMANCE CONTRACT`
- `STOP / NO MATERIAL VALUE`

Promotion threshold:

- zero dramatic-truth failures;
- at least three scenes `CLEARLY STRONGER`;
- no more than one `WORSE / FLATTENED`;
- no systematic loss of Greg interiority, mundane texture, or domain-specific behavior.

This threshold is a lab decision aid, not a manuscript quota.

## Final verification

Run:

```bash
python -m unittest scripts.test_performance_lab_check -v
python scripts/performance_lab_check.py --root state/editorial/performance-lab
```

Then inspect changed paths and confirm there are no changes under:

```text
chapters/
state/manuscript/
state/MANUSCRIPT_ENGINE_PLAYBOOK.md
state/MANUSCRIPT_WORKFLOW.md
```

Also confirm the lab contains no `novel*.md`, `prose*.md`, or `canon.patch` artifact.

## STOP

Even if the decision is `PROMOTE TO NOVELIZATION DESIGN`, stop here. Do not novelize, patch canonical prose, wire PERFORMANCE into forward generation, or promote temporary frames into stable voice authority.
