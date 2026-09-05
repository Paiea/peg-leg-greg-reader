# Reader Book and Act Navigation Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the 344+ chapter reader navigable by book first, give Book III a closed multi-act structure, introduce Book IV, and keep both Illustrated and Text readers synchronized.

**Architecture:** Keep `scripts/reader_sections.py` as the single structural authority for Book/Act ranges and labels. Upgrade its rendered hierarchy so books themselves are collapsible navigation units and only the current/latest book opens by default. Preserve act-level disclosure inside a selected book. Shared CSS controls the compact book-first experience; illustrated CSS only adds role-card presentation.

**Tech Stack:** Python 3.12 generation scripts, static HTML/CSS, unittest, GitHub Actions/GitHub Pages.

**Spec:** User-approved chat design on 2026-09-04: four-book reader, acts inside books, collapsible chapter grids, current book obvious, same structure in Illustrated and Text readers, boundaries derived from story movement rather than round chapter numbers.

## Global Constraints

- Exact manuscript prose remains authority.
- Structural boundaries describe story movement and must not manufacture plot.
- Both Illustrated and Text readers use the same Book/Act authority.
- Mobile navigation must avoid forcing a scroll through hundreds of chapter links.
- Existing Book I and Book II boundaries remain 1-82 and 83-180.
- Preserve existing reader URLs and chapter URLs.
- No em dashes in manuscript prose; this task does not alter manuscript prose.

---

### Task 1: Close Book III with an earned third act

**Files:**
- Modify: `scripts/reader_sections.py`
- Modify: `tests/test_reader_sections.py`

**Interfaces:**
- Produces: authoritative Book III closed range and three-act map consumed by both reader generators.

- [ ] Write tests for the closed Book III boundary and third act.
- [ ] Run reader-section tests and confirm failure.
- [ ] Implement the minimal structural map.
- [ ] Run tests and confirm pass.
- [ ] Commit.

### Task 2: Introduce Book IV with acts

**Files:**
- Modify: `scripts/reader_sections.py`
- Modify: `tests/test_reader_sections.py`

**Interfaces:**
- Produces: `BOOK IV` and its current act map, open-ended only at the live frontier.

- [ ] Write failing tests for Book IV range, slug, and acts.
- [ ] Implement Book IV in shared authority.
- [ ] Verify Text and Illustrated renderers both expose it.
- [ ] Commit.

### Task 3: Make Books the primary disclosure level

**Files:**
- Modify: `scripts/reader_sections.py`
- Modify: `tests/test_reader_sections.py`

**Interfaces:**
- Produces: nested Book -> Act -> Chapter disclosure markup.

- [ ] Write failing tests that earlier books are collapsed and latest book opens by default.
- [ ] Wrap each book in semantic `<details>`/`<summary>` navigation.
- [ ] Keep act disclosures nested inside the selected book.
- [ ] Preserve role-card links and accessible headings.
- [ ] Run tests and commit.

### Task 4: Compact the menu/UI for 344+ chapters

**Files:**
- Modify: `assets/book-contents-base.css`
- Modify: `assets/book-contents.css`
- Modify/Test: `tests/test_book_contents_css.py`

**Interfaces:**
- Consumes: nested Book/Act markup from Task 3.
- Produces: compact desktop/mobile book-first navigation without giant default chapter scrolls.

- [ ] Add failing CSS contract tests for book summary/disclosure selectors.
- [ ] Style book summaries as primary navigation cards/rows.
- [ ] Keep chapter grids hidden until their act is opened.
- [ ] Ensure mobile role cards do not dominate the menu.
- [ ] Run CSS tests and commit.

### Task 5: Publish and verify both reader modes

**Files:**
- Modify only if required: `scripts/update_home_contents.py`, `scripts/update_reader_navigation.py`, `.github/workflows/light-edition.yml`
- Generated: `index.html`, `light/index.html`, current chapter derivatives.

**Interfaces:**
- Consumes: Tasks 1-4.
- Produces: live synchronized Illustrated/Text navigation through current manuscript authority.

- [ ] Run complete unittest suite.
- [ ] Generate current Text and Illustrated derivatives.
- [ ] Verify Book I-IV labels, ranges, act labels, latest chapter, cross-mode links, and no broken chapter navigation.
- [ ] Run `git diff --check` equivalent through workflow verification.
- [ ] Publish to `main` and verify GitHub Actions/Pages success before claiming live.
