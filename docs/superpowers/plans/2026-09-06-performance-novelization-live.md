# PERFORMANCE Round Trip + Live Reader Experiment Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development when available, or superpowers:executing-plans to execute and verify this plan task by task.

**Goal:** Validate the approved hidden editorial round trip across the full displayed Chapters 1-20 Showcase sequence, preserve only earned PERFORMANCE gains in authoritative PLG prose, repair any Showcase seam exposed by hidden canon, and ship only after attribution, continuity, seam, reader, and repository validation pass.

**Architecture:** Canon prose remains the sole manuscript authority. The editorial transformation is `current authoritative prose -> dramatic structure -> PERFORMANCE -> explicit script -> PLG prose -> attribution / continuity / Showcase seam validation`. Dramatic structure, PERFORMANCE, and explicit script are derived and disposable intermediate layers. They may diagnose and propose changes, but they never become a second manuscript authority.

**Tech Stack:** Existing chapter HTML authority, Python editorial harnesses, unittest, GitHub Actions, generated reader validation, GitHub Pages.

**Spec:** Approved conversation contract plus the existing dialogue PERFORMANCE authority under `state/DIALOGUE_VARIANCE_ENGINE.md`, `state/DIALOGUE_VARIANCE_PERFORMANCE_LAYER.md`, and `state/voices/`.

## Global constraints

- Pinned source manuscript / reader authority: `35055180a116cf7a0dfd4a1fa94704c2c5b0bd40`.
- Preserved high-resolution PERFORMANCE lab: `experiment/performance-lab` at `48bf312924c5d1d6836587e9cb3e21f3944a4d43`.
- Integration branch: `experiment/performance-novelization-live`.
- Canon prose remains the only durable story authority. Derived dramatic, PERFORMANCE, and script representations remain editorial machinery.
- Greg remains the sole first-person narrator. Do not import another character's unobservable internal state into prose.
- Source wins every tie. There is no rewrite quota.
- Preserve canon facts, causality, money, magic, objects, body state, relationship state, knowledge ceilings, outcomes, and distinctive mundane/domain texture.
- Preserve speaker ownership and action ownership explicitly enough for a first read.
- Do not add em dashes to prose.
- Audit visible Showcase adjacency independently from canon-number adjacency.
- Future expansion beyond displayed Chapters 1-20 requires a fresh authority pin and a new bounded scope decision. This plan does not authorize manuscript-wide PERFORMANCE rewriting.

---

### Task 1: High-resolution round-trip fixtures

**Files:**
- Use: preserved `experiment/performance-lab` artifacts.
- Modify only when earned: `chapters/007.html`, `chapters/013.html`, `chapters/018.html`.
- Retain source when it wins: canon 002 and 016.

**Interfaces:**
- Consumes: exact pinned authoritative prose and existing voice/performance authority.
- Produces: explicit dramatic structure, comparative PERFORMANCE, explicit script evidence, and source-vs-candidate decisions for five representative scenes.

Five fixtures:
1. Canon 002 / displayed Chapter 2, Antonius loan.
2. Canon 007 / displayed Chapter 5, Antonius storeroom.
3. Canon 013 / displayed Chapter 9, Arlo workshop.
4. Canon 016 / displayed Chapter 12, Jorren + Alden + Greg.
5. Canon 018 / displayed Chapter 14, Hessa beans.

Decision rule: preserve only changes that remain better after returning from explicit script to Greg's first-person PLG prose.

Expected surviving decisions from the completed bounded run:
- 002: SOURCE RETAINED.
- 007: CHANGE.
- 013: CHANGE.
- 016: SOURCE RETAINED.
- 018: CHANGE.

---

### Task 2: Full displayed Chapters 1-20 PERFORMANCE round trip

**Files:**
- Create: `state/editorial/performance-lab/VISIBLE_001_020_ROUNDTRIP.md`.
- Create/update: `state/editorial/performance-lab/NOVELIZATION_LIVE_REPORT.md`.

**Interfaces:**
- Consumes: displayed-to-canon Showcase order, exact chapter prose, dramatic structure, comparative PERFORMANCE fingerprints, and explicit-script diagnostic stage.
- Produces: a chapter-by-chapter source-retain/change decision with no requirement that every chapter change.

Displayed-to-canon scope:
`001, 002, 004, 005, 007, 009, 010, 011, 013, 014, 015, 016, 017, 018, 019, 022, 023, 024, 025, 026`.

