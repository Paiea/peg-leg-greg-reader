# Chapter 001 Audio Score v2 Verification

Status: **VERIFIED_UNLISTENED**

Mechanical verification completed before publication:

- authoritative source: `r2/assets/audio-score/ch001.md`
- source blob: `155de484c67836f615e2704896aa37984002d690`
- 33 ordered preview-safe takes cover the Audio Score in source order
- `transcript` and `preview_transcript` were identical for each provider request
- provider-facing text differs from score spelling only for documented `mana -> ma-na` pronunciation aliases
- all 33 Google Storage preview MP3 artifacts were downloaded durably
- every take passed minimum-byte gating and `ffprobe`
- per-take bytes, durations, SHA-256 hashes, and preview URLs are recorded in `greg-again/audio/v2/production/001/capture-metadata.tsv`
- deterministic take boundaries and provider artifacts are recorded in `greg-again/audio/v2/takes/001/preview-capture-map.json`
- final chapter was assembled in take order with ffmpeg, with no music, SFX, crossfades, or decorative processing
- approximately 2 seconds of settling silence were added only at final chapter assembly
- final MP3 passed `ffprobe`
- final asset: `greg-again/audio/assets/v2/chapter-001.mp3`
- final duration: 886.896 seconds
- final size: 7,918,557 bytes
- final SHA-256: `4148946c20eb931867547ff1e559a6c90733fcd4fb129d501cd5698bea0624c9`
- Audio Score source was not edited

Subjective human listen-back has not been claimed or simulated.
