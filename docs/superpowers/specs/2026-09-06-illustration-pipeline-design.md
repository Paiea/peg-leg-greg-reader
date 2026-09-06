# Manuscript-Informed Illustration Pipeline Design

## Goal

Create a durable illustration-production system that turns manuscript scenes into a visible art backlog, reusable generation briefs, accepted assets, and verified reader coverage without contaminating canonical prose with production metadata.

## Scope

This design adds a sidecar visual-production subsystem. It does not rewrite manuscript prose, alter visual style rules, replace existing accepted art, or automate final artistic approval.

## Architecture

The pipeline is:

**MANUSCRIPT AUTHORITY → SCENE CANDIDATES → ILLUSTRATION REGISTRY → PROMPT PACKS → GENERATED/APPROVED ASSETS → READER PROMOTION → COVERAGE REPORT**

Canonical prose remains clean. Visual metadata lives under `state/visual/` and refers back to chapter numbers, titles, scene summaries, and natural paragraph anchors.

## 1. Scene candidates

`state/visual/SCENE_CANDIDATES.json` stores manuscript-informed visual moments. Each candidate has:

- `id`
- `chapter`
- `chapter_title`
- `scene_summary`
- `visual_hook`
- `characters`
- `location`
- `mood`
- `priority` (`high`, `medium`, `low`)
- `kind` (`chapter_illustration`, `role_card`, `act_card`, `book_card`)
- `fit_target` (`exact`, `close_enough`)
- `spoiler_level` (`low`, `medium`, `high`)
- `status` (`candidate`, `prompt_ready`, `generated`, `approved`, `live`, `rejected`)
- optional `paragraph_anchor`
- optional `notes`

Scene candidates are production metadata, not canon. A candidate may be regenerated or rejected without changing the manuscript.

## 2. Illustration registry

`state/visual/ILLUSTRATION_REGISTRY.json` is the single source of truth for accepted and in-flight illustration records. Every promoted reader image must have a registry record.

Each record includes:

- `id`
- `candidate_id`
- `chapter`
- `kind`
- `status`
- `style_family`
- `source_asset`
- `live_asset`
- `caption`
- `alt_text`
- `approved_fit`
- `prompt_pack`
- optional `paragraph_anchor`
- optional `notes`

Only records with `status: approved` may be promoted. Promotion changes status to `live` after the reader update succeeds.

## 3. Scene harvesting

`scripts/extract_scene_candidates.py` reads manuscript authority and produces candidate suggestions without editing prose. Initial automation is heuristic and conservative. It should prefer:

- physical action or work
- entrances/exits and directional movement
- unusual environments or stage geometry
- meaningful props or objects
- relationship action rather than posed dialogue
- comedy/recovery beats
- visually legible reveals
- moments with strong camera opportunities

The script outputs suggestions for review; it does not auto-approve them.

## 4. Backlog

`scripts/build_illustration_backlog.py` combines scene candidates, registry state, and current reader coverage into `state/visual/ILLUSTRATION_BACKLOG.md`.

Priority order:

1. missing book/act/role cards
2. live chapters with zero art
3. live chapters with one image
4. high-priority scene candidates
5. weak/mismatched art
6. second/third image opportunities

The existing production-first rule remains authoritative: normal chapters may use `close_enough` art when it is useful and not contradictory.

## 5. Prompt packs

`scripts/build_prompt_packs.py` turns reviewed candidates into Markdown prompt packs under `state/visual/prompt-packs/`.

Each pack includes:

- target id and chapter
- scene summary
- subject/action
- camera/framing
- foreground/environmental movement
- eye path
- manuscript details
- character continuity constraints
- shared `SKETCH + INK + PAINT` style language
- target filename and reader destination
- fit target

Prompt packs support generation consistency but remain editable production briefs.

## 6. Promotion into the reader

`scripts/promote_illustrations.py` is the only automated promotion path. It:

1. validates registry records marked `approved`
2. verifies source and destination paths
3. inserts or updates chapter image markup only at the declared natural anchor
4. updates `art.html` where applicable
5. preserves prose byte-for-byte outside image markup
6. marks records `live` only after successful writes
7. refuses ambiguous anchors or missing metadata instead of guessing

The Text Reader remains image-free.

## 7. Coverage report and CI

`scripts/report_illustration_coverage.py` writes `state/visual/ILLUSTRATION_COVERAGE.md` with:

- live manuscript frontier
- illustrated chapter count
- zero/one/two/three+ image chapter counts
- approved-but-unpublished count
- queued candidate count
- role/act/book card completeness

Tests must reject:

- a live image missing from the registry
- a registry `live_asset` that does not exist
- approved/live art without alt text
- duplicate registry ids
- a live chapter image path not represented in the registry
- Text Reader image leakage
- promotion that changes prose outside image markup

## 8. Manuscript integration policy

The Manuscript Engine may nominate strong visual moments as sidecar scene candidates after a chapter is durably accepted. It must not insert production tags into canonical prose. Candidate extraction may run later in batch form, so forward manuscript throughput is not blocked by art production.

A chapter does not need an illustration candidate if no scene is visually worthwhile. The system should prefer fewer useful candidates over mechanically tagging every chapter.

## 9. Generation policy

Image generation remains an explicit production action, not an automatic CI side effect. The repository prepares deterministic prompt packs and destinations; a visual worker or image-generation tool creates the asset, a human/visual review marks it approved, then the promotion script integrates it.

This preserves artistic judgment while making backlog, naming, continuity, and reader integration repeatable.

## Success criteria

- A fresh worker can answer what art is missing from repository state alone.
- A manuscript chapter can nominate one or more strong scenes without altering prose.
- A reviewed candidate can become a deterministic prompt pack.
- An approved image can be promoted once and wired into all required reader surfaces.
- CI catches broken/missing image paths and registry drift.
- The system scales while the manuscript continues advancing independently.