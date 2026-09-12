# Audio Score Light Rolling Pool

Campaign: Chapters 001-030
Generation: `audio-score-light`
Voice: `deep`
Max simultaneous synthesis lanes: **5**

## Eligibility

A chapter becomes eligible when:

- `r2/assets/audio-score-light/chNNN.md` exists
- `python scripts/audio_score_light_validate.py NNN` passes
- it is not already Light-published
- it is not actively owned by another Light lane

## Claim rule

Claim the earliest eligible free chapter.

One lane owns one chapter. Do not reserve future siblings merely because a worker expects to continue.

When a lane fully verifies and publishes its chapter, refresh current authority and claim the next earliest eligible free chapter.

## Campaign state

Text frontier: not yet materialized
Light audio published: none

Do not infer Light completion from legacy or v2 / Score 1 publication.
