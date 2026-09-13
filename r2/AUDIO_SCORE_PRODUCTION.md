# Greg, Again — Audio Score v2 Production Override

Status: **ACTIVE FOR AUDIO-SCORE REVOICE WORK**

This file owns production routing for the Audio Score revoice generation. It is a narrow override of legacy source-selection and publication rules in `r2/AUDIO_PRODUCTION.md`.

Read both files. Where this file conflicts with the legacy protocol for Audio Score chapters, **this file wins**.

## Scope

Current production scope is Chapters 001–030 when their score files exist under:

`r2/assets/audio-score/chNNN.md`

The clean readable rendition remains under `r2/assets/written/` and must not be edited by ordinary v2 audio workers.

## Source authority

For v2 synthesis, the exact spoken source is the Audio Score file:

`r2/assets/audio-score/chNNN.md`

Do **not** fall back to the clean written chapter merely because it is more polished.

Do **not** run the legacy light Audio Finish over the clean prose instead.

The Audio Score is already the audio-native performance layer. Its awkward lineation, repetition, questions, ellipses, unfinished thoughts, abrupt resets, and thought webbing are intentional voice controls unless a listen-back proves a specific passage fails.

Story facts, dialogue ownership, prices, terms, causal relationships, and chapter identity still inherit from Story State / Greg Experience and the clean source recorded in the score header.

## Iterative improvement

The Audio Score layer is experimental and should learn from actual rendered audio.

A worker may make **small, chapter-local score repairs** when an audition or generated take reveals a concrete performance problem such as:

- a pause that is bulldozed
- a question that rises in the wrong place
- a declarative that lands unnaturally
- an ellipsis that produces a bad cadence
- a repeated musing that becomes tedious aloud
- a line break that fails to create separation
- a pronunciation or orthographic cue that the renderer mishandles

Prefer the smallest repair that fixes the heard problem. Preserve successful surrounding text and provider work.

Do not redesign the whole Audio Score system inside a routine chapter worker. Durable cross-chapter lessons belong back in `r2/AUDIO_SCORE.md` after repeated evidence.

## Codex boundary

Routine Audio Score production is **Codex-free by default**.

Normal chapter production should use the cheapest established owner for each stage:

1. deterministic Python / GitHub Actions for target resolution, chunk planning, validation, capture binding, downloading, `ffprobe`, stitching, settling tail, hashing, manifest reconciliation, and durable commits
2. normal Chat/Mana plus the available voice tool for the nondeterministic voice requests and compact provider-result capture
3. normal Chat/Mana or human listen-back for chapter-local performance judgment
4. direct GitHub tooling for branch / PR / merge operations when no engineering repair is required

Do not invoke Codex merely to:

- find the next chapter
- split a score into preview-safe takes
- submit established voice requests
- copy context IDs or preview URLs into capture results
- bind completed captures
- assemble audio
- reconcile manifests
- open or merge an otherwise routine production PR
- continue the same proven production recipe on another chapter

Codex is reserved for a bounded engineering intervention when the established factory itself is broken, missing a needed deterministic capability, or requires a cross-file implementation that normal Chat/tools cannot safely complete. Any such call inherits `state/editorial/CODEX_EXECUTION_POLICY.md` and should preferably remove Codex from future repetitions of the same work.

## v2 ownership

Legacy audio publication does **not** make a chapter unavailable for v2.

For v2, a chapter is unavailable only when:

- it is already present as published/verified in `greg-again/audio/v2/manifest.json`, or
- a live v2 single-chapter branch owns it, or
- an open v2 audio PR or durable v2 production evidence clearly owns it.

Use one chapter per worker.

Claim branch format:

`audio/v2-greg-again-chNNN-auto`

Examples:

- `audio/v2-greg-again-ch001-auto`
- `audio/v2-greg-again-ch002-auto`

Creating the branch is the claim. Never force-update an existing claim.

## v2 availability scan

Use the deterministic read-only resolver instead of manually rediscovering score, manifest, and single-chapter claim state:

```bash
python scripts/plg_ai_tools.py call audio_next --json '{}'
```

The underlying resolver is `scripts/audio_score_next.py`. It:

1. enumerates actual `r2/assets/audio-score/chNNN.md` files in scope
2. reads published numbers from `greg-again/audio/v2/manifest.json`
3. reads current v2 single-chapter claim refs
4. returns the earliest score chapter that is neither v2-published nor claimed

Resolution does **not** create a branch or mutate production state. Treat the returned `claim_branch` only as the branch name to attempt. The worker owns the chapter only after a create-only claim operation proves that this worker created that branch. If another worker wins the branch race, refresh authority and resolve again.

Do not treat the legacy `greg-again/audio/manifest.json` as proof that a v2 chapter is complete.

## Voice and performance

Use the established `deep` narrator unless explicit newer authority changes it.

