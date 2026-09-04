# Chapter Renumber After 220 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace provisional Chapters 220A/220B/220C with canonical Chapters 221/222/223 and shift every former Chapter 224+ forward by three without changing prose chronology.

**Architecture:** Run one deterministic repository migration in a full GitHub Actions checkout. Restore the non-empty running manuscript from pre-integration authority if necessary, integrate the three inserted chapters into the running manuscript, renumber later source/checkpoint files and chapter references, regenerate reader derivatives, then verify continuity and stale-number conditions before committing atomically.

**Tech Stack:** Python 3.12, git, existing Peg-Leg Greg reader generation/verification scripts, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-03-plg-memory-bren-revision-design.md`

## Global Constraints

- Former 220A becomes 221, 220B becomes 222, 220C becomes 223.
- Every former numeric Chapter 224+ becomes old number + 3.
- Chapter 220 remains Chapter 220.
- Prose chronology and chapter prose do not change except chapter labels and reference numbers.
- No em-dash prose cleanup or unrelated revision is part of this migration.
- Greg magic counts, money, character facts, and unresolved plot facts must not change.
- Vale/Bren linkage remains unresolved.

### Task 1: Source migration

- [ ] Restore the running manuscript from commit `90615b90d1fbddbed632ef18dba8ade64c919af6` if the branch copy is empty.
- [ ] Renumber running-manuscript Chapters 221+ by +3.
- [ ] Normalize and insert provisional 220A/220B/220C as numeric Chapters 221/222/223.
- [ ] Renumber exact checkpoint filenames/content from old 249+ to +3.
- [ ] Remove obsolete alphanumeric canonical source files after integration.

### Task 2: Durable state/reference migration

- [ ] Update contextual chapter references (`Chapter N`, `ChN`, checkpoint filenames, chapter URLs/query parameters) for old 221+ to +3.
- [ ] Replace 220A/B/C state references with 221/222/223.
- [ ] Rebuild `MANUSCRIPT_CHAPTER_INDEX.md` from the migrated source authority through the latest chapter.
- [ ] Update endpoint state from old 301 to new 304 where chapter-context semantics require it.

### Task 3: Reader/site regeneration

- [ ] Rebuild preview chapter wrappers for Chapters 220 through the new endpoint.
- [ ] Generate the Light edition from migrated source files.
- [ ] Update home contents/navigation and latest page using existing scripts.
- [ ] Preserve Book I/II/III chapter-art semantics while shifting chapter-number references where required.

### Task 4: Verification

- [ ] Run unit tests.
- [ ] Run existing Light verification for recovered and current ranges.
- [ ] Verify numeric sequence `220, 221, 222, 223, 224` maps to `THE LANDLORD, THE SHORTAGE, THE OLD MAN, THE ROUTE, THE PARTICIPANT`.
- [ ] Verify latest old 301 is now 304.
- [ ] Verify no canonical `220A`, `220B`, or `220C` chapter labels/URLs remain outside archival/editorial history notes.
- [ ] Verify no old numeric checkpoint filenames remain at 249+ under their pre-migration numbers.
- [ ] Run `git diff --check`.
- [ ] Commit the migration atomically with `[renumber-done]` in the commit message to prevent workflow recursion.
