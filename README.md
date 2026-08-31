# PEG-LEG GREG — ILLUSTRATED READER

Open `index.html` in any modern browser.

This repository contains both the illustrated static reader and the durable project/manuscript state used to keep Peg-Leg Greg moving across chats and work sessions.

## Current authority

- Current story endpoint: **Chapter 220 — THE LANDLORD**
- Book 1: Chapters 1–82, CLOSED
- Book 2: ACTIVE
- Current manuscript state: `state/MANUSCRIPT_STATE.md`
- Permanent forward manuscript path: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`

Important: Chapters 156–219 still require exact-text synchronization into the permanent running-manuscript file. Chapter 220 is materialized directly there and new forward chapters should continue on that permanent path. `state/MANUSCRIPT_STATE.md` remains the compact current endpoint/continuity authority.

## Public reader

The static illustrated reader currently publishes **Chapters 1–155**.

The reader is a derived publishing build, not manuscript authority. Do not invent reader Chapters 156–220 from summaries. Synchronize them from authoritative prose when available.

Open `art.html` or click **ART** to browse approved visual material. Only reader-promoted art ships in chapter pages. Development contact sheets and unpromoted production assets are not reader authority.

## Shared project memory

When `project_brain/` is present, it serves as compact durable working memory for plot, characters, worldbuilding, reader production, and cross-chat continuity.

Fresh workers should begin with:

1. `AGENTS.md`
2. `state/MANUSCRIPT_STATE.md`
3. `project_brain/README.md`
4. `project_brain/PROJECT_STATUS.md`
5. the relevant lane-specific project-brain files

The intended workflow is:

**READ REPO -> WORK ONE LANE -> VALIDATE -> UPDATE DURABLE STATE -> HANDOFF -> FRESH WORKER CONTINUES**

GitHub should carry the continuity so dedicated chats are useful but not irreplaceable.

## Reader presentation

The reader intentionally uses mixed-fidelity illustrations. Small raster art should remain near a sensible intrinsic size; stronger feature art may display larger. Mobile behavior should preserve intrinsic aspect ratio and avoid fixed-height image boxes. Do not force full-bleed treatment simply for visual uniformity.