# R2 Audio Library Remix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing R2 Audio Library into the flagship listen-first experience using the current static architecture, reused patterns from existing Paiea readers, and replaceable hero/chapter art slots.

**Architecture:** Preserve the existing static HTML/CSS/vanilla-JS audio page and audio manifest. Reuse proven responsive shelf and localStorage patterns from the Falling Off a Cliff reader, keep native audio controls for the first pass, and add lightweight search, resume state, written-rendition links, and image fallbacks without adding a framework or database.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, JSON manifests, GitHub Pages, Python unittest site contract.

**Spec:** Approved conversation direction for R2 Audio Library, September 10, 2026.

## Global Constraints

- R2 is audio-first. The page must say `LISTEN FIRST` and visually prioritize playback over reading.
- Reading remains available but secondary.
- No React or new framework.
- No database or account system.
- Keep native audio controls for this pass.
- Preserve stable chapter numbers and audio files.
- Hero art is replaceable and must fall back to current R2 cover assets until the new high-quality artwork is uploaded.
- Chapter artwork is optional and must not block playback.
- No em dashes in reader-facing copy.

---

### Task 1: Add the Audio Library site contract

**Files:**
- Modify: `tests/test_r2_site.py`

**Interfaces:**
- Consumes: current audio page files under `greg-again/audio/`
- Produces: regression assertions for listen-first copy, search, resume storage, written links, responsive grid, and fallback hero art

- [ ] Add assertions that the Audio Library includes `AUDIO LIBRARY`, `LISTEN FIRST`, `Reading available. Listening is the point.`, a search input, and a continue-listening region.
- [ ] Assert player JS uses `localStorage`, renders written-rendition links, supports search filtering, and keeps native `audio` controls.
- [ ] Assert CSS contains a responsive card grid with three-column desktop and one-column mobile behavior.
- [ ] Assert the hero references new Audio Library art paths with current R2 cover fallbacks.

### Task 2: Rebuild the Audio Library shell

**Files:**
- Modify: `greg-again/audio/index.html`

**Interfaces:**
- Consumes: `manifest.json`, `player.js`, existing R2 cover images
- Produces: semantic page structure for hero, warning, resume card, controls, and chapter grid

- [ ] Replace the explanatory hero with a compact visual hero headed `AUDIO LIBRARY`.
- [ ] Add the warning treatment `LISTEN FIRST` and support line `Reading available. Listening is the point.`.
- [ ] Add a `continue-listening` region that player JS can populate.
- [ ] Add a search input and simple availability/length controls.
- [ ] Keep navigation compact and make Listen current.
- [ ] Add `<picture>` sources for `r2-audio-library-portrait.webp` and `r2-audio-library-wide.webp`, with JS-free fallback behavior to current R2 cover assets via `onerror`.

### Task 3: Reuse proven shelf and progress behavior

**Files:**
- Modify: `greg-again/audio/player.js`

**Interfaces:**
- Consumes: `manifest.json`, Audio Library DOM regions
- Produces: chapter cards, search filtering, native audio playback, per-chapter resume state, and written-rendition links

- [ ] Use a namespaced localStorage record for current chapter and playback time.
- [ ] On `timeupdate`, save chapter number and current time with defensive parsing.
- [ ] On page load, render Continue Listening when saved progress points to a published audio chapter.
- [ ] Ensure only one audio element plays at a time.
- [ ] Render cards with chapter number, title, duration, native audio controls, and `Written rendition →` linking to `../../r2/chapter.html?id=r2-chNNN`.
- [ ] Filter cards live by chapter number/title search.
- [ ] Add lightweight duration filtering without inventing arc/location metadata.
- [ ] Render safely when metadata or storage is missing.

### Task 4: Apply the R2 remix visual system

**Files:**
- Modify: `greg-again/audio/audio.css`
- Modify: `greg-again/audio/audio-front-door.css`

**Interfaces:**
- Consumes: semantic classes from Task 2 and card markup from Task 3
- Produces: dark Carrow/remix presentation with loud identity layer and clean controls

- [ ] Preserve dark charcoal base and accessibility contrast.
- [ ] Add cyan, marker-yellow, and rough-paper accent variables.
- [ ] Style the hero as an image-led poster rather than a prose block.
- [ ] Style the listen-first warning as a slapped-on hazard sticker.
- [ ] Convert chapter list to a responsive visual card grid.
- [ ] Keep native audio controls readable and uncluttered.
- [ ] Keep written links visibly secondary.
- [ ] Make mobile layout one-column with comfortable touch targets.

### Task 5: Verify and integrate

**Files:**
- Verify: `tests/test_r2_site.py`
- Verify: `greg-again/audio/index.html`
- Verify: `greg-again/audio/player.js`
- Verify: `greg-again/audio/audio.css`
- Verify: `greg-again/audio/audio-front-door.css`

- [ ] Run the repository R2 site contract.
- [ ] Inspect the final diff for accidental story/audio-manifest changes.
- [ ] Verify the page still uses the existing durable audio manifest and MP3 assets.
- [ ] Open a PR against `main` only after the available automated verification is green.
- [ ] Leave new hero artwork as a replaceable asset upload, not a merge blocker.
