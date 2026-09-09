# R2 Public Rebuild Reroute Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the obsolete public R2 continuation after Chapter 26 with the accepted character-first rebuild through Chapter 35 while preserving the old forward run as historical quarry.

**Architecture:** Keep stable chapter IDs 27–35, replace their public prose and metadata with the accepted rebuild, cap the public manifest and production registry at 35, and archive the old 304-chapter registry intact. Leave old Chapter 36+ files physically present but unreachable from normal public chapter listing/navigation.

**Tech Stack:** Static GitHub Pages reader, JSON chapter manifests, Markdown written surfaces, Python unittest regression coverage.

**Spec:** User-approved reroute in the R2 character-first rebuild session.

## Global Constraints

- Chapters 1–26 remain unchanged.
- Rebuilt Chapters 27–35 become current public R2 authority.
- Old Chapter 36+ files remain repository evidence/quarry, not current story authority.
- Do not publish B/C/D temporal rehearsal material directly.
- Do not attach obsolete images or audio to rewritten Chapters 27–35.
- Chapter 35 must have no public next link until later A material is selected and published.

### Task 1: Preserve and reroute public authority

- [x] Archive the pre-rebuild chapter registry intact.
- [x] Copy accepted reconstructed Chapter 27–35 prose into `r2/assets/written/`.
- [x] Replace Chapter 27–35 public JSON metadata and navigation.
- [x] Cap `r2/data/project.json` at Chapter 35.
- [x] Replace `r2/data/chapter-registry.json` with the accepted 1–35 production frontier.

### Task 2: Protect the reroute

- [x] Add `r2/PUBLIC_REBUILD_AUTHORITY.md`.
- [x] Update R2 site tests to expect a 35-chapter public frontier.
- [x] Verify Chapter 36 remains on disk as historical evidence but is absent from the public manifest.

### Task 3: Integrate safely

- [ ] Compare branch against `main` and inspect changed paths.
- [ ] Run available CI/status checks for the branch head.
- [ ] Merge only after the publication surface is coherent.
- [ ] Verify `main` exposes Chapters 1–35, new titles/prose for 27–35, and no Next link after 35.
