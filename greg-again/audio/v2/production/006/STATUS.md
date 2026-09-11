# Audio Score v2 Chapter 006 — Production Status

Status: **PREVIEW-SAFE CAPTURE COMPLETE / MECHANICALLY VERIFIED**

Chapter: `006` — **The First Customer**
Claim branch: `audio/v2-greg-again-ch006-auto`
Audio Score source: `r2/assets/audio-score/ch006.md`
Audio Score blob SHA: `660801faef0a727a50c73c2b4768e12b71780618`
Recorded clean-source SHA: `2fcf88a0688365a4a1a06643d383cdc7ecd7267a`
Voice: `deep`
Score repair: **none**

Provider-facing substitutions:

- `Vale` → `Vayle`
- `mana` / `Mana` → `ma-na` / `Ma-na`

## Final capture transaction

The listener-facing v2 artifact uses the proven preview-safe capture factory:

**Audio Score → natural chunks ≤500 chars → `deep` → identical `transcript` + `preview_transcript` → Google Storage preview MP3 → GitHub Actions capture / ffprobe → ffmpeg stitch → 2-second settling tail.**

- preview-safe chunks: **30**
- exact capture map: `greg-again/audio/v2/production/006/capture.json`
- durable chunk audio: `greg-again/audio/v2/takes/006/audio/chunk-01.mp3` through `chunk-30.mp3`
- final MP3: `greg-again/audio/assets/v2/chapter-006.mp3`
- duration: **649.632 seconds**
- final SHA-256: `e627ac90138948b225c2d45d7537cd92b4323819bd07262c08c91737b42d9f83`
- settling tail: **2 seconds**

GitHub Actions mechanically verified that the provider-facing capture transcript covers the Audio Score body exactly once after only the approved pronunciation substitutions, that all 30 chunk MP3s download and parse with `ffprobe`, and that the assembled final MP3 parses successfully.

## Historical full-render transaction

Before the preview-safe artifact boundary was identified, 11 larger full-audio requests were submitted. They are preserved as historical recovery evidence and are **not** the source of the final listener-facing MP3.

| Historical take | Provider context ID |
| --- | --- |
| 01 | `e8f9fd1163f842ee973823912d7f6711` |
| 02 | `cccc8166262e4dcf99af24536eddf854` |
| 03 | `95a46c4f655a4fe7a025fc060dfbb213` |
| 04 | `913ac52ad0f941929a3abeb6833cb4ca` |
| 05 | `1eae1356d22b48d8a47f9d39957bddd1` |
| 06 | `46bb53f7b2e046e4af20db8c635701aa` |
| 07 | `1aa8855be5c5430d81f21df9de708dfc` |
| 08 | `a1ac58344a554a30936bbacac1f12d03` |
| 09 | `a328ac1091724177abf876a8e7344ef1` |
| 10 | `7e3e67e3a0a94731bd3c16237f53af65` |
| 11 | `6a91a6ac03e541ffb13701e32f443769` |

Do not regenerate or delete those historical provider jobs merely to normalize production history.

## Publication state

The claim branch has reconciled the newest Audio Score authority into both manifests while preserving sibling v2 Chapter 009:

- `greg-again/audio/v2/manifest.json` records Chapter 006 as `verified_unlistened`
- `greg-again/audio/manifest.json` routes Chapter 006 to `assets/v2/chapter-006.mp3`

Subjective human listen-back has **not** been performed and is intentionally not claimed here.
