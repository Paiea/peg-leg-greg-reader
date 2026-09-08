# Greg, Again — Audio-Native Proving Run Design

Date: 2026-09-08
Status: DESIGN FOR REVIEW
Branch: `experiment/plg-r2-opening`

## Purpose

Build one real, repeatable audio-native proving run for **Greg, Again**, using the current experimental Chapter 1 (`state/experiments/plg-r2/prose/001-the-boy.md`) as source evidence rather than as immutable spoken prose.

The experiment answers one question:

> Can Greg, Again become genuinely good audio by treating the heard performance as the primary audience artifact, rather than converting a finished novel into narration?

If the answer is no, the story architecture remains useful and the run may return to conventional prose rendering.

## Product principle

This is not generic TTS and not an audiobook conversion pipeline.

```text
STORY STATE
-> REHEARSAL / PERFORMANCE
-> AUDIO SCORE
-> EXPRESSIVE AUDIO PERFORMANCE
-> LISTEN-BACK
-> DIAGNOSIS
-> REVISE THE CHEAPEST CORRECT LAYER
-> RERENDER
```

The heard result is the quality authority for this experiment.

The hidden score may look unlike polished prose if that makes the spoken result better.

## Quality gate zero

Do not count a render as successful merely because speech was generated.

The renderer must be in the quality class of the expressive ChatGPT playback experience the creator already considers good.

A flat or generic synthetic voice is a failed render, not a fallback success.

Renderer states:

- `qualified`
- `experimental`
- `failed_quality_gate`
- `unrendered`

There is no `good_enough_tts` state.

## Renderer strategy

Use an adapter boundary so the story/audio system does not depend on one transport.

### Preferred adapter

A programmable expressive audio endpoint capable of scene-aware delivery and stable narration quality.

### Bootstrap adapter

If the programmable renderer is materially worse than the known-good ChatGPT playback experience, allow a temporary bootstrap path that:

1. sends one audio-score block at a time through a dedicated narrator chat/session,
2. triggers expressive playback,
3. captures system/loopback audio,
4. saves the resulting block,
5. repeats while preserving narrator/session continuity when useful,
6. assembles approved blocks into the chapter master.

This path is deliberately allowed to be inelegant. Its purpose is to prove the medium at the desired quality bar.

The bootstrap must remain replaceable. Do not make story state, score format, or publication UI depend on browser automation details.

## Narrator model

Start with **one primary traditional narrator who also performs Greg and the other characters**.

Do not begin with a full cast.

The narrator has one stable base identity across the project.

Characters receive behavioral performance profiles rather than mandatory separate biometric voices.

Examples:

### Greg

- dominant POV
- slightly quicker when confident
- can run ahead of himself while building a model
- dry humor should usually be underplayed
- uncertainty should sound different from cockiness

### Hessa

- lower reactivity
- precise
- comfortable with silence
- rarely rushes to reassure Greg

### Jorren

- practical
- immediate
- more physical conversational rhythm
- comfortable interrupting overbuilt theory

Profiles are tendencies, not rigid pitch or accent prescriptions.

## Audio Score

The Audio Score is the primary render input. It contains two distinct layers.

### 1. Spoken layer

Exactly what the audience should hear as language.

This text may differ from the conventional prose source whenever listening quality improves.

It may use:

- repeated names for orientation,
- intentional verbal reinforcement,
- shorter or longer syntax than the written version,
- audible transitions,
- action beats that clarify speaker ownership,
- wording chosen for performance rather than page elegance.

### 2. Hidden performance layer

Metadata/instructions that should not be spoken:

- block ID
- scene ID
- speaker / target
- narrator mode
- entering emotional state
- intention
- physical context
- scene-level pace / energy arc
- pronunciation notes
- critical silence or interruption
- continuity from previous block
- listener-orientation risks

Avoid line-by-line micromanagement such as tagging every sentence `[sad]`, `[angry]`, or exact pause durations unless testing proves a specific instruction repeatedly improves output.

Prefer dramatic truth and scene direction over mechanical acting tags.

## Block model

Render Chapter 1 as stable, replaceable performance blocks.

Block boundaries should follow performance units, not arbitrary character/token counts.

Initial target range: roughly 30 seconds to 2 minutes of final audio per block, adjusted when continuity requires longer or a clean beat supports shorter.

Each block gets a stable ID such as:

```text
ga-001-b001
ga-001-b002
ga-001-b003
```

A failed block can be rerendered without rebuilding the full chapter.

Store generation provenance for each selected block:

- score revision
- renderer adapter
- renderer/model/voice identifier when available
- generation time
- selected take
- listen-back notes

## Speaker clarity

A first-time listener must be able to follow speaker ownership without looking at text.