For each displayed chapter:
1. Reduce the authoritative prose to dramatic structure without changing story facts.
2. Apply comparative PERFORMANCE, including speaker goals, task ownership, social mode, state/pressure, and exchange rhythm.
3. Make dialogue/action ownership explicit in the script stage.
4. Return only earned gains to Greg's first-person PLG prose.
5. Prefer the source whenever the intermediate representation merely restates an already healthy scene.

---

### Task 3: Conservative attribution and replacement-seam hardening

**Files:**
- Retain bounded harness: `scripts/harden_performance_novelization_attribution.py`.
- Retain bounded harness: `scripts/clean_performance_novelization_seams.py`.
- Test: `tests/test_performance_novelization_experiment.py`.

**Interfaces:**
- Consumes: only the bounded surviving prose candidate.
- Produces: explicit first-read speaker/action ownership and clean entry/exit seams around replacements.

Rules:
- Ordinary `said` / `asked` tags are allowed and preferred over ambiguity.
- An action beat may carry attribution only when the actor is unquestionably the speaker in that paragraph.
- Do not attach another character's action to someone else's spoken line.
- Do not rewrite surrounding prose unless the replacement creates a real seam problem.
- Fail closed when an exact patch boundary is missing or ambiguous.

---

### Task 4: Showcase handoff audit

**Files:**
- Create: `state/editorial/performance-lab/SHOWCASE_SEAM_AUDIT_VISIBLE_001_020.md`.
- Modify only if required by a visible handoff: `chapters/004.html`.

**Interfaces:**
- Consumes: the 20-chapter displayed Showcase sequence after chapter curation hides canon chapters.
- Produces: classification of all 19 visible-to-visible handoffs as CLEAN, SOFT, or REPAIR, plus the smallest repair required.

Completed audit expectation:
- 14 CLEAN.
- 4 SOFT but self-contained enough to retain.
- 1 REPAIR: displayed Chapter 2 -> 3, canon 002 -> 004.

The canon 004 repair must re-establish the shale-test antecedent without restoring hidden canon 003 or changing its facts. Preserve that the sixth disk first barely beat the control, later testing reached closer to twenty percent, and the project remained promising rather than proven.

---

### Task 5: Retained bounded editorial harness and validation

**Files:**
- Retain: `scripts/apply_performance_novelization_experiment.py`.
- Retain: `scripts/run_performance_novelization_experiment.py`.
- Retain: `scripts/polish_performance_novelization_candidate.py`.
- Retain: `scripts/harden_performance_novelization_attribution.py`.
- Retain: `scripts/clean_performance_novelization_seams.py`.
- Retain: `tests/test_performance_novelization_experiment.py`.
- Retain: `.github/workflows/performance-novelization-live.yml`.
- Retain: `.github/workflows/performance-novelization-polish.yml`.

The harness was originally temporary, but the approved scope expanded from five scenes to a full displayed 1-20 round trip. It is therefore retained as bounded, inert-on-main editorial machinery so the experiment is reproducible and auditable. Its automatic push triggers remain scoped to `experiment/performance-novelization-live`; merging these files does not authorize or automatically run manuscript-wide PERFORMANCE work on `main`.

Validation requirements:
- focused PERFORMANCE experiment tests pass;
- full repository unit-test discovery passes;
- `git diff --check` passes;
- reader-frontier verification passes;
- no em dash appears in affected prose;
- required attribution and seam anchors remain present;
- generated prose diff stays bounded to the approved chapter surfaces;
- all 19 Showcase handoffs are recorded;
- no non-Greg internal state enters first-person narration;
- source-retained scenes remain unchanged merely for the sake of demonstrating the pipeline.

---

### Task 6: Publish and post-merge verification

1. Confirm the feature branch is based on the pinned current `main` with no behind commits.
2. Review the exact final diff and the three performance prose changes plus one Showcase seam repair.
3. Open a PR to `main` summarizing the derived pipeline, scope, surviving prose edits, seam audit, and non-authoritative status of hidden layers.
4. Merge only after required checks are green.
5. Follow the normal generated-reader and Pages deployment path from merged `main`.
6. Verify the live displayed chapters affected by canon 004, 007, 013, and 018.
7. Record final merge/main authority and deployment evidence.
8. Stop. Do not broaden the PERFORMANCE round trip beyond displayed Chapters 1-20 under this plan.
