# Chapter 003 Audio Score v2 Production Status

Claim branch: `audio/v2-greg-again-ch003-auto`
Authority base: `audio-score/chapters-001-010` (PR #287 still open at claim time)
Audio Score source: `r2/assets/audio-score/ch003.md`
Audio Score blob SHA: `211ed23b1bfc34f3f37144d31f91eec60fff0ab2`
Voice: `deep`
Take map: `greg-again/audio/v2/takes/003/take-map.md`
Score repairs: none
Reusable Audio Score lesson: none promoted; this production did not reach human listen-back.

## Provider submissions

All 12 locked takes were submitted once. Do not regenerate merely because binary transfer is incomplete.

| Take | Provider context_id | Provider audio URL | Returned status |
| --- | --- | --- | --- |
| 01 | `bb70b5d05d2c4ff192c012caf3d9456d` | `https://www.aidocmaker.com/g0/audio?name=bb70b5d05d2c4ff192c012caf3d9456d` | queued |
| 02 | `23da008683e349f289c88833e3016205` | `https://www.aidocmaker.com/g0/audio?name=23da008683e349f289c88833e3016205` | queued |
| 03 | `7af38f24f9074594ba89dff3c9f307f6` | `https://www.aidocmaker.com/g0/audio?name=7af38f24f9074594ba89dff3c9f307f6` | queued |
| 04 | `b02dea1a99cf45b8a5864bc2405ce776` | `https://www.aidocmaker.com/g0/audio?name=b02dea1a99cf45b8a5864bc2405ce776` | queued |
| 05 | `972ce519e1134be196824962c1ffda15` | `https://www.aidocmaker.com/g0/audio?name=972ce519e1134be196824962c1ffda15` | queued |
| 06 | `234c42a700a44d15a9779b955a8b0867` | `https://www.aidocmaker.com/g0/audio?name=234c42a700a44d15a9779b955a8b0867` | queued |
| 07 | `d5826c04f11544d7a296f5b54bc10416` | `https://www.aidocmaker.com/g0/audio?name=d5826c04f11544d7a296f5b54bc10416` | queued |
| 08 | `c8aa4a9fc12f47fcbeb0667661bf6474` | `https://www.aidocmaker.com/g0/audio?name=c8aa4a9fc12f47fcbeb0667661bf6474` | queued |
| 09 | `192cb997afad4146bf5f5d0a2827a86d` | `https://www.aidocmaker.com/g0/audio?name=192cb997afad4146bf5f5d0a2827a86d` | queued |
| 10 | `25d3f51c1e2c4e90bbcf011b64224349` | `https://www.aidocmaker.com/g0/audio?name=25d3f51c1e2c4e90bbcf011b64224349` | queued |
| 11 | `65e2eebe58df4c34b896f74dc0322a68` | `https://www.aidocmaker.com/g0/audio?name=65e2eebe58df4c34b896f74dc0322a68` | queued |
| 12 | `a944bfd62d9c471cbe19a0f73368b253` | `https://www.aidocmaker.com/g0/audio?name=a944bfd62d9c471cbe19a0f73368b253` | queued |

Provider-facing aliases applied only for synthesis: `mana` -> `ma-na`; `Vale` -> `Vayle`. Source text remains unchanged.

## Current blocker

The available voice-generation surface returned provider context IDs and audio URLs, but did not expose a durable binary/file reference in this worker. A direct downstream download attempt could not cross the artifact boundary from this environment. Therefore the chapter cannot yet be assembled, listened back, verified, entered into the v2 completion manifest, or switched in the public manifest without risking false completion.

## Exact next action

Recover the already-generated audio binaries for the 12 provider context IDs above without regenerating successful synthesis. Save them in deterministic take order, assemble `greg-again/audio/assets/v2/chapter-003.mp3` with the established ~2 second terminal silence, verify score coverage/seams/playability/pronunciations, then reconcile `greg-again/audio/v2/manifest.json` and switch only Chapter 003 in `greg-again/audio/manifest.json` to `assets/v2/chapter-003.mp3`.