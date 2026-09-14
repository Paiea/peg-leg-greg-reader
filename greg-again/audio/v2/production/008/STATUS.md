# Audio Score v2 — Chapter 008 Production Status

Chapter: 008 — Road Work
Claim branch: `audio/v2-greg-again-ch008-auto`
Source: `r2/assets/audio-score/ch008.md`
Audio Score blob SHA: `70fb72370291aa2a47b76d383cae9434254305e8`
Voice: `deep`

## Current state

- 20 preview-safe chunks captured with identical `transcript` + `preview_transcript`
- all 20 returned durable Google Storage preview MP3 URLs
- all 20 downloaded and passed `ffprobe`
- exact Audio Score body reconstructs from the 20 source chunks once and in order
- provider-facing pronunciation aliases only on chunks 10 and 17 (`mana` -> `ma-na`)
- final listener-facing asset exists at `greg-again/audio/assets/v2/chapter-008.mp3`
- final duration: 535.800 seconds
- approximately 2 seconds of settling tail appended at assembly
- v2 manifest reconciled from newest Audio Score authority
- public manifest Chapter 008 switched to `assets/v2/chapter-008.mp3`

## QA boundary

Objective artifact/source/assembly verification is complete. No claim is made that a human subjective listen-back occurred in this worker. Future listener feedback should repair only the smallest failed chunk or seam if needed.

## Reusable production lesson

Audio Score -> natural preview-safe chunks (about 500 chars max) -> `deep` -> identical `transcript` and `preview_transcript` -> capture returned Google Storage `preview_url` -> Actions download/ffprobe -> ffmpeg stitch -> settling tail -> verify -> v2 asset -> reconcile v2 + public manifests.
