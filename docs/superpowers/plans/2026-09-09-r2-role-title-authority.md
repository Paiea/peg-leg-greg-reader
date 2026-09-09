# R2 Role Title Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make selected R2 chapter headings the canonical embodied-Greg role titles and keep every title-bearing surface synchronized by stable chapter number.

**Architecture:** Editorial judgment is stored once in a durable R2 role-title audit. The selected written heading becomes semantic title authority. A small Python reconciler propagates that title to public chapter manifests, the R2 production registry, and Greg, Again audio metadata without touching stable IDs, routes, media, or prose body text.

**Tech Stack:** Python 3, JSON, Markdown, existing unittest-based repository tests, static GitHub Pages manifests.

**Spec:** `docs/superpowers/specs/2026-09-09-r2-role-title-authority-design.md`

## Global Constraints

- `r2-chNNN`, `ga-NNN`, and numeric chapter number remain stable identity.
- Title is mutable metadata and must answer **Who is Greg in this chapter?**
- No new `role` field.
- No story prose changes below the chapter heading.
- No audio regeneration or binary changes.
- No route/path renumbering.
- Existing approved public R2 role titles are preserved unless a new explicit editorial decision supersedes them.
- Chapter 26 is approved as `The Adventurer`, deliberately duplicating Chapter 23 because the chapter explicitly frames maintenance, spending, recovery, and choosing not to work as part of embodied adventuring.

---

### Task 1: Durable doctrine and audit

**Files:**
- Create: `r2/TITLE_POLICY.md`
- Create: `r2/TITLE_ROLE_AUDIT.md`
- Modify: `r2/README.md`

**Interfaces:**
- Consumes: existing Run 1 role-title doctrine and R2 stable-identity policy.
- Produces: the human editorial authority used by Tasks 2-5.

- [ ] **Step 1: Record the title contract**

Write `r2/TITLE_POLICY.md` with the exact rule that selected titles answer `Who is Greg in this chapter?`, allowed role classes, failure classes, duplicate-role policy, stable identity boundary, and downstream propagation order.

- [ ] **Step 2: Record the current-frontier audit**

Create `r2/TITLE_ROLE_AUDIT.md` with Chapters 1-26 and these approved results:

```text
1  The Boy -> KEEP
2  Two Things -> The Novice
3  The Borrower -> KEEP
4  Thirty Days -> The Contractor
5  The Partner -> KEEP
6  The First Customer -> The Troubleshooter
7  The Extra Guard -> KEEP
8  Road Work -> The Defender
9  The Bridge -> The Backstop
10 What Moved -> The Returner
11 The North Gate -> The Gate Hand
12 Mara -> The Stranger
13 The Good Sword -> The Fighter
14 The Back Room -> The Helper
15 The Morning Barge -> The Friend
16 Three Names -> The Investor
17 The Wrong Rope -> The Extra Hand
18 Six Weeks -> The Applicant
19 Who Cleans It -> The Maintainer
20 Ward Hand -> KEEP
21 The Reply -> The Letter Writer
22 The Neighbor -> KEEP
23 The Adventurer -> KEEP
24 The Watchman -> KEEP
25 The Hired Sword -> KEEP
26 The Day Off -> The Adventurer
```

Each rename gets one short Greg-role rationale. Do not reopen clean titles for polish.

- [ ] **Step 3: Link the policy from R2 routing docs**

Add `TITLE_POLICY.md` and `TITLE_ROLE_AUDIT.md` to the R2 README authority map.

- [ ] **Step 4: Verify documentation scope**

Check that docs contain no claim that title owns identity and no instruction to create a second role field.

- [ ] **Step 5: Commit**

Commit message: `docs: establish R2 role title authority`

---

### Task 2: Failing parity tests

**Files:**
- Create: `tests/test_r2_role_titles.py`

**Interfaces:**
- Consumes: `r2/TITLE_ROLE_AUDIT.md`, selected written files, chapter manifests, registry, and audio manifest.
- Produces: failing regression coverage that Task 3 must satisfy.

- [ ] **Step 1: Write a selected-heading parser test**

Test that `r2/assets/written/ch002.md` is expected to have heading `# Chapter 2: The Novice`. This must fail before migration because main currently says `Two Things`.

- [ ] **Step 2: Write current-frontier expected-title snapshot**

Define the approved map for Chapters 1-26 and assert every selected written heading equals it.

- [ ] **Step 3: Write cross-surface parity tests**

For every chapter 1-26:

```python
self.assertEqual(public_manifest['title'], expected_title)
self.assertEqual(registry['chapters'][chapter_id]['title'], expected_title)
```

For every existing `ga-NNN` audio entry, assert its `title` equals the same expected title by numeric chapter number.

- [ ] **Step 4: Write stable-identity assertions**

Assert chapter IDs, display numbers, manifest audio paths, and project ordering remain numeric/stable and are not derived from title text.

- [ ] **Step 5: Verify RED**

Run:

```bash
python -m unittest tests.test_r2_role_titles -v
```

Expected: FAIL on known drift such as Chapter 2 selected heading and stale audio title metadata.

- [ ] **Step 6: Commit failing tests**

Commit message: `test: expose R2 role title drift`

---