When ambiguity appears, revise at the cheapest useful layer:

1. performance profile / delivery,
2. action attribution,
3. explicit spoken name,
4. dialogue restructuring,
5. scene restructuring.

Do not mechanically add `X said` to every line.

Three-or-more-person exchanges require stronger re-anchoring than two-person dialogue.

After a long Greg-internal passage, deliberately re-establish external speaker ownership when needed.

## Listen-back and diagnosis

The performance is reviewed as audio, not by staring at the score.

For each block and for the assembled chapter, record findings in these categories:

- naturalness
- acting intelligence
- narrator continuity
- character distinction
- speaker clarity
- first-listen comprehension
- pacing
- joke timing
- emotional turn clarity
- listening fatigue
- desire to continue

When something fails, classify the failure before changing anything:

- renderer
- narrator/voice choice
- performance context
- spoken wording
- scene construction
- underlying story beat
- block seam / assembly

Revise the cheapest correct layer.

Do not solve a boring scene with punctuation tweaks.

## Chapter 1 proving material

Use current experimental Chapter 1, **The Boy**, as source evidence.

It is useful because it contains:

- Greg interior narration,
- short external dialogue,
- humor,
- bodily action,
- fantasy exposition,
- memory uncertainty,
- grief,
- emotional recovery,
- a forward-driving chapter ending.

The written chapter is not locked as the spoken score. Preserve story truth unless audio-specific REHEARSAL or listen-back finds a materially stronger scene execution.

## Product surface

Build the smallest useful public/preview product for the proving run.

Target surface:

```text
/greg-again/audio/
```

Initial page contents:

- `GREG, AGAIN`
- `Audio-Native Proving Run`
- Chapter 1: `The Boy`
- one clear Play/Pause player
- elapsed / duration
- simple chapter status (`experimental` or `approved`)
- optional concise note that this version is being composed for listening rather than converted from a finished audiobook manuscript

Do not build a catalog, account system, full waveform editor, multi-book UI, or elaborate audio-production dashboard.

The player is a product sample, not the Audio OS itself.

## Data / file shape

Exact names may follow existing repository conventions, but preserve these boundaries:

```text
state/experiments/greg-again/audio/
  narrator.md
  pronunciation.json
  chapters/001/
    score.*
    manifest.json
    listen-back.md
    takes/

public/derived audio assets or equivalent publication path
  chapter-001.<audio-format>

greg-again/audio/
  index.html (or existing site-equivalent generated surface)
```

The score/state side owns production evidence.
The publication side owns only approved/selected output and player metadata.

Do not make binary audio story authority.

## Chapter manifest

The Chapter 1 audio manifest should at minimum track:

- story/run identity
- chapter stable ID
- title
- score revision
- block order
- selected take per block
- renderer adapter
- quality status
- assembled asset path when available
- duration when known
- approval state

Navigation must not depend on numeric filename arithmetic.

## Audio assembly

Assemble only selected block takes.

Use deterministic tooling for:

- concatenation
- format normalization
- basic loudness consistency
- silence trimming only when intentional performance timing is preserved

Do not aggressively normalize away dynamic performance.

Keep the selected source blocks so the master is reproducible.

## First success criterion

The first build succeeds only if it produces an actual Chapter 1 audio sample that meets both conditions:

1. the narrator quality is acceptable against the creator's known-good ChatGPT playback reference, and
2. the creator voluntarily wants to keep listening for at least roughly 10 consecutive minutes or the full available sample if shorter.

Technical completion without listening quality is not success.

## Fallback

If expressive audio cannot meet the bar after a bounded proving effort:

- preserve Story State,
- preserve REHEARSAL/PERFORMANCE discoveries,
- preserve Audio Score and listen-back evidence,
- mark the audio renderer experiment unsuccessful,
- return Greg, Again to a prose-first renderer without treating the work as wasted.

## Non-goals for the first build

- full-cast audio drama
- unique permanent voice actor for every character
- soundtrack
- dense Foley
- generic TTS compatibility
- automatic publication of every generated take
- full-series audiobook production
- replacing the original PLG reader
- solving Image OS in the same implementation pass

## Testing

The implementation plan should include tests for:

- score/manifest schema validation
- stable block ordering
- selected-take assembly inputs
- missing/unapproved block rejection
- renderer adapter boundary
- deterministic player metadata generation
- graceful `unrendered` state
- no silent fallback to generic TTS

Manual listen-back remains required for quality approval; automated tests cannot certify performance quality.

## Promotion rule

Chapter 1 remains `experimental` until explicitly approved after listening.

If approved, the Audio OS becomes a supported Greg, Again renderer and the next run may continue audio-first.

If not approved, revise or fall back to prose. Do not force the medium merely because infrastructure exists.
