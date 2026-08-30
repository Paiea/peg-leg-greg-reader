# Illustrated Novel Presentation Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the existing 82-chapter Peg-Leg Greg reader feel more intentionally like an illustrated novel without changing prose, art anchors, titles, order, or reader architecture.

**Architecture:** Preserve all existing HTML structure and artwork. Make restrained CSS refinements to chapter openings and the three existing illustration roles, then add only three semantic threshold classes to chapter shells at manuscript-supported transitions. Leave homepage content and artwork unchanged because the current frontispiece-first entry already meets the brief.

**Tech Stack:** Static HTML/CSS.

**Spec:** User-provided Illustrated Novel Presentation Pass prompt in current conversation.

## Global Constraints
- No prose changes.
- No chapter title/number/order changes.
- No image anchor movement or artwork replacement.
- No DEVELOPMENT art promotion.
- No new subsystem or interactive feature.
- Preserve self-contained static reader and mobile intrinsic image sizing.

---

### Task 1: Refine chapter-opening and illustration rhythm
**Files:** Modify `assets/reader.css`.
- [ ] Tighten chapter-number/title hierarchy while keeping the existing typography family and restrained rule.
- [ ] Make sketch/scene/feature spacing visibly distinct as reading rhythm, with mobile-safe intrinsic sizing preserved.
- [ ] Add threshold styles that use whitespace/rule emphasis only.
- [ ] Leave homepage content hierarchy untouched.

### Task 2: Mark manuscript-supported narrative thresholds
**Files:** Modify only `chapters/045.html`, `chapters/064.html`, `chapters/075.html`.
- [ ] Add `story-threshold` to Chapter 45 shell for the shift into ordinary Bronze/adventuring work after Chapter 44 explicitly ends with “Tomorrow I would be a Bronze adventurer.”
- [ ] Add `story-threshold story-threshold-major` to Chapter 64 shell for the West River injury/surgery/amputation threshold.
- [ ] Add `story-threshold` to Chapter 75 shell for the return-to-stairs/mobility threshold after the recovery/lodging stretch.
- [ ] Change no other chapter markup.

### Task 3: Validate
- [ ] Verify 82 chapter files and Chapter 82 endpoint/title.
- [ ] Compare all prose text, chapter numbers/titles, image src sequences, and nav hrefs against pre-pass reader.
- [ ] Verify zero DEVELOPMENT/contact-sheet references and zero broken local assets.
- [ ] Verify frontispiece, world map, and gallery still exist.
- [ ] Parse CSS braces and inspect mobile intrinsic image rules structurally.
- [ ] Attempt representative browser/mobile rendering if runtime permits; report limitation if blocked.
