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

All chapter surfaces were split into deterministic ordered production seams and submitted to the connected AI voice provider using voice `deep`:

- Chapter 015: 6 submitted takes
- Chapter 016: 10 submitted takes
- Chapter 017: 11 submitted takes
- Total: 27 submitted provider contexts

Original submission records remain in:

- `production/015-017/ch015.urls`
- `production/015-017/ch016.urls`
- `production/015-017/ch017.urls`

The third field in those files is a provider **player URL**, not a raw MP3 artifact URL. Do not concatenate or publish those URLs as audio bytes.

Audio-finish maps remain in:

- `scripts/015-the-morning-barge.md`
- `scripts/016-three-names.md`
- `scripts/017-the-wrong-rope.md`

Durable resumable take maps now also exist at:

- `takes/015.json`
- `takes/016.json`
- `takes/017.json`

Those JSON maps preserve deterministic take number, exact first/last source anchors, provider context ID, provider player URL, voice, and explicit `submitted` status. `artifact_url` is intentionally `null` until the real provider artifact boundary is crossed. The current source boundaries remain the exact spoken authority; do not infer that the player URL is a durable artifact.

## Reconciliation state

On 2026-09-09 UTC, current `main` at `85307283c6e52f5230d9120a55def438af1736cf` was merged into this claim branch through reconciliation PR #205. At that checkpoint the claim branch was behind current `main` by **0** commits. Always fresh-read `main` again before final publication because concurrent workers may move it after this checkpoint.

No Chapter 15-17 manifest entries were added during reconciliation. No listener-facing publication has been claimed.

## Current blocker

The connected voice action accepted synthesis but exposes only creation/player context in this environment. Its available action does not provide an authorized operation for fetching/exporting an already-generated context as raw MP3 bytes.

The provider web client's `user_fetch_document` resolver was independently tested from GitHub Actions by this batch and by the separate `018-020` worker. Calls returned HTTP 500 even for a known-good published Chapter 11 provider context. This confirms the GitHub-side failure is not evidence that the 015-017 synthesis jobs are malformed or stale; the provider-side identity/session used by the connected voice surface is not available to GitHub. Do not bypass that access boundary.

Therefore this batch is **submitted/generated-provider-side as far as the connected creation action reports, but not artifact-captured, verified, or published**. `greg-again/audio/manifest.json` must not be updated until actual raw MP3 artifacts are available and verified.

## NEXT_TASK

Resume this existing claim. Do **not** auto-claim another range.

1. Fresh-read current `main` and preserve any newer audio merges.
2. Use an **authorized provider surface that can retrieve existing contexts** to resolve/export the raw MP3 artifact for every provider context already recorded in `takes/015.json`, `016.json`, and `017.json`. Do not regenerate merely to solve export plumbing.
3. For each successful export, update the existing take entry with the raw durable `artifact_url` or durable take binary reference and advance status from `submitted` to `artifact_captured`. Add the exact transcript to the JSON record if the authorized export surface returns/validates it; otherwise derive it mechanically from the locked first/last source boundaries without rewriting prose.
4. If any provider output itself is missing, truncated, corrupt, mispronounced, or otherwise bad, repair **only that take**.
5. Stitch each chapter in exact take order to `greg-again/audio/assets/chapter-015.mp3`, `chapter-016.mp3`, and `chapter-017.mp3`.
6. Verify exact source coverage/order, seam continuity, playability, route title, pronunciation authority, and duration under `r2/AUDIO_PRODUCTION.md`.
7. Fresh-read `main` again immediately before touching shared files. Reconcile `greg-again/audio/manifest.json`, append only verified 015-017 entries, run repository checks, publish via PR/merge, verify `main`, then leave the next handshake.

Do not regenerate the entire chapters because export is blocked. The 27 queued provider contexts, deterministic source seams, and take identities are durable work and remain the production assets to recover first.
