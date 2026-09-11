# Greg, Again Audio Score v2 — Chapter 004 Verification

Chapter: `004` — **Thirty Days**
Claim branch: `audio/v2-greg-again-ch004-auto`
Audio Score source: `r2/assets/audio-score/ch004.md`
Audio Score blob SHA: `7c2f4b9cdf40fe8035568fa7e503bff4589780fe`
Take map: `greg-again/audio/v2/takes/004/take-map.md`

## Verified before binary capture

- Correct v2 source selected: Audio Score, not clean written rendition.
- Score metadata/header is excluded from narration; score body after `---` is the intended spoken material.
- Take map is deterministic and ordered 01–13.
- Take boundaries are continuous and non-overlapping by source construction, from `A month later...` through `I went to see what it had done...`.
- Dialogue ownership is preserved in the locked transcripts.
- Contract quantities / prices / timing are preserved, including five silver plus salvage, three-silver bathhouse addition, `Two-fifty.`, four copper, nine days, and Vale due in two days.
- Provider-facing substitutions follow `r2/AUDIO_PRONUNCIATION.md` and do not alter score authority: `mana` → `ma-na`, `sparring` → `spar-ring`, `Vale` → `Vayle`.
- No chapter-local Audio Score repair was made.
- All 13 takes were submitted once with voice `deep`; their provider context IDs and artifact URLs are preserved in `greg-again/audio/v2/production/004/STATUS.md`.

## Not yet verifiable in this worker

The available voice action returns a queued provider context ID and artifact URL but exposes no status/retrieval action for the produced binary. The working container also cannot resolve the provider host directly. Therefore this worker cannot honestly verify:

- whether each queued synthesis job has completed
- actual take audio content / cadence
- pronunciation by listening
- take binary integrity
- seam quality
- final chapter assembly
- final 2-second settling tail
- final MP3 playability / duration
- v2 listener-facing asset path
- v2 manifest completion
- public manifest switch / public route

## Publication gate

**NOT PUBLISHED.** Do not update `greg-again/audio/v2/manifest.json` or reroute `greg-again/audio/manifest.json` until the existing provider artifacts have been recovered, assembled, and verified.

Do not regenerate these takes merely to bypass the artifact-transfer problem. Recover the submitted artifacts by their recorded provider context IDs / URLs first.
