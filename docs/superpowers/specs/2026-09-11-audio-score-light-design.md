# R2 Audio Score Light Design

Date: 2026-09-11
Status: APPROVED DIRECTION
Scope: Greg, Again Chapters 001-030

## Goal

Create a second, lighter audio-performance layer that preserves the original written prose and uses only small speech-generation edits where they materially improve the `deep` voice rendering.

This is not a second prose rendition and is not a replacement for the existing heavy Audio Score experiment.

## Authority

- Story/written authority remains `r2/assets/written/chNNN.md`.
- Existing heavy Audio Score remains preserved under `r2/assets/audio-score/` as Score 1 / experimental evidence.
- Audio Score Light starts fresh from the written chapter, never from Score 1.
- Audio Score Light is derived voice-input only and must not update canonical written prose.

## Editing doctrine

Default: preserve the written text.

Allowed interventions are small speech-generation techniques:

- punctuation changes that improve spoken cadence
- paragraph or line-break changes that change delivery without changing meaning
- occasional statement -> question -> statement shaping
- rare short restatement when it creates useful processing time or makes a thought audibly legible
- small self-correction or thought turn when already implied by the prose
- sentence split/join where the renderer handles the spoken rhythm better
- small provider-facing pronunciation substitutions
- very small wording edits when needed for spoken clarity

Do not broadly rewrite paragraphs, add new characterization, intensify drama, manufacture Greg voice, add facts, steal another character's reasoning, or treat repetition as a default performance trick.

Invented repetition is allowed only when it clearly adds audible value. If it can plausibly sound like a duplicate/stutter/rendering error, do not use it.

## Change budget

- Expected textual difference for a normal chapter: roughly 2-8%.
- 15% word-level textual change is a hard ceiling, not a target.
- Punctuation, whitespace, lineation, and paragraph boundaries do not count toward the word-level budget.
- Zero textual changes are valid if the written prose already renders well.
- A chapter exceeding 15% requires explicit author approval and should normally be treated as evidence that the prose itself needs separate editorial work rather than a Light Score.

Validation should report word-level change percentage and fail the normal production gate above 15%.

## Files

Light score source:

`r2/assets/audio-score-light/chNNN.md`

The Chapters 001-030 baseline is intentionally byte-for-byte identical to the written source. Provenance is stored separately in:

`r2/assets/audio-score-light/SOURCES.json`

That manifest records the clean written source path and source blob SHA for every Light chapter. Once a chapter receives a real speech-generation edit, its Light file becomes a visible derived diff from that exact written baseline while the provenance manifest continues to anchor the source identity.

Light audio asset:

`greg-again/audio/assets/light/chapter-NNN.mp3`

Light completion registry:

`greg-again/audio/light/manifest.json`

Light production / take / verification evidence should use parallel `greg-again/audio/light/...` paths rather than overwriting Score 1 v2 evidence.

## Production

Use the proven short-take capture factory:

1. Light Score source is the exact intended spoken source.
2. Split at natural preview-safe boundaries, normally <=500 provider characters.
3. Use `deep`.
4. Use identical `transcript` and `preview_transcript` for each request except documented provider-facing pronunciation substitutions.
5. Capture durable playable preview artifacts.
6. Download and `ffprobe` every chunk.
7. Stitch deterministically in order.
8. Add the established ~2 second settling tail after the final spoken word.
9. Verify final MP3, hashes, duration, source identity, and complete ordered coverage.

Text scoring is cheap and may run ahead of synthesis. Audio production is the expensive bottleneck and may proceed independently chapter-by-chapter.

## Public promotion

Do not reset the existing public audio frontier.

Each chapter may independently move through generations. Existing Score 1 or legacy audio remains public until that chapter's Light render is fully assembled and verified.

Only after Light verification:

- add/update the Light manifest entry
- preserve all legacy and Score 1 assets/evidence
- reconcile newest public `greg-again/audio/manifest.json`
- switch only that chapter's `audio_src` to `assets/light/chapter-NNN.mp3`
- update generation/finish metadata without changing stable chapter identity
- verify the public route

Mixed generations across Chapters 001-030 are valid during migration.

## Batch strategy for Chapters 001-030

1. Generate/validate Light Score text for 001-030 from exact written authority.
2. Keep text production ahead of audio production when possible.
3. Run audio synthesis in bounded parallel lanes using current claim/ownership rules adapted to Light paths.
4. Promote each finished Light chapter independently.
5. Never regenerate an already durable good take solely because another chapter or shared manifest moved.
6. Reconcile shared manifests against newest authority before every publication write.

## Success criteria

A Light chapter succeeds when:

- source is the current written chapter, not Score 1
- story meaning and dialogue ownership are unchanged
- word-level textual change is <=15%
- intervention is clearly speech-generation oriented rather than prose rewriting
- all intended source is spoken exactly once
- durable audio artifacts exist and verify
- final MP3 includes listener-safe settling tail
- Light manifest records the result
- public route switches only after full verification

The artistic success criterion is simpler: it should sound like the original R2 prose read well, with a few useful voice-engine nudges that disappear into the listening experience.
