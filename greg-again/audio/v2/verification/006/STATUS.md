# Audio Score v2 Chapter 006 — Verification Status

Status: **BLOCKED BEFORE ASSEMBLY / NOT PUBLISHED**

## Verified from repository authority

- Chapter: `006` — **The First Customer**
- Spoken source: `r2/assets/audio-score/ch006.md`
- Audio Score blob SHA: `660801faef0a727a50c73c2b4768e12b71780618`
- Clean source recorded in score header: `r2/assets/written/ch006.md`
- Recorded clean-source SHA: `2fcf88a0688365a4a1a06643d383cdc7ecd7267a`
- Voice: `deep`
- Effective take count: **11**
- Take order: 01 → 11
- Score body coverage is continuous from `Vale counted the money twice.` through `Apparently...`
- No intentional overlap or duplicated seam text in the locked source ranges
- Provider-facing pronunciation authority applied: `Vale` → `Vayle`; `mana` / `Mana` → `ma-na` / `Ma-na`
- Dialogue ownership, eight-copper refund, shop/process terms, and chapter-ending ellipsis remain preserved in the locked source ranges
- Audio Score source itself was not repaired or rewritten

## Provider state

All 11 intended takes were submitted to the `deep` renderer. Provider context IDs and returned AI Doc Maker audio references are recorded in `greg-again/audio/v2/production/006/STATUS.md`.

The available voice action does not expose provider completion polling or a binary-download action. The runtime also cannot resolve `www.aidocmaker.com`, so the returned provider audio references could not be transferred into durable MP3 take files here.

I did **not** audition the generated takes and do not claim subjective cadence/pronunciation QA.

## Completion gates not yet satisfied

- provider audio binaries durably captured: **NO**
- individual take playability verified: **NO**
- final chapter MP3 assembled: **NO**
- chapter-tail settling silence verified: **NO**
- final listener-facing MP3 playable: **NO**
- `greg-again/audio/v2/manifest.json` updated: **NO**
- public `greg-again/audio/manifest.json` switched to `assets/v2/chapter-006.mp3`: **NO**
- public route verified: **NO**

Current public manifest therefore remains on legacy Chapter 006 audio at `assets/chapter-006.mp3`.

## Recovery instruction

Recover the existing 11 provider artifacts first. Do not regenerate successful synthesis merely to solve transfer plumbing. After binaries are captured, assemble Takes 01–11 exactly once in order, preserve natural internal seams, add/verify the established roughly two-second final chapter tail, audition and repair only concrete local failures, then reconcile the newest v2/public manifests and switch only Chapter 006 to `assets/v2/chapter-006.mp3`.
