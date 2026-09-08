# PLG Visual Evidence, Temporal State, and Purpose-Aware Presentation

## Status

Approved Definitive Edition architecture extension to the bounded visual pilot.

## Authority

- Canon prose remains the only story authority.
- PERFORMANCE archives remain `derived_editorial_reference` only and may be consumed only through their existing freshness and exact-scene-anchor boundary.
- Visual scene evidence is generated, rebuildable, noncanon editorial state.
- Temporal character visual state is sparse editorial continuity state. It may constrain generation but may not invent story facts.
- `ILLUSTRATION_APPROVALS.json` is the persistent creator-taste layer for concrete assets.
- Reader presentation state is generated from approved/live registry state and must never become story authority.

## Pipeline

```text
CANON + SCENE CANDIDATES + fresh scene-local PERFORMANCE + temporal visual state + current art
    -> generated VISUAL_SCENE_EVIDENCE.json
    -> generation queue / prompt packs
    -> concrete generated asset
    -> ILLUSTRATION_APPROVALS.json creator judgment
    -> registry
    -> generated READER_PRESENTATION.json
    -> static Illustrated Reader
```

Do not create a second durable approval system. `BOUNDED_GENERATION_APPROVALS.json` remains only a temporary generation-authorization overlay required by the current structural hold. It is not the creator-taste store.

## Rebuildable visual scene evidence

Create `state/visual/VISUAL_SCENE_EVIDENCE.json` by script. Each scene record should preserve only derived, reproducible visual preproduction facts:

- candidate id, chapter, title, paragraph anchor;
- scene summary, visual hook, characters, location, mood, scene tags;
- exact current live/approved art records for the chapter as comparison context;
- resolved temporal visual state for each character when available;
- fresh exact-scene PERFORMANCE visual reference when available;
- an evidence condition label such as `prose_only`, `prose_temporal`, or `prose_temporal_performance`.

The generator must use the existing PERFORMANCE freshness loader and exact anchor matching behavior. A stale archive or nonmatching scene anchor contributes nothing.

The file is safe to delete and rebuild. No hand edits belong in it.

## Temporal character visual state

Create `state/visual/CHARACTER_VISUAL_TIMELINE.json` as sparse interval state. Each entry has:

- `character`
- `state_id`
- `chapter_start`
- optional `chapter_end`
- `authority: derived_editorial_reference`
- `canon_authority: false`
- `evidence`
- `appearance`
- `body_state`
- `mobility_state`
- optional `must_show` / `must_not_show`

Intervals may not overlap for the same character. Unknown chapters return no temporal state rather than inheriting an invented one.

Seed only states supported by current evidence. For the present pilot:

- Greg chapters 1–18: pre-amputation, both legs intact, no crutches/prosthesis, young Greg with light beard/stubble/fuzz rather than clean-shaven presentation.
- Greg chapters 496–499: later prosthetic fitting/trial period, with two crutches remaining normal backup mobility and prosthetic use bounded to supervised trial evidence.

The late state is a visual constraint, not a statement that every moment in chapters 496–499 visibly uses the prosthesis.

Scene-local explicit continuity remains allowed and wins over interval defaults when it is more specific.

## Creator taste in the existing approval layer

Extend concrete `ILLUSTRATION_APPROVALS.json` approval records with optional creator-taste fields:

- `presentation_role`: `sketch-beat`, `scene-illustration`, `feature-illustration`, or `feature-portrait`;
- `editorial_purpose`: short nonempty text explaining what the image earns in the reading experience;
- `editorial_note`: optional freeform judgment/review note.

On approval, these fields are copied into the illustration registry. Rejections remain rejections and require a reason.

Defaults preserve current behavior: an approved asset without a presentation role renders as `scene-illustration`.

The approval layer remains asset-specific. It does not make PERFORMANCE or visual-scene evidence canon.

## Generated purpose-aware reader presentation

Create `state/visual/READER_PRESENTATION.json` from live registry records. The generator maps each live chapter illustration to:

- chapter
- asset
- paragraph anchor
- presentation role
- editorial purpose
- alt text
- caption

The Illustrated Reader consumes this generated state for figure classes. Existing CSS role families are reused:

- `sketch-beat`
- `scene-illustration`
- `feature-illustration`
- `feature-illustration feature-portrait`

No JavaScript reader rewrite is required. Static chapter URLs and Showcase navigation remain unchanged.

## Pilot integration

The current five generation candidates should gain generated visual-scene evidence immediately:

- Ch005 gambling and training remain prose-led controls but receive Greg's early temporal state.
- Ch007, Ch013, Ch018 receive both early temporal state and fresh scene-local PERFORMANCE evidence when their exact anchors still match.

This preserves the A/B value while fixing continuity at a general system level.

## Success criteria

- Visual scene evidence can be deleted and rebuilt deterministically from authoritative inputs.
- Stale or anchor-mismatched PERFORMANCE evidence never enters visual scene evidence.
- Temporal lookup returns the correct early Greg state for Ch005/007/013/018 and no invented state outside declared intervals.
- Explicit scene continuity can override timeline defaults.
- Concrete approvals can persist presentation role and editorial purpose into registry state.
- Reader presentation can be regenerated from live registry state.
- `generate_illustrated.py` renders role-specific figure classes while preserving current default behavior.
- No canon prose, Showcase state, live art choice, or global production-hold state changes merely from building these derived files.
