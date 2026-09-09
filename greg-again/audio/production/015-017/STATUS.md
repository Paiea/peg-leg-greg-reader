# Greg, Again audio batch 015-017 — WIP checkpoint

Claim branch: `audio/greg-again-batch-015-017`

Owned chapters:

- 015 — public route title **The Friend**; written source title **The Morning Barge**
- 016 — public route title **The Investor**; written source title **Three Names**
- 017 — public route title **The Extra Hand**; written source title **The Wrong Rope**

Authority:

- `AGENTS.md`
- `r2/PIPELINE.md`
- `r2/AUDIO_PRODUCTION.md`
- `r2/assets/written/ch015.md`
- `r2/assets/written/ch016.md`
- `r2/assets/written/ch017.md`
- `r2/data/chapter-registry.json`

## Production state

The range was claimed before synthesis after a concurrent worker won the attempted `012-014` claim. Do not release or overlap `015-017` while this branch remains live.

All chapter surfaces were split into deterministic ordered production seams and submitted to the connected AI voice provider using voice `deep`.

Queued provider contexts are recorded in:

- `production/015-017/ch015.urls` — 6 contexts
- `production/015-017/ch016.urls` — 10 contexts
- `production/015-017/ch017.urls` — 11 contexts

The third field in those files is a provider **player URL**, not a raw MP3 artifact URL. Do not concatenate or publish those URLs as audio bytes.

Audio-finish maps are recorded in:

- `scripts/015-the-morning-barge.md`
- `scripts/016-three-names.md`
- `scripts/017-the-wrong-rope.md`

## Current blocker

The connected voice action accepted synthesis but returned queued player contexts rather than the raw public `mcp-preview/*.mp3` artifact URLs used by completed Chapter 11 production.

The provider web client's authenticated `user_fetch_document` resolver was identified and tested from GitHub Actions. Calls from GitHub return HTTP 500 for these contexts because the provider-side identity/session used by the connected voice action is not available to GitHub. Do not bypass that access boundary.

Therefore this batch is **produced/queued but not yet verified or published**. `greg-again/audio/manifest.json` must not be updated until actual raw MP3 artifacts are available and verified.

## NEXT_TASK

Resume this existing claim. Do **not** auto-claim another range.

1. Read current `main` first and preserve any newer audio merges.
2. Resolve/export the raw MP3 artifact for every recorded provider context using an authorized provider surface.
3. Create durable `greg-again/audio/takes/015.json`, `016.json`, and `017.json` with exact ordered transcript, provider context ID, raw artifact URL, and first/last anchors. If any provider output is missing/bad, repair only that take.
4. Stitch each chapter in exact take order to `greg-again/audio/assets/chapter-015.mp3`, `chapter-016.mp3`, and `chapter-017.mp3`.
5. Verify exact source coverage/order, seam continuity, playability, route title, and duration under `r2/AUDIO_PRODUCTION.md`.
6. Reconcile `greg-again/audio/manifest.json` against current `main`, append only verified 015-017 entries, run repository checks, publish via PR/merge, verify `main`, then leave the next handshake.

Do not regenerate the entire chapters merely because export is blocked. The queued contexts and deterministic seams are durable work and should be reused if their raw artifacts can be exported.