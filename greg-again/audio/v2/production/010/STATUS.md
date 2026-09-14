# Greg, Again Audio Score v2 — Chapter 010 Production

Status: ASSEMBLED / TECHNICALLY VERIFIED

- Chapter: `010 — What Moved`
- Claim branch: `audio/v2-greg-again-ch010-auto`
- Audio Score source: `r2/assets/audio-score/ch010.md`
- Audio Score blob SHA: `bf0e024b5117ad519d24cc2ed3ce629b3afbcf05`
- Clean written source recorded by score: `r2/assets/written/ch010.md` @ `dac4163caf088000ae6a44ba880e604168ec9050`
- Voice: `deep`
- Take count: `25`
- Take map: `greg-again/audio/v2/takes/010/take-map.md`
- Provider-facing substitutions only: `mana` → `ma-na`; `Vale` → `Vayle`
- Audio Score source repair: none
- Final asset: `greg-again/audio/assets/v2/chapter-010.mp3`
- Final duration: `591.480000` seconds
- Final SHA-256: `b0c65a9d96985703d693d05516439ca2a83bf10d9d722e01b7854221d9356474`
- Tail: approximately two seconds added after assembly via `apad=pad_dur=2`

## Artifact boundary

All 25 voice requests returned durable preview MP3 URLs. The exact provider context IDs, preview URLs, order, and provider-facing transcripts are preserved in the take map. GitHub Actions downloaded all 25 MP3s, rejected trivial files, passed `ffprobe` on each take, stitched them in deterministic filename order, added the settling tail, passed `ffprobe` on the final MP3, and recorded hashes plus final duration.

The first two capture attempts failed only in downstream tooling (`ffprobe` absent, then concat-list path resolution). No successful provider synthesis was regenerated. The third capture run succeeded end-to-end.

## Subjective listen-back boundary

This worker did not claim subjective audition. Technical artifact integrity, source/take ordering, provider identity, deterministic stitching, duration, hashes, and tail construction are verified. Any future cadence or pronunciation repair should be driven by an actual human listen-back and should replace only the affected local take(s).

## Reusable production lesson

When the concat list is stored outside the repository workspace, ffmpeg resolves relative file entries relative to the list file. Use absolute `$GITHUB_WORKSPACE` paths (or place the list beside the take files) so downstream assembly does not fail after successful capture.
