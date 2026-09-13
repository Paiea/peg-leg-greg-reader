# 3L SPEAKER TAGGING AUTHORITY

Status: active production rule.

This file refines `../VOICE_PERFORMANCE_AUTHORITY.md` without changing canon prose authority.

## Goal

3L has many remembered speakers but only two recurring audio identities.

The production system must know **who is speaking semantically** while still routing almost the entire remembered chronicle through Greg's voice.

## Voice identities

### GREG VOICE

Routes:

- all narration
- Greg's spoken dialogue
- young Greg
- older Greg
- all remembered human dialogue
- all remembered non-Ithar dialogue unless a future authority explicitly adds a new recurring vocal identity

Examples of semantic remembered speakers that still map to GREG VOICE:

- MOTHER
- FATHER
- SISTER
- NESSA
- DERA
- HALDEN
- BREN
- MIRA
- GUILD CLERK
- EXAMINER

The semantic speaker label is retained for editorial clarity even though the rendered voice remains Greg.

### DRAGON VOICE

Routes only:

- ITHAR's actual spoken dialogue

Narration describing Ithar remains GREG VOICE.

## Derived artifact format

Canon stays clean in `3l/manuscript/record-XXX.md`.

Tagged production material belongs in `3l/performance/` and is not reader-facing.

Preferred block form:

```text
@voice GREG
@speaker NARRATOR_GREG

<prose>

@voice GREG
@speaker NESSA

<remembered dialogue>

@voice DRAGON
@speaker ITHAR

<dragon dialogue>
```

Tags are production metadata and must never render on the public reading surface.

## Hide rule

Reader pages always load canon manuscript files, never tagged performance files.

If a future debug/player surface can display speaker metadata, the default is hidden. A developer/editor toggle may reveal tags.

## Default inference

For 3L audio production:

- Untagged narration defaults to `GREG / NARRATOR_GREG`.
- A remembered speaker may receive a semantic speaker tag but still routes to `GREG`.
- Only explicit `speaker ITHAR` routes to `DRAGON`.

This means a long remembered stretch can remain one Greg performance even while the editorial layer tracks which remembered character owns each quoted line.

## Present-frame re-entry

When Ithar interrupts a remembered-life chapter, the voice change itself should act as the primary temporal signal.

Do not require a sound effect or a spoken "back in the cave" marker unless prose clarity independently requires one.

The desired listener experience is:

**Greg has been telling the life for minutes. Ithar speaks. The listener instantly knows the present has returned.**

## Performance generation rule

When deriving a performance script from canon:

1. Preserve exact canon wording and order.
2. Segment at natural paragraph/speaker boundaries.
3. Assign the actual semantic speaker.
4. Map every speaker except Ithar to GREG VOICE.
5. Map Ithar to DRAGON VOICE.
6. Allow long Greg stretches without unnecessary technical voice breaks.
7. Allow long Ithar turns to remain one semantic block even if TTS later chunks them technically.
8. Never rewrite prose solely to simplify tagging.

## Canon vs production

Canon prose answers: **what is the story?**

Speaker tags answer: **who owns this spoken block?**

Voice profile answers: **which audio identity performs it?**

Audio generation settings answer: **how is that identity synthesized today?**

Keep these layers separate.