# Chapter 002 Audio Score v2 Verification

Status: **BLOCKED BEFORE BINARY CAPTURE / ASSEMBLY**

## Verified now

- Claim branch: `audio/v2-greg-again-ch002-auto`
- Spoken source: `r2/assets/audio-score/ch002.md`
- Audio Score blob SHA: `5f7cd653880568baad4fd65ab88ef1eaf327e026`
- Clean source identity recorded by score: `r2/assets/written/ch002.md` @ `5304f99a6192d9ee73d5eb254990c5e63d0f284c`
- 12 intended takes are locked in deterministic order.
- Locked take transcripts cover the full Audio Score body after its metadata/header separator exactly once by construction.
- Dialogue ownership, prices, quantities, names, and binding wording were preserved in the locked transcripts.
- Voice target is `deep` for every take.
- Take 10 applies the hard provider-facing pronunciation alias `Mana` -> `Ma-na`; the earlier literal-`Mana` submission is preserved but explicitly superseded.
- All 12 active take generations were accepted by the provider and have preserved context IDs / recovery URLs in `greg-again/audio/v2/takes/002/provider-artifacts.json`.
- No chapter-local Audio Score prose repair was made.

## Not yet verifiable in this runtime

- Provider generation completion state beyond the returned `queued` status.
- Actual binary capture for the 12 active takes.
- Audition / subjective cadence QA.
- Final ordered MP3 assembly.
- Duplicate/missing seam verification against assembled audio.
- Playability / duration / SHA-256 of final MP3.
- ~2 second chapter-tail settling silence.
- Listener-facing asset `greg-again/audio/assets/v2/chapter-002.mp3`.
- v2 manifest completion entry.
- Public manifest switch from legacy `assets/chapter-002.mp3` to `assets/v2/chapter-002.mp3`.
- Public-route verification.

## Hard blocker

The available voice-generation action returns provider `context_id` and `audio_url` references but exposes no fetch/status action for recovering the generated audio binary. The current execution runtime also cannot resolve/download the AI Doc Maker URL directly. Per `r2/AUDIO_PRODUCTION.md`, successful synthesis must not be regenerated merely to solve this downstream plumbing problem.

## Exact next action

Retrieve the 12 **active** provider artifacts using the preserved context IDs/URLs without regenerating them. Discard the superseded literal-`Mana` Take 10 from assembly. Audition and locally repair only concrete failures. Assemble active Takes 01-12 in numeric order, append about 2 seconds of chapter-tail silence, verify coverage/seams/playability, write `greg-again/audio/assets/v2/chapter-002.mp3`, then reconcile newest Audio Score authority plus both manifests and switch only Chapter 002's public `audio_src` after verification.
