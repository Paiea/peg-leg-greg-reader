# Chapter 007 Audio Score v2 production status

Chapter: **007 — The Extra Guard**
Claim branch: `audio/v2-greg-again-ch007-auto`
Authority base: `audio-score/chapters-001-010` because PR #287 remains open/unmerged.
Audio Score source: `r2/assets/audio-score/ch007.md`
Audio Score blob SHA: `d179b9621a0903c286171b707264b6256600b99f`
Narrator: `deep`

## Production complete

- Recovered the proven short-take capture factory used by earlier Greg, Again audio chapters.
- Repartitioned the Audio Score into 31 natural preview-safe chunks.
- Sent identical text as `transcript` and `preview_transcript` with voice `deep`.
- Captured a playable direct Google Storage `preview_url` for every take.
- Applied provider-facing pronunciation substitutions only: written `Vale` -> `Vayle`; written `Mana` -> `Ma-na`.
- GitHub Actions downloaded and `ffprobe`-verified all 31 MP3 chunks.
- ffmpeg stitched Takes 01–31 in deterministic order.
- Added the established approximately two-second settling tail after the final spoken word.
- No Audio Score source repair was made.
- The earlier ten long queued submissions are superseded production evidence only and are not part of the published v2 render.

## Durable result

Final MP3: `greg-again/audio/assets/v2/chapter-007.mp3`
Take map: `greg-again/audio/v2/takes/007/take-map.md`
Verification: `greg-again/audio/v2/verification/007/VERIFY.md`
Duration: `623.448` seconds
Size: `9,975,597` bytes
SHA-256: `de12bffa3ed699816837db6b9e41abaad514368ca94e57ecb2fa16f578f8af8f`

## Publication state

V2 manifest: **UPDATED / Chapter 007 verified**
Public manifest: **UPDATED / Chapter 007 points to `assets/v2/chapter-007.mp3`**
Legacy v1 Chapter 007 MP3: **PRESERVED**
Temporary capture/publication workflow: **REMOVED after successful use**

## Factory lesson

For Audio Score v2, use the proven preview-first capture path by default: Audio Score -> natural preview-safe chunks (~500 chars max) -> `deep` -> identical `transcript` + `preview_transcript` -> durable returned `preview_url` -> GitHub Actions download/ffprobe -> ffmpeg stitch -> ~2-second settling tail -> verify -> v2 asset -> reconcile v2 and public manifests.
