# 3L Dialogue Territory Rebuild 002–010 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Records 002–010 so Ithar appears in every record but occupies fewer, longer, cleanly spliceable voice territories while preserving story content and Greg's remembered-life voice.

**Architecture:** Canon prose remains authority. Records 002–003 receive the heaviest dialogue-shape pass; 004–005 keep their remembered prose but gain one deliberate Ithar checkpoint each; 006–010 consolidate existing cave interruption clusters. After prose is locked, regenerate routing/chunk plans and rebuild only published 002–003 audio before updating the website.

**Tech Stack:** Markdown canon manuscripts, Python 3L speaker/chunk planners, GitHub Actions, ffmpeg/ffprobe, static HTML site.

**Spec:** `docs/superpowers/specs/2026-09-13-3l-dialogue-territory-rebuild-design.md`

## Global Constraints

- Greg owns the account. Ithar owns the examination.
- Every Record 002–010 contains at least one deliberate Ithar presence.
- Prefer sustained Ithar blocks; routine short questions become Greg narration or nonverbal Dragon behavior.
- No mid-sentence Greg↔Ithar splice caused by Dragon speech tags.
- Remembered-life characters remain Greg voice.
- Greg=`deep`; Ithar=`normal`; tempo=1.0; pitch=0; no formant/DSP changes.
- Preserve plot, continuity, revelations, humor, and Greg's interior voice.

---

### Task 1: Rebuild Record 002

**Files:**
- Modify: `3l/manuscript/record-002.md`
- Regenerate later: `3l/audio/record-002-quote-inventory.tsv`
- Regenerate later: `3l/audio/record-002-short-dual-plan.json`

**Interfaces:**
- Consumes: current Record 002 canon and the dialogue territory spec.
- Produces: revised canon with fewer Dragon entrances and preserved factual content.

- [ ] Mark all current Greg↔Ithar voice transitions and identify short Dragon islands.
- [ ] Consolidate procedural question chains into Greg narration plus sustained Ithar examination blocks.
- [ ] Remove Dragon `he said` / `he asked` mid-sentence tags.
- [ ] Preserve the claim, forty-year memory, S-class/top-seven explanation, redback test, Nhal path, missing causal path, and final hypothesis block.
- [ ] Verify every surviving Ithar entry is either a substantial block or an intentionally sharp short line.
- [ ] Commit Record 002 canon revision.

### Task 2: Rebuild Record 003

**Files:**
- Modify: `3l/manuscript/record-003.md`

**Interfaces:**
- Consumes: revised 002 cadence rules.
- Produces: negotiation chapter with larger Dragon territories and the same ending at Greg remembering age nineteen.

- [ ] Collapse opening yes/no negotiation ping-pong.
- [ ] Keep one sustained Ithar block for why Greg came before the Line crisis.
- [ ] Keep sustained Ithar blocks for nouns-as-containers, Life Two path/Life One pressure, compression rules, and human-time pressure.
- [ ] Convert disposable Ithar confirmations/questions to nonverbal cues or Greg narration.
- [ ] Preserve the exact structural handoff into Record 004.
- [ ] Commit Record 003 canon revision.

### Task 3: Add Ithar checkpoints to Records 004–005

**Files:**
- Modify: `3l/manuscript/record-004.md`
- Modify: `3l/manuscript/record-005.md`

**Interfaces:**
- Consumes: remembered-life prose that is already working.
- Produces: one clean Dragon re-entry in each chapter without fragmenting the remembered stretch.

- [ ] Add one sustained Ithar checkpoint near the end of 004 focused on Greg's assumption that he still wanted the same life.
- [ ] Add one sustained Ithar checkpoint near the end of 005 focused on the ridge rejection, East Four, paper lanterns, and Greg calling the detour temporary.
- [ ] Keep all existing remembered-life scenes otherwise substantially verbatim.
- [ ] Commit 004–005 checkpoint additions.

### Task 4: Consolidate Records 006–010

