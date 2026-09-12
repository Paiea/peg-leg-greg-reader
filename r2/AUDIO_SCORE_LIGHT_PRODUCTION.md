# Greg, Again — Audio Score Light Production

Status: **ACTIVE FOR SCORE 2 / LIGHT REVOICE WORK**

This file owns production routing for the Light Score generation.

Read `r2/AUDIO_SCORE_LIGHT.md` first. Also read `r2/AUDIO_PRODUCTION.md` for the established artifact, assembly, verification, and publication mechanics. Where this file conflicts for Light work, this file wins.

## Scope

Current campaign scope is Chapters 001-030.

Exact spoken source:

`r2/assets/audio-score-light/chNNN.md`

Do not synthesize a Light chapter until:

`python scripts/audio_score_light_validate.py NNN`

passes.

## Generation identity

- generation: `audio-score-light`
- narrator: `deep`
- final asset: `greg-again/audio/assets/light/chapter-NNN.mp3`
- completion registry: `greg-again/audio/light/manifest.json`
- take evidence: `greg-again/audio/light/takes/NNN/`
- full-capture evidence: `greg-again/audio/light/full/NNN/`
- production evidence: `greg-again/audio/light/production/NNN/`
- verification evidence: `greg-again/audio/light/verification/NNN/`

Existing legacy and v2 / Score 1 assets are immutable historical generations. Do not overwrite or delete them.

## Ownership

Use at most five simultaneous synthesis lanes.

One lane owns one chapter. When a lane fully verifies and publishes its chapter, it may claim the next earliest eligible unowned Light chapter.

Do not pre-claim all 30 chapters.

A legacy or v2 publication does not make a chapter unavailable for Light. Only active Light ownership or completed Light publication does.

## Voice factory

Prefer the cheapest mechanically safe capture mode.

### Fast path: provider full chapter

When the current voice provider accepts the entire exact Light transcript and returns a downloadable full-audio URL:

1. send the complete Light chapter as one `deep` voice job
2. generate a short inline preview only as a convenience; the preview is not the chapter artifact
3. record the provider context ID, full `audio_url`, optional `preview_url`, and SHA-256 of the exact full transcript sent
4. write that evidence to `greg-again/audio/light/production/NNN/FULL_CAPTURE.tsv`
5. GitHub Actions must recompute the exact Light transcript SHA and reject any mismatch
6. download the full provider audio and require a nontrivial playable audio stream via `ffprobe`
7. add approximately two seconds of silence only after the final spoken word
8. verify/hash the final MP3 and record full-capture evidence
9. reconcile Light and public manifests only after mechanical verification succeeds

A provider player page, gated response, tiny file, or non-audio response is a failed fast-path capture. Do not publish it.

### Fallback: preview-safe short takes

If the provider full-audio artifact cannot be downloaded or verified, use the proven preview-safe short-take factory:

1. split at natural performance boundaries, normally <=500 provider characters
2. use `deep`
3. send identical provider-facing text as `transcript` and `preview_transcript`
4. capture the returned playable `preview_url`
5. preserve context ID, preview URL, source text, provider-facing text, order, voice, and substitutions
6. download and `ffprobe` every preview artifact in GitHub Actions
7. stitch verified chunks in deterministic order
8. add approximately two seconds of silence only after the final spoken word
9. `ffprobe` the final MP3 and record duration/hash

Never regenerate a durable good artifact merely because downstream plumbing failed.

## Provider-facing pronunciation

Keep normal pronunciation aliases provider-facing where possible, including current established handling such as `mana` / `Mana`, `Vale`, and `sparring` when the renderer needs it.

Pronunciation substitutions do not count as Light prose changes when they exist only in provider-facing take text.

## Opportunistic reuse

Existing durable audio may be reused only when exact transcript identity can be proven for the reused span.

Do not infer transcript identity from chapter number, an old note, similar prose, or the existence of an MP3.

When transcript identity is not durably provable, synthesize the Light source normally.

## Publication

Light chapters publish independently.

After full verification:

1. reconcile `greg-again/audio/light/manifest.json`
2. refresh newest `greg-again/audio/manifest.json`
3. change only that chapter's public `audio_src` to `assets/light/chapter-NNN.mp3`
4. set `audio_finish` to `audio-score-light`
5. preserve stable chapter ID, number, title, lens/image metadata, and unrelated newer changes
6. verify the public route resolves to the Light asset

Mixed legacy / v2 / Light playback is valid while the campaign is incomplete.

## Completion gate

A Light chapter is complete only when:

- written source identity is recorded
- Light validator passes <=15%
- every intended Light word is represented exactly once in the submitted transcript
- durable provider audio exists
- final MP3 is playable
- listener tail is present
- Light manifest is reconciled
- public manifest points that chapter to the Light asset
- current GitHub authority verifies the route

If subjective listen-back was not performed, record `verified_unlistened` rather than implying otherwise.
