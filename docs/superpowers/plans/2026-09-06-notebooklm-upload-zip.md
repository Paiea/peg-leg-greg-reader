# NotebookLM Upload ZIP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically package current NotebookLM manuscript exports into one downloadable ZIP without changing the manuscript exporter itself.

**Architecture:** Keep `scripts/build_notebooklm_export.py` responsible only for generating current Markdown sources. Add a small GitHub Actions workflow that watches those generated Markdown files, creates a flat ZIP containing the manuscript sources, structure map, and README, validates the archive, and commits only the ZIP back to `main`. Because the workflow path filter excludes ZIP changes, its own commit does not recurse.

**Tech Stack:** GitHub Actions, bash, `zip`, `unzip`.

**Spec:** User requested one automatically refreshed ZIP for convenient download and local unzip before NotebookLM upload.

## Global Constraints

- Preserve the existing Book/Act Markdown export behavior.
- The ZIP is convenience packaging only and is not itself a NotebookLM source.
- Include all current `PLG_BOOK_*.md` sources, `PLG_STRUCTURE_MAP.md`, and `README.md`.
- Do not include project-brain/state files.
- Avoid recursive workflow triggering.

---

### Task 1: Add upload-package workflow

**Files:**
- Create: `.github/workflows/notebooklm-upload-zip.yml`

**Interfaces:**
- Consumes: `exports/notebooklm/PLG_BOOK_*.md`, `PLG_STRUCTURE_MAP.md`, `README.md`
- Produces: `exports/notebooklm/PLG_NOTEBOOKLM_UPLOAD.zip`

- [x] **Step 1: Define workflow trigger only for NotebookLM Markdown exports and the workflow file itself.**
- [x] **Step 2: Build a flat ZIP from current manuscript sources plus orientation files.**
- [x] **Step 3: Validate archive integrity and required members with `unzip`.**
- [x] **Step 4: Commit the ZIP only when its bytes change.**
- [x] **Step 5: Rebuild after rebasing on moving `main` before push.**

### Task 2: Verify on main

- [ ] **Step 1: Merge the focused PR.**
- [ ] **Step 2: Confirm the packaging workflow completes successfully.**
- [ ] **Step 3: Confirm `exports/notebooklm/PLG_NOTEBOOKLM_UPLOAD.zip` exists on `main`.**
- [ ] **Step 4: Confirm a later NotebookLM Markdown refresh automatically triggers ZIP refresh.**