**Files:**
- Modify: `3l/manuscript/record-006.md`
- Modify: `3l/manuscript/record-007.md`
- Modify: `3l/manuscript/record-008.md`
- Modify: `3l/manuscript/record-009.md`
- Modify: `3l/manuscript/record-010.md`

**Interfaces:**
- Consumes: existing cave interruption clusters.
- Produces: one or a few clean Ithar checkpoints per chapter instead of repeated short alternation.

- [ ] 006: consolidate four-weeks/eleven-years examination and stew interruption.
- [ ] 007: consolidate Halden/future-confidence examination.
- [ ] 008: consolidate Nessa/rescue and motive-vs-method examinations.
- [ ] 009: consolidate reasons-for-staying/table/payment examination.
- [ ] 010: consolidate Bren/choice and `my life` examinations.
- [ ] Verify every chapter still contains at least one deliberate Ithar presence.
- [ ] Commit 006–010 canon revisions.

### Task 5: Lock speaker routing and regression checks

**Files:**
- Modify: `3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md`
- Regenerate: `3l/audio/record-002-quote-inventory.tsv`
- Regenerate: `3l/audio/record-003-quote-inventory.tsv`
- Regenerate: `3l/audio/record-002-short-dual-plan.json`
- Regenerate: `3l/audio/record-003-short-dual-plan.json`
- Modify/Create tests under existing 3L test patterns.

**Interfaces:**
- Consumes: revised canon.
- Produces: explicit semantic speaker ownership and preview-safe short-take plans.

- [ ] Add production authority rule that every Dragon entrance must earn a seam and every record has at least one Ithar checkpoint.
- [ ] Regenerate quote inventories from revised canon.
- [ ] Explicitly lock speaker roles; do not infer by alternation.
- [ ] Regenerate preview-safe short-dual plans at ≤500 characters per source capture.
- [ ] Add/check regression assertions for no Dragon attribution seam inside a sentence and no missing Ithar presence in 002–010.
- [ ] Run 3L planner/site tests and commit routing changes.

### Task 6: Regenerate and republish Record 002 audio

**Files:**
- Replace: `3l/assets/audio/record-002.mp3`
- Update: Record 002 capture manifests/verification receipt/audit files following current short-take factory.

**Interfaces:**
- Consumes: revised 002 canon and locked short-dual plan.
- Produces: newly assembled, verified Record 002 MP3.

- [ ] Capture only revised preview-safe source takes required by the new plan.
- [ ] Verify every source transcript and ffprobe decode.
- [ ] Assemble with semantic speaker territories and ~2-second settling tail.
- [ ] Verify final duration, decode, SHA-256, and audit receipt.
- [ ] Commit new Record 002 asset.

### Task 7: Regenerate and republish Record 003 audio

**Files:**
- Replace: `3l/assets/audio/record-003.mp3`
- Update: Record 003 capture manifests/verification receipt/audit files following current short-take factory.

**Interfaces:**
- Consumes: revised 003 canon and locked short-dual plan.
- Produces: newly assembled, verified Record 003 MP3.

- [ ] Capture only revised preview-safe source takes required by the new plan.
- [ ] Verify every source transcript and ffprobe decode.
- [ ] Assemble with semantic speaker territories and ~2-second settling tail.
- [ ] Verify final duration, decode, SHA-256, and audit receipt.
- [ ] Commit new Record 003 asset.

### Task 8: Publish and verify website

**Files:**
- Verify/update: `3l/records/002.html`
- Verify/update: `3l/records/003.html`
- Verify/update: `3l/audio/index.html`
- Test: existing 3L site tests.

**Interfaces:**
- Consumes: verified replacement 002/003 MP3s.
- Produces: live website serving revised audio while retaining prose reading pages and Listening Archive.

- [ ] Verify record pages and Listening Archive reference the replacement assets.
- [ ] Run the targeted 3L site suite.
- [ ] Merge only after revised canon/audio checks are green.
- [ ] Verify GitHub Pages deploy completes successfully.
