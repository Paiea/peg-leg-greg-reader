# Chapter 007 Audio Score v2 production status

Chapter: **007 — The Extra Guard**
Claim branch: `audio/v2-greg-again-ch007-auto`
Authority base: `audio-score/chapters-001-010` because PR #287 remained open/unmerged at claim time.
Audio Score source: `r2/assets/audio-score/ch007.md`
Audio Score blob SHA: `d179b9621a0903c286171b707264b6256600b99f`
Narrator: `deep`

## Production completed

- Claim branch created durably before synthesis.
- Score body split into 10 natural provider-safe takes without rewriting the score.
- All 10 takes submitted to the established voice provider.
- Provider context IDs and recovery URLs captured in `greg-again/audio/v2/takes/007/take-map.md`.
- One provider-facing pronunciation alias used: written `Mana` -> `Ma-na` in Take 07, per pronunciation authority.
- No Audio Score source repair was made.

## Hard boundary

The available voice action reports submissions as `queued` and returns provider context/artifact URLs, but exposes no status/download/capture action for the generated binary. Therefore these submissions have not yet crossed the durable audio-binary boundary and cannot honestly be assembled, auditioned, or certified playable from this worker.

Do **not** regenerate successful provider work to solve this plumbing boundary. Recover/capture the existing ten provider artifacts by their recorded identities first.

## Publication state

Final MP3: **NOT ASSEMBLED**
Expected path when complete: `greg-again/audio/assets/v2/chapter-007.mp3`
V2 manifest: **NOT UPDATED**
Public manifest: **NOT UPDATED**
Public route: **UNCHANGED / v1 preserved**

## Verification remaining

After artifact capture: verify each take completed and is playable; audition pronunciation/cadence; repair only rejected local takes; assemble takes 01–10 in order; add ~2 seconds settling tail; verify score coverage once/no seam duplication, dialogue ownership, quantities/names, final landing and MP3 playability; then reconcile newest GitHub authority and update v2 + public manifests for Chapter 007 only.

## Reusable lesson

No new cross-chapter Audio Score doctrine is justified from this run. Existing provider-facing `Mana` -> `Ma-na` authority applied cleanly. Subjective cadence claims are intentionally deferred because this worker could not audition the provider output.
