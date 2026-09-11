# Audio Score v2 Chapter 006 — Verification Status

Status: **VERIFIED_UNLISTENED / READY FOR AUTHORITY PUBLICATION**

## Source and capture verification

- Chapter: `006` — **The First Customer**
- spoken source: `r2/assets/audio-score/ch006.md`
- Audio Score blob SHA: `660801faef0a727a50c73c2b4768e12b71780618`
- clean source recorded in score header: `r2/assets/written/ch006.md`
- recorded clean-source SHA: `2fcf88a0688365a4a1a06643d383cdc7ecd7267a`
- voice: `deep`
- preview-safe chunk count: **30**
- provider-facing substitutions: `Vale` → `Vayle`; `mana` / `Mana` → `ma-na` / `Ma-na`
- Audio Score repair: **none**

The capture workflow compared the concatenated provider-facing chunk transcripts against the complete Audio Score body after applying only the approved provider substitutions. Coverage passed exactly: no missing source material and no duplicated source range.

## Binary verification

All 30 Google Storage preview MP3s were downloaded by GitHub Actions, size-checked, and parsed with `ffprobe` before assembly.

Final listener-facing artifact:

`greg-again/audio/assets/v2/chapter-006.mp3`

- duration: **649.632 seconds**
- SHA-256: `e627ac90138948b225c2d45d7537cd92b4323819bd07262c08c91737b42d9f83`
- final tail: **2 seconds**
- final MP3 `ffprobe`: **PASS**

Supporting evidence:

- `greg-again/audio/v2/verification/006/chunk-probes.tsv`
- `greg-again/audio/v2/verification/006/SHA256SUMS`
- `greg-again/audio/v2/verification/006/final.txt`

## Manifest verification on claim branch

- v2 manifest records Chapter 006 with `status: verified_unlistened`
- v2 manifest preserves sibling Chapter 009
- public manifest preserves stable Chapter 006 identity/title/lens
- public Chapter 006 `audio_src`: `assets/v2/chapter-006.mp3`
- public duration: **649.632**
- public take count: **30**

## Human listen-back boundary

No subjective audition was performed in this worker. I do **not** claim that cadence, pronunciation, seam feel, or performance taste has received human listen-back approval. Mechanical publication verification and subjective listen-back remain separate gates.

Exact remaining publication action: merge PR #293 into the current `audio-score/chapters-001-010` authority after confirming the PR is conflict-free against the latest base, then verify the asset and both manifest routes on that authority.
