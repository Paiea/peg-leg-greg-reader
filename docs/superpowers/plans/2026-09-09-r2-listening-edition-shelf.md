# R2 Listening Edition Shelf Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/greg-again/audio/` into a light-mode, editorial R2 Listening Edition with a derived availability strip, manifest-driven illustrated chapter cards, and optional stable-ID presentation metadata that never blocks audio playback.

**Architecture:** Keep `greg-again/audio/manifest.json` as the sole authority for chapter number, title, duration, audio source, and publication. Add `greg-again/audio/presentation.json` as optional display metadata keyed only by stable `ga-NNN` identity, then have `player.js` join the sources at runtime. HTML/CSS own the page shell and light-mode visual hierarchy; JavaScript owns derived counts, resilient presentation metadata loading, card rendering, and image fallback behavior.

**Tech Stack:** Static HTML, CSS, vanilla browser JavaScript, JSON manifests, Python `unittest` repository contracts, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-09-r2-listening-edition-shelf-design.md`

## Global Constraints

- Audio remains the primary public R2 experience; written chapters remain a secondary reference surface.
- `greg-again/audio/manifest.json` remains authoritative for stable identity, number, title, duration, audio source, and publication state.
- Presentation metadata is optional and keyed by stable `ga-NNN` identity; it must not duplicate mutable title, duration, publication state, or audio source.
- Audio publication must never depend on art or quote availability.
- The public page must not expose experiment, lab, approved render, take count, lens, provider, or production-note language.
- Default visual mode is warm light mode: cream/paper background, dark ink/brown type, muted maroon accents, restrained borders, art supplying most color.
- Desktop chapter cards use two columns when space permits; mobile uses one column.
- Missing presentation metadata, image, or quote must degrade to a complete playable text-first card.
- A title rename must not break art association because joins happen through stable `ga-NNN` identity.
- Native accessible audio controls remain the playback surface.
- No custom streaming player, account progress, story rewrite, audio regeneration, or requirement to create chapter art before page architecture ships.

---

## Implementation tasks

1. Define failing site contracts for light mode, runtime-derived availability, stable-ID presentation metadata, and graceful fallback behavior.
2. Rework the audio HTML shell and CSS into the approved warm, editorial Listening Edition layout.
3. Add `presentation.json` as optional stable-ID presentation authority only.
4. Update `player.js` to join audio and presentation metadata, derive availability, render optional art/quotes, and preserve playback when presentation assets are absent.
5. Reconcile newest `main`, run focused R2 tests, Greg Again audio validation, the full repository suite, inspect the final diff, and merge only with fresh green PR-head checks.
