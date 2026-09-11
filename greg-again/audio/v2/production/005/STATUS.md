# Greg, Again Audio Score v2 — Chapter 005 Status

Status: **RECOVERY PATH IDENTIFIED / PREVIEW-SAFE REGENERATION REQUIRED**

Claim: `audio/v2-greg-again-ch005-auto`
Chapter: **005 — The Partner**
Audio Score: `r2/assets/audio-score/ch005.md`
Audio Score blob SHA: `843bee0da9f81deb4fa4e8dff3d6a50b77591332`
Clean source recorded by score: `r2/assets/written/ch005.md` @ `a1b653c75e962f23e09454d8792f5ec17e6d32be`
Voice: `deep`

## Root cause

The first v2 Chapter 005 pass used 12 large cadence-shaped takes and submitted them only as full voice jobs. That produced `context_id` + AI Doc Maker `audio_url`, but no direct binary URL on the current tool surface.

Historical successful Greg, Again production used a different capture contract: provider-safe takes were kept within the voice tool's preview limit, and each call sent the same locked take text as both `transcript` and `preview_transcript`. That returned a direct `preview_url` on public Google Storage. A temporary GitHub Actions capture workflow then downloaded each preview MP3 with `curl`, verified it with `ffprobe`, stitched the ordered takes, added the approximately 2-second chapter tail, and committed the durable binaries and final chapter asset.

This historical bridge is visible in the Chapter 29 and Chapter 38 production commits.

## Minimal reproduction

The recovery contract was re-tested on Chapter 005 Take 01 text with voice `deep` and succeeded immediately:

- context_id: `1b4289a69bf044789953cb860be5eda4`
- preview_url: `https://storage.googleapis.com/adm--audio-playback--7d--public/mcp-preview/f211f15e-ee1a-47d2-81ec-9e0fce81e4c2.mp3`
- provider status: `ready`

Therefore artifact transfer itself is not generally broken. The failed first pass used the wrong take size / request shape for this tool surface.

## Existing provider work

The original 12 full-audio submissions remain preserved as historical provider evidence. Do not discard their IDs. However, because they expose no direct capturable binary on the available interface, they are not sufficient to complete this chapter here.

Regenerating the chapter into preview-safe takes is justified because this is a renderer/tool-surface compatibility failure, not a subjective re-roll of acceptable audio.

## Exact next production action

1. Re-split the exact Audio Score body into natural preview-safe takes, each at or below the provider preview limit (roughly <=500 characters), preserving exact order and score wording except approved provider-only pronunciation aliases.
2. For each take call `deep` with identical `transcript` and `preview_transcript`.
3. Record `context_id` + direct `preview_url` immediately.
4. Add a temporary Chapter 005 GitHub Actions capture workflow modeled on the proven Chapter 29/38 bridge.
5. Workflow downloads each preview MP3, verifies duration/readability, reconstructs exact Audio Score coverage, stitches takes in order, appends ~2 seconds of tail silence, and writes `greg-again/audio/assets/v2/chapter-005.mp3`.
6. Audition/repair only local failed passages if needed, then reconcile the v2 and public manifests.

## Score repair

None yet. The Audio Score remains untouched.

## Reusable production lesson

On the current AI voice tool surface, a take must be preview-safe and explicitly supplied as `preview_transcript` if the worker needs a direct downloadable MP3 for GitHub-side capture. `audio_url` alone points to the AI Doc Maker experience and is not the proven durable capture path.
