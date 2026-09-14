# R2 Three-Year Seam Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the intended R2 continuation as one accumulated chronology: recovered Chapters 40–42, the one-year Black Stair run, a return-home seam, then the two-year Halden run, ending at Chapter 118.

**Architecture:** Preserve exact reviewed prose blobs wherever continuity already works. Promote the Black Stair year as Chapters 43–82, add one reader-facing return chapter as Chapter 83, and shift the existing two-year Halden prose from current Chapters 40–74 to Chapters 84–118. Re-perform only false-reset seams and remove literal drafting/meta leakage. The public R2 manifest/navigation becomes contiguous 1–118.

**Tech Stack:** Static Markdown story assets, JSON chapter manifests, GitHub Pages reader, Python unittest site contract.

**Spec:** Approved conversation direction plus `r2/TEMPORAL_ENGINE.md`, `r2/WRITTEN_PRODUCTION.md`, and the completed Black Stair temporal-year audit.

## Global Constraints

- Character before system; time must leave residue.
- No em dashes in reader-facing prose.
- Preserve exact successful scenes rather than rewriting for polish.
- No soft reset between temporal runs.
- Later material inherits Silver rank, Blackglass Anchor history, Mara/Halden history, recurring roads, Field Support Three, Westreach, money/reputation, and accumulated relationships.
- Greg's later permanent left-leg loss remains the earned Brell consequence already discovered in the two-year run.
- The Halden rendezvous remains the two-year hard date and emotional endpoint.
- Planner/rehearsal labels must not appear in rendered reader prose.
- Audio/images may lag written publication and do not block written chapters.

---

### Task 1: Recover the true frontier and Black Stair year

**Files:**
- Replace: `r2/assets/written/ch040.md`–`ch042.md`
- Replace/create: `r2/assets/written/ch043.md`–`ch082.md`

- [ ] Restore exact true-frontier Chapters 40–42 from `experiment/r2-temporal-year-043-plus`.
- [ ] Map temporal-year chapters 01–40 to public Chapters 43–82 in chronological order.
- [ ] Remove literal reader-facing drafting notes identified by the temporal-year audit without changing scene outcomes.
- [ ] Fix only continuity wording that becomes false under the accepted sequence.

### Task 2: Build the year-to-years seam

**Files:**
- Replace: `r2/assets/written/ch083.md`
- Replace/create: `r2/assets/written/ch084.md`–`ch118.md`

- [ ] Write Chapter 83 as the return from Black Stair/Westreach to Carrow, carrying Silver status, Field Support Three experience, Blackglass Anchor wear, and accumulated relationships home.
- [ ] Shift the reviewed two-year Halden run from old public slots 40–74 into 84–118.
- [ ] Re-perform Chapter 84 so Mara's two-year Vey term is a new fixed appointment/promotion after her already-lived Halden year, not a first six-week trial.
- [ ] Convert the later duplicate Silver-promotion beat into removal of Greg's municipal structural-magic restriction / broader certification rather than a second rank promotion.
- [ ] Update false first-time and elapsed-time references, especially Noll/Brass Spoon, Mara/Halden, Brell history, road familiarity, and Greg's professional baseline.
- [ ] Preserve the earned leg-loss, angry S-class recovery turn, Faultglass theft/return, and D730 Halden meeting.

### Task 3: Rebuild public chapter manifests and authority

**Files:**
- Replace/create: `r2/data/chapters/ch040.json`–`ch118.json`
- Modify: `r2/data/project.json`
- Modify: `r2/PUBLIC_REBUILD_AUTHORITY.md`
- Modify: `r2/data/chapter-registry.json` if its current schema can be advanced without restoring superseded quarry authority.

- [ ] Publish a contiguous written sequence 1–118.
- [ ] Set `current_chapter` to `r2-ch118`.
- [ ] Wire previous/next navigation through 118.
- [ ] Keep audio unavailable where no durable audio exists and images empty where no accepted art exists.
- [ ] Record that Chapters 40–118 are the author-selected three-year continuation; old pre-rebuild 40+ files remain superseded quarry.

### Task 4: Update and run the site contract

**Files:**
- Modify: `tests/test_r2_site.py`

- [ ] Change the public-frontier contract from 74 to 118.
- [ ] Assert manifests, Markdown assets, and navigation are contiguous through 118.
- [ ] Assert public authority names Chapter 118.
- [ ] Run `python -m unittest tests.test_r2_site -v` through the repository workflow.
- [ ] Fix only real integration failures, not unrelated historical tests.

### Task 5: Integrate safely

- [ ] Compare `editor/r2-three-year-seam` against newest `main` and preserve newer unrelated authority.
- [ ] Verify Chapter 39 points to recovered Chapter 40 and Chapter 118 has no next chapter.
- [ ] Verify representative prose seams: 42→43, 82→83, 83→84, pre-loss→Brell, post-loss, Faultglass, 118.
- [ ] Fast-forward/merge to `main` only after the R2 site contract is green.
- [ ] Re-read final `main` and report the durable public frontier.