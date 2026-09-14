# Chapter 003 Audio Score v2 Production Status

Claim branch: `audio/v2-greg-again-ch003-auto`
Authority base: `audio-score/chapters-001-010`
Audio Score source: `r2/assets/audio-score/ch003.md`
Audio Score blob SHA: `211ed23b1bfc34f3f37144d31f91eec60fff0ab2`
Voice: `deep`
Score repairs: none

## Current production

The original 12 long provider submissions are retained as historical evidence, but they did not expose durable preview artifacts and are **not** the assembled chapter source.

The chapter was resegmented from the same Audio Score into 30 natural preview-safe takes, each no more than about 500 characters. Every take used:

- voice `deep`
- identical `transcript` and `preview_transcript`
- approved provider-facing substitutions only (`mana` -> `ma-na`, `Vale` -> `Vayle`)
- a returned durable Google Storage `preview_url`

Exact transcripts, context IDs, preview URLs, order, and durable capture metadata are recorded in:

`greg-again/audio/v2/takes/003/short-takes.json`

GitHub Actions downloaded all 30 preview MP3s, rejected trivial files, and `ffprobe`-verified every chunk before assembly.

## Assembly

Final asset:

`greg-again/audio/assets/v2/chapter-003.mp3`

Structural verification evidence:

`greg-again/audio/v2/verification/003/assembly.md`

Verified assembly facts:

- 30/30 preview takes captured durably
- deterministic order 01–30
- all chunks pass `ffprobe`
- component duration: `671.04` seconds
- final duration: `673.104` seconds
- approximately 2 seconds of settling silence added after assembly
- final SHA-256: `9d73d75d0122815fbce95e44bf5d1d10ae48cd60835f92023d02022ae9aa04c9`
- final GitHub asset size: `6022557` bytes

## Remaining publication gate

The binary/artifact blocker is resolved and the chapter is assembled. This worker still has not performed a genuine human-audible listen-back, so audible pronunciation/cadence and seam quality are not claimed as subjectively verified.

Do not mark Chapter 003 published in `greg-again/audio/v2/manifest.json` or switch the public manifest until that listen-back gate is satisfied under current authority.

## Reusable production lesson

The durable short-take capture factory has been promoted into `r2/AUDIO_SCORE_PRODUCTION.md` on the current Audio Score authority branch. For Audio Score v2, prefer natural preview-safe chunks, identical `transcript` + `preview_transcript`, durable Google Storage `preview_url` capture, GitHub Actions download/`ffprobe`, deterministic ffmpeg assembly, and the established settling tail.
