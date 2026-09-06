# PLG DIALOGUE VARIANCE CURRENT EDGE

Branch: `editor/voice-compression-pass`

This compact edge marker supplements `state/editorial/DIALOGUE_VARIANCE_PASS_STATE.md` when that larger ledger has not yet been rewritten after a bounded review batch.

## Current sequential coverage

- Chapters **1-440: VARIANCE REVIEWED**
- Current sequential edge: **Chapter 441**
- Latest batch: `state/editorial/dialogue-variance-pass/BATCH_431_440.md`
- Current `main` manuscript authority at latest review: **Chapter 477**
- Next intended bounded batch: **441-450**

## Authority rule

If this file is newer than the edge recorded in `state/editorial/DIALOGUE_VARIANCE_PASS_STATE.md`, use this file and the latest sequential batch artifact to resume. Exact `main` prose and active correction overlays still outrank summaries.

## Restart prompt

`Continue PLG whole-manuscript dialogue + attribution pass from current GitHub authority on editor/voice-compression-pass, using the dialogue variance engine. Treat the newest sequential batch plus state/editorial/dialogue-variance-pass/CURRENT_EDGE.md as the live continuation edge.`