The exact Audio Score text is the starting performance transcript. Do not silently clean it into page prose.

Provider-facing substitutions are allowed when they improve the actual sound without changing story meaning. This includes approved pronunciation substitutions and, when auditioned, nonstandard orthography or clipped spelling used only to shape performance.

Read `r2/AUDIO_PRONUNCIATION.md` before synthesis.

## Take production

Use the proven **short-take capture factory** whenever the provider exposes a durable preview artifact:

1. split the Audio Score at natural performance boundaries into preview-safe chunks, normally no more than about 500 characters
2. preserve the score wording exactly except approved provider-facing pronunciation/performance substitutions
3. use `deep`
4. send **identical text** as `transcript` and `preview_transcript`
5. require a returned playable `preview_url`; when available, prefer that durable preview artifact over an opaque provider-only audio URL
6. record the chunk transcript, provider context ID, preview URL, voice, order, and substitutions as production evidence
7. use GitHub Actions to download every preview URL, reject missing/trivial files, and `ffprobe` every chunk
8. stitch the verified chunks in deterministic order with ffmpeg
9. add the established approximately two-second settling tail only after the assembled final spoken word
10. `ffprobe` the final MP3, record hashes/duration, then proceed to v2 verification and manifest reconciliation

Chunk count is determined by **natural performance boundaries plus preview safety**, not by a target number of takes. A chapter may need substantially more than a dozen takes when the preview limit is the only reliable durable-artifact boundary.

Do not split so aggressively that every score line becomes a separate performance reset. Prefer coherent thought runs, dialogue turns, cadence changes, abrupt resets, action transitions, or other audible units that fit safely inside the preview ceiling.

One take equals one voice request. Preserve every successful provider artifact. Never regenerate a good captured take merely because downstream download, verification, stitching, or publication plumbing failed.

If a request does not return a durable preview artifact, preserve its provider evidence but do not pretend it crossed the artifact boundary. Prefer a preview-safe retry over an uncapturable long take when the long take cannot be made durable.

### Durable-artifact recovery override

For Audio Score v2, a provider submission is **not** a protected completed take merely because synthesis was accepted or because a provider context ID / opaque audio reference exists.

A take becomes protected provider work only when its synthesized audio is durably recoverable, for example through a playable `preview_url`, a captured binary, or another verified artifact that can actually be downloaded and assembled.

Therefore, when resuming an existing claimed chapter:

- preserve all old provider IDs, transcripts, substitutions, and recovery references as historical evidence
- if an old take has a durable playable artifact, keep it and do not regenerate it
- if an old take never crossed the durable artifact boundary, it may be rerun through the proven preview-safe short-take factory
- when the old segmentation itself depended on uncapturable long takes, re-split the exact Audio Score into natural preview-safe chunks rather than waiting indefinitely on opaque provider references
- this recovery rerun is **not** considered wasteful regeneration under the legacy preservation rule because no durable synthesized take existed to preserve

This override was introduced to unblock early 001–010 workers that successfully submitted synthesis but could not retrieve the resulting audio binaries, and remains valid for later chapters if the same failure mode appears. The durable boundary, not the provider request itself, decides whether a take must be preserved.

## Durable v2 paths

Listener-facing v2 chapter MP3:

`greg-again/audio/assets/v2/chapter-NNN.mp3`

V2 production evidence:

`greg-again/audio/v2/production/NNN/`

V2 take artifacts / maps:

`greg-again/audio/v2/takes/NNN/`

V2 verification evidence:

`greg-again/audio/v2/verification/NNN/`

Do not overwrite or relocate legacy v1 MP3s merely to normalize structure.

## Manifests and public routing

`greg-again/audio/v2/manifest.json` is the authoritative v2 completion registry.

The existing public player still reads:

`greg-again/audio/manifest.json`

After a v2 chapter is fully assembled and verified:

1. reconcile and add/update that chapter in `greg-again/audio/v2/manifest.json`
2. preserve the legacy MP3
3. reconcile the current public `greg-again/audio/manifest.json` against newest authority
4. switch only that chapter's public `audio_src` to `assets/v2/chapter-NNN.mp3`
5. update duration / take metadata for the v2 render while preserving chapter ID, number, title, image metadata, and unrelated newer chapter changes
6. verify the public route resolves to the v2 MP3

This allows Chapters 001–030 to migrate independently. Mixed v1/v2 public playback is valid during the transition.

## Completion gate

A v2 chapter is complete only when:

- Audio Score source identity is recorded
- every intended score segment is spoken exactly once
- dialogue / facts / quantities remain correct
- take artifacts are durable
- final MP3 is assembled and playable
- chapter tail has the established settling silence
- v2 manifest is reconciled
- public manifest points that chapter to the v2 asset
- the route is verified from current GitHub authority

If any of these fail, preserve the claim and durable work. Do not call the chapter published yet.
