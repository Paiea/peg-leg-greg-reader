# R2 Audio Score Light / Score 2

Status: **ACTIVE EXPERIMENTAL LIGHT PERFORMANCE LAYER**

Audio Score Light is the restrained successor experiment to the heavier `r2/AUDIO_SCORE.md` treatment.

It is a derived voice-input layer for Listen. It does not replace the written rendition and it does not replace or delete Score 1.

## Authority

For each chapter, start from the exact current written prose:

`r2/assets/written/chNNN.md`

Never start from `r2/assets/audio-score/chNNN.md`.

The written prose remains the readable/story rendering. Score 1 remains preserved as experimental evidence. Score 2 exists only to make the written prose speak a little better through the current voice renderer.

## Core goal

> **Preserve the prose. Nudge the voice.**

The original written chapter already carries Greg's POV, cadence, humor, processing, and sentence logic. Do not recreate those things from scratch.

Use the smallest intervention that gives the renderer useful spoken nuance.

## Normal edit scale

Expected wording difference for a normal chapter is roughly **2-8% or less**.

**15% word-level change is a hard ceiling, not a target.**

Punctuation, whitespace, paragraph boundaries, and lineation do not count toward that word-level budget.

Zero wording changes are valid when the prose already speaks well.

A chapter approaching 15% should trigger suspicion that the score is rewriting instead of lightly performing.

## Preferred tools

Prefer these in roughly this order:

1. punctuation changes that alter spoken cadence
2. paragraph / line-break changes that give a thought room
3. sentence split or join where the renderer handles the rhythm better
4. occasional statement -> question -> statement movement
5. a tiny self-correction already implied by the prose
6. a short restatement when it clearly buys cognition, orientation, humor, or absorption
7. a very small wording adjustment for spoken clarity
8. provider-facing pronunciation substitutions during synthesis

The best Light edit is often invisible on listen-back.

## Repetition

Do not use repeated words or phrases as a house technique.

Invented repetition is allowed only when the second utterance clearly changes the thought or produces obvious audible value.

If a repeated word could plausibly sound like:

- a stutter
- a duplicated take
- a generation glitch
- accidental repeated text

then do not add it.

Existing repetition in the written prose is not automatically a problem. Judge it as written.

## Statement / question flow

Question contours can help the renderer expose Greg thinking in real time, but use them sparingly.

A useful pattern may turn one already-implied thought into:

`statement -> question -> landing`

without changing what Greg knows or inventing extra drama.

Do not convert every realization into a question-answer exchange.

## Protected material

Preserve:

- facts and causal relationships
- who acts
- who knows what
- dialogue ownership
- binding wording, prices, terms, deadlines, quantities, and locations
- Greg's uncertainty and evidence ceiling
- jokes whose wording depends on setup/payoff
- another character's expertise and reasoning

Do not manufacture a stronger Greg voice. The written prose already owns the voice.

## Anti-patterns

Avoid:

- broad paragraph rewrites
- adding drama because audio can sound more dramatic
- fragmenting every sentence
- repeated `No.`, `Wait.`, `Again.`, or similar tics
- invented echoes that sound like errors
- explanatory filler
- extra cognition that the written prose already communicates cleanly
- turning every paragraph into a performance moment
- using the 15% ceiling as a quota

## File policy

Light score chapters live in:

`r2/assets/audio-score-light/chNNN.md`

Each file records its written source path and source blob SHA.

Validate with:

`python scripts/audio_score_light_validate.py NNN`

The normal production gate fails above 15% word-level change.

## Production

For synthesis and publication rules, read:

`r2/AUDIO_SCORE_LIGHT_PRODUCTION.md`

Use the established `deep` narrator and proven preview-safe short-take factory. Keep pronunciation substitutions provider-facing unless the Light source itself genuinely needs a textual repair.