### Task 3: Deterministic title reconciler

**Files:**
- Create: `scripts/sync_r2_role_titles.py`
- Modify: `tests/test_r2_role_titles.py`

**Interfaces:**
- Consumes: selected written headings as semantic title authority after Task 4 migration.
- Produces: `collect_drift(root: Path) -> list[str]`, `apply_titles(root: Path) -> list[Path]`, CLI `--check` / `--apply`.

- [ ] **Step 1: Implement heading parsing**

Use a strict first-line regex:

```python
HEADING_RE = re.compile(r'^# Chapter (?P<number>\d+): (?P<title>.+)$')
```

Reject a file whose numeric heading does not match its `chNNN.md` filename.

- [ ] **Step 2: Implement public-manifest reconciliation**

For each chapter in `r2/data/project.json`, read `r2/data/chapters/chNNN.json` and replace only its `title` value when different from selected written authority.

- [ ] **Step 3: Implement registry reconciliation**

Key by `r2-chNNN`, replace only `chapters[chapter_id]['title']`, and preserve all pipeline/status/image fields unchanged.

- [ ] **Step 4: Implement audio metadata reconciliation**

For each audio manifest entry, use `number` / `ga-NNN` stable identity and replace only `title`. Never infer a missing chapter from title mismatch.

- [ ] **Step 5: Implement check/apply CLI**

`--check` exits nonzero and prints drift lines. `--apply` rewrites JSON with stable formatting and reports changed paths. It must not modify MP3s, paths, IDs, numbers, notes, durations, take counts, or prose body text.

- [ ] **Step 6: Verify GREEN against fixture/temp-copy tests**

Add temporary-directory tests proving `--apply` changes only title fields and leaves representative stable fields untouched.

Run:

```bash
python -m unittest tests.test_r2_role_titles -v
```

Expected: reconciler unit tests PASS; repository snapshot tests remain RED until Task 4 migrates headings.

- [ ] **Step 7: Commit**

Commit message: `feat: add R2 role title reconciler`

---

### Task 4: Promote approved role titles into selected authority

**Files:**
- Modify headings only: `r2/assets/written/ch002.md`, `ch004.md`, `ch006.md`, `ch008.md`, `ch009.md`, `ch010.md`, `ch011.md`, `ch012.md`, `ch013.md`, `ch014.md`, `ch015.md`, `ch016.md`, `ch017.md`, `ch018.md`, `ch019.md`, `ch021.md`, `ch026.md`
- Modify via reconciler: `r2/data/chapters/chNNN.json` only where needed, `r2/data/chapter-registry.json`, `greg-again/audio/manifest.json`

**Interfaces:**
- Consumes: approved audit map from Task 1 and reconciler from Task 3.
- Produces: one canonical role title on all selected/public metadata surfaces.

- [ ] **Step 1: Change only first-line headings**

Replace each listed old heading with the approved role title. Preserve every byte after the first line.

- [ ] **Step 2: Apply deterministic reconciliation**

Run:

```bash
python scripts/sync_r2_role_titles.py --apply
```

- [ ] **Step 3: Verify parity**

Run:

```bash
python scripts/sync_r2_role_titles.py --check
python -m unittest tests.test_r2_role_titles -v
python -m unittest tests.test_r2_site -v
```

Expected: PASS.

- [ ] **Step 4: Verify no forbidden changes**

Confirm no `.mp3`, take-map, route, navigation identity, chapter IDs, numeric ordering, or prose body changes occurred.

- [ ] **Step 5: Commit**

Commit message: `fix: promote R2 embodied role titles`

---

### Task 5: Forward routing and CI guard

**Files:**
- Modify: `r2/WRITTEN_PRODUCTION.md`
- Modify: `r2/AUDIO_PRODUCTION.md`
- Modify: `tests/test_r2_site.py`

**Interfaces:**
- Consumes: canonical title policy and `scripts/sync_r2_role_titles.py`.
- Produces: future workers route title changes through one authority and normal tests catch drift.

- [ ] **Step 1: Add written-selection rule**

Require selected/public chapter headings to pass the embodied-role test before publication. Working titles may remain non-role before selection.

- [ ] **Step 2: Add audio identity rule**

State that audio uses chapter number / `ga-NNN` as identity; title metadata follows selected written R2 authority and may change without synthesis or ownership changes.

- [ ] **Step 3: Add site regression hook**

Extend `tests/test_r2_site.py` to invoke/check the title parity contract or assert the policy/reconciler is wired into the repository.

- [ ] **Step 4: Run full focused verification**

Run:

```bash
python scripts/sync_r2_role_titles.py --check
python -m unittest tests.test_r2_role_titles -v
python -m unittest tests.test_r2_site -v
```

Then run the repository's normal relevant test discovery if CI exposes additional failures.

- [ ] **Step 5: Commit**

Commit message: `docs: route R2 titles through selected authority`

## Final verification

Before merge:

```bash
python scripts/sync_r2_role_titles.py --check
python -m unittest tests.test_r2_role_titles -v
python -m unittest tests.test_r2_site -v
git diff --check
```

Compare the branch against newest `main`, reconcile any concurrent audio/publication changes by stable chapter number, rerun checks, and merge only from a fresh green PR head.
