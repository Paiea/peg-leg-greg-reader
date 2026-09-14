# Chapter 44 Audio Status

## Current state

- Claim: `audio/greg-again-ch044-auto`
- Draft PR: #283
- Chapter: 44 — The Swordsman
- Source blob: `34581028ddc7929c8bfdcb5c5c541daffd18fb73`
- Voice: `deep`
- Takes synthesized: 27/27
- Provider jobs outstanding: 0
- Provider-generated takes lacking repository binary capture: 27
- Final chapter assembly: pending
- Manifest/catalog publication: not started

## Recovery rule

Do not regenerate these takes merely because this worker could not ingest provider MP3 bytes into the assembly runtime. `take-map.json` preserves the exact transcript, provider context ID, direct preview MP3 URL, and provider audio URL for every take.

## Finisher checklist

1. Recover the existing provider MP3 for Takes 001–027 from the preserved references.
2. Save durable take binaries under the established Chapter 44 production path.
3. Verify each binary is playable and record bytes, duration, and SHA-256.
4. Verify exact transcript coverage and numeric order with no duplicated or omitted seam text.
5. Stitch Takes 001–027 exactly once in order.
6. Preserve the final take's authoritative `...` landing.
7. Add about 2.0 seconds of silence to the final assembled chapter only.
8. Verify final duration, bytes, SHA-256, playability, seam continuity, and listener tail.
9. Refresh current `main` immediately before shared-file edits.
10. Preserve every newer valid manifest/catalog entry and add only `ga-044`.
11. Publish `greg-again/audio/assets/chapter-044.mp3` and verification evidence.
12. Merge only after fresh branch/main and publication verification.

## Restart prompt

Continue Greg, Again Chapter 44 audio finishing from current GitHub authority. Resume `audio/greg-again-ch044-auto` / PR #283. Recover the 27 already-generated provider artifacts from `greg-again/audio/production/044/take-map.json`; do not regenerate acceptable takes. Capture, verify, stitch in order, add the two-second chapter tail, reconcile newest shared publication state, publish ga-044, verify, merge, and leave the next handshake. Preserve newer authority and do not overlap another worker.