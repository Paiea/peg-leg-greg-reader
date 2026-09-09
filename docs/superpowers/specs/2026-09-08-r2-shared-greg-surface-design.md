# R2 Shared Greg Surface Design

## Status

Approved architecture for R2 / Greg, Again rendering.

This design replaces the experimental mental model of:

```text
written novel -> audio rewrite -> written cleanup
```

with one shared Greg-shaped wording layer feeding two light medium-specific finishes.

## Goal

Keep the written and spoken R2 versions recognizably the same chapter while preserving the useful discoveries of audio-first composition.

The system should make it difficult for audio and written versions to drift into two independently authored books.

## Authority and data flow

```text
STORY STATE / PERFORMANCE
        ↓
GREG EXPERIENCE
        ↓
SHARED GREG SURFACE
      ↙       ↘
AUDIO FINISH   WRITTEN FINISH
      ↓             ↓
VOICE / LISTEN      READ
      ↘             ↙
    FEEDBACK CLASSIFICATION
```

### Story State / Performance

Owns what actually happened, who acted, who knew what, causal ownership, binding language, state changes, and continuity.

### Greg Experience

Owns what Greg perceives, notices, misunderstands, ignores, remembers, associates, and how attention moves through the event.

Greg owns POV continuity, not causality, expertise, or every other character's meaning.

### Shared Greg Surface

The Shared Greg Surface is the default wording layer for both media.

It should already be close to publishable prose and close to speakable audio.

It carries:

- continuous Greg thought-line
- attention gravity
- selective direct speech
- voice breaches
- embodied outside characters
- language-as-action ownership
- fragments when Greg's cognition genuinely fragments
- self-corrections, resets, and repetition when they are genuinely Greg
- material action and consequence

It must not contain provider-specific stage directions, SSML, timing codes, hidden acting notes, or synthetic vocal tics added only to make text sound human.

### Audio Finish

Audio Finish is a light transformation of the Shared Greg Surface.

It may:

- split paragraphs into breath-sized units
- isolate words or phrases when the pause reflects cognition
- add a rare reset, self-correction, or repetition when one-pass listening genuinely needs it
- simplify syntax that is difficult to understand once
- make speaker ownership explicit when the ear would otherwise lose it
- preserve voice breaches and binding language with special care

It may not:

- add new story facts
- transfer another character's agency, expertise, leverage, decision, or meaning to Greg
- invent dialogue merely to make audio lively
- substantially rewrite the chapter when the Shared Greg Surface already works aloud

### Written Finish

Written Finish is also a light transformation of the Shared Greg Surface.

It may:

- recombine excessive breath fragments into paragraphs
- normalize punctuation and visual rhythm
- remove audio-only repetition that reads as performance residue on the page
- improve sentence architecture where reading can hold more complexity
- preserve isolated lines and fragments when they express Greg's cognition rather than audio markup

It may not:

- clean away Greg's spoken-cognitive character merely to look conventionally literary
- add new story facts
- transfer causal or linguistic ownership
- become a transcript-cleanup pass after an independently authored audio rewrite

## Core cleanup rule

> **Clean performance residue. Do not clean away cognition.**

A short line, repeated word, reset, fragment, or interruption stays in written prose when it represents Greg thinking.

It is removed or recomposed only when it exists solely to help vocal delivery.

## Outside language

The existing Greg-dominant rules remain active.

Outside voice earns direct space for:

- falsification
- state transition
- motor interrupt
- irreplaceable character language
- domain authority
- relationship state

Language that creates prices, promises, refusals, threats, deadlines, ownership, consent, wagers, contracts, or other obligations must preserve who said, proposed, accepted, rejected, or committed to what.

Greg may own the linguistic surface. He may not steal another character's thought.

## Feedback routing

Listen-back and page-read feedback must be classified before revision.

### Shared / Greg Experience discovery

If hearing or reading reveals that Greg's attention, interpretation, perception, or causal understanding is wrong, revise Greg Experience and the Shared Greg Surface so both media inherit the correction.

Example:

A cart enters and is more salient than Greg's current training thought. Greg should lose the thought in both media.

### Audio-only discovery

If the issue is breath, pause length, one-pass clarity, pronunciation, audible speaker ownership, or performance timing, revise only Audio Finish.

### Written-only discovery

If the issue is paragraph shape, visual repetition, punctuation, or page rhythm, revise only Written Finish.

## Similarity target

Read and Listen should normally feel almost line-for-line familiar.

A useful heuristic is roughly **90-97% lexical overlap** between the Shared Greg Surface and either finish when the chapter does not contain a medium-specific problem.

This is not a numeric gate or quota. If a scene genuinely needs a larger medium-specific divergence, story clarity wins.

## Production memory

The durable public/publishing surface should expose this architecture in two places:

1. `r2/PIPELINE.md` — human-readable worker contract.
2. `r2/data/rendering-pipeline.json` — small machine-readable routing contract.

`r2/data/project.json` should point to the machine-readable contract.

`r2/README.md` should direct workers to the shared-surface pipeline before publishing or rendering a chapter.

## Non-goals

This change does not:

- rewrite Chapters 1-16
- regenerate existing audio
- force the current written and audio experiments to become byte-identical
- redesign the R2 website
- create a full generalized renderer framework
- impose a dialogue quota, fragment quota, pause quota, or lexical-overlap test

Existing Chapters 1-3 remain experimental evidence. Future chapters should use the shared-surface model by default, and older chapters can be reconciled only when a real revision or listen-back justifies it.
