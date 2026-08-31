# GitHub-First Asset Archaeology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove GitHub can replace routine full-project ZIP handoffs and add non-destructive repository, manuscript, reader, and image archaeology.

**Architecture:** Use small Python standard-library modules to extract factual manifests and validation results from the current tree. Preserve human judgment in Markdown audit documents and keep reader changes within the existing static HTML/CSS architecture.

**Tech Stack:** Python 3 standard library, unittest, static HTML/CSS/JavaScript, Git/GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-31-github-first-asset-archaeology-design.md`

## Global Constraints

- Do not delete manuscript prose, image sources, external artifacts, or Git history.
- Do not generate new illustrations or modify story prose.
- Protect `Peg_Leg_Greg_Heavy_Edit.md` as active unique external editorial work.
- Classify external ZIP families only from traced GitHub evidence and explicit verification requirements.
- Keep the first PR non-destructive and reviewable.

---

### Task 1: Repository and manuscript inventory

**Files:**
- Create: `scripts/project_audit.py`
- Create: `test_project_audit.py`
- Create: `publishing/repository_inventory.json`

**Interfaces:**
- Produces: `inventory_repository(root: Path) -> dict`
- Produces: `detect_manuscript_ranges(root: Path) -> list[dict]`

- [ ] Write failing unittest cases using temporary repositories with active, historical, generated, and unknown files.
- [ ] Run `python -m unittest test_project_audit.RepositoryInventoryTests -v` and verify failures cite missing interfaces.
- [ ] Implement deterministic path, size, hash, reference, and manuscript-range extraction.
- [ ] Run the focused tests and verify they pass.
- [ ] Generate the repository inventory from the real tree.

### Task 2: Image manifest and chapter coverage

**Files:**
- Modify: `scripts/project_audit.py`
- Modify: `test_project_audit.py`
- Create: `publishing/image_asset_manifest.json`
- Create: `publishing/chapter_art_coverage.json`

**Interfaces:**
- Produces: `inventory_images(root: Path) -> list[dict]`
- Produces: `chapter_art_coverage(root: Path, images: list[dict]) -> dict`

- [ ] Write failing tests for PNG/JPEG dimensions, image references, duplicate hashes, broken references, unused assets, and chapters with zero/one/multiple images.
- [ ] Run focused tests and verify expected failures.
- [ ] Implement image-header parsing and HTML reference extraction without third-party dependencies.
- [ ] Run focused tests and verify they pass.
- [ ] Generate both real manifests.

### Task 3: Project validation commands

**Files:**
- Create: `scripts/project_check.py`
- Create: `test_project_check.py`
- Modify: stale reader-count tests where their asserted authority is demonstrably obsolete.

**Interfaces:**
- CLI: `python scripts/project_check.py manuscript|reader|assets|all`

- [ ] Write failing subprocess tests for each command and its JSON-readable diagnostics.
- [ ] Run focused tests and verify expected failures.
- [ ] Implement minimal checks for chapter sequence, duplicate chapters, em dashes, canonical-name hazards, broken links/images, unused assets, duplicate hashes, and image thresholds.
- [ ] Update stale tests to distinguish illustrated pages 1–155 from preview pages 220–221.
- [ ] Run focused and full unittest suites.

### Task 4: GitHub-first and external cleanup audits

**Files:**
- Modify: `AGENTS.md`
- Modify: `state/HANDSHAKE_PROTOCOL.md`
- Create: `state/REPOSITORY_ASSET_AUDIT.md`
- Create: `state/EXTERNAL_HANDOFF_CLEANUP_AUDIT.md`
- Create: `state/CHATGPT_LIBRARY_CLEANUP_HANDOFF.md`

**Interfaces:**
- Consumes the generated inventory, Git history, repository authority files, and observed external filename families.

- [ ] Trace every active lane and identify GitHub authority gaps.
- [ ] Compare major checkpoint generations against Git history/current files.
- [ ] Classify external families as safe-after-name-match, verify-then-remove, keep/archive, do-not-delete, or unknown.
- [ ] Document manuscript overlaps, image/source safety, storage estimates, cleanup candidates, and heavy-edit migration recommendation.
- [ ] Add a compact GitHub-first handoff rule and explicit exceptions.

### Task 5: Reader image presentation

**Files:**
- Modify: `assets/reader.css`
- Modify: chapter HTML only when mechanical attributes are safely added.
- Create or modify: reader presentation tests.

**Interfaces:**
- Preserves current reader identity and image paths.

- [ ] Inspect actual computed conventions and select only evidence-backed fixes.
- [ ] Write failing tests for the selected presentation behavior.
- [ ] Run focused tests and verify expected failures.
- [ ] Implement restrained sizing/layout/lazy-loading changes.
- [ ] Run focused and full tests.

### Task 6: Verification and PR

**Files:**
- Update generated manifests and audit documents with final evidence.

- [ ] Run `python -m unittest discover -v`.
- [ ] Run all four project-check commands.
- [ ] Inspect `git diff --stat`, `git diff --check`, generated-data determinism, and forbidden manuscript/image deletions.
- [ ] Commit in reviewable units, push the branch, and open a non-destructive PR.
- [ ] Record exact verification results and the next cleanup prompt.
