# Audio Score v2 — Chapter 008 Production Status

Chapter: 008 — Road Work
Claim branch: `audio/v2-greg-again-ch008-auto`
Source: `r2/assets/audio-score/ch008.md`
Audio Score blob SHA: `70fb72370291aa2a47b76d383cae9434254305e8`
Recorded clean-source SHA: `e7d5b96042c05407976a0e3204000fcccf614168`
Voice: `deep`
Take map: `greg-again/audio/v2/takes/008/take-map.md`

## Provider submissions

All 14 locked takes were submitted exactly once. Status returned by the available voice action was `queued` for each request. Preserve these identities; do not regenerate simply to solve artifact-transfer plumbing.

| Take | Context ID | Provider artifact URL | Returned status |
|---|---|---|---|
| 01 | `1407caaffca14c8fb90510cca8a29373` | `https://www.aidocmaker.com/g0/audio?name=1407caaffca14c8fb90510cca8a29373` | queued |
| 02 | `fe98a9248695496c87faced1bd4fc82b` | `https://www.aidocmaker.com/g0/audio?name=fe98a9248695496c87faced1bd4fc82b` | queued |
| 03 | `3ea254a853934159909729c41188bb18` | `https://www.aidocmaker.com/g0/audio?name=3ea254a853934159909729c41188bb18` | queued |
| 04 | `7a1deabdd4764540884f4418e1d3e003` | `https://www.aidocmaker.com/g0/audio?name=7a1deabdd4764540884f4418e1d3e003` | queued |
| 05 | `b69e5061030d4551b2e556eb6be71ff4` | `https://www.aidocmaker.com/g0/audio?name=b69e5061030d4551b2e556eb6be71ff4` | queued |
| 06 | `5d2045ba807d4ef69fe894bb1df2ca93` | `https://www.aidocmaker.com/g0/audio?name=5d2045ba807d4ef69fe894bb1df2ca93` | queued |
| 07 | `23b4bb2b5536435489136859f00fc5e2` | `https://www.aidocmaker.com/g0/audio?name=23b4bb2b5536435489136859f00fc5e2` | queued |
| 08 | `1ed8b9076bdc427dbc8f121bf567264e` | `https://www.aidocmaker.com/g0/audio?name=1ed8b9076bdc427dbc8f121bf567264e` | queued |
| 09 | `7fc488ff270e4acc90704e559fb4166a` | `https://www.aidocmaker.com/g0/audio?name=7fc488ff270e4acc90704e559fb4166a` | queued |
| 10 | `9cceb804f2c9447fb2fcfd2f3cde2cfd` | `https://www.aidocmaker.com/g0/audio?name=9cceb804f2c9447fb2fcfd2f3cde2cfd` | queued |
| 11 | `ac2e3147133d4a268d830d5863db4ff7` | `https://www.aidocmaker.com/g0/audio?name=ac2e3147133d4a268d830d5863db4ff7` | queued |
| 12 | `bebb4b6446eb438c87aa110cfae57a44` | `https://www.aidocmaker.com/g0/audio?name=bebb4b6446eb438c87aa110cfae57a44` | queued |
| 13 | `b75ed6a213c2422595509e72752a071a` | `https://www.aidocmaker.com/g0/audio?name=b75ed6a213c2422595509e72752a071a` | queued |
| 14 | `5f3b0f3105684cf4ab02d1dd3aaf5381` | `https://www.aidocmaker.com/g0/audio?name=5f3b0f3105684cf4ab02d1dd3aaf5381` | queued |

## Pronunciation / source handling

No Audio Score source repair was made.

Provider-facing substitution only:
- Take 04: `Mana` → `Ma-na`
- Take 11: `mana` → `ma-na`

The durable Audio Score text remains unchanged.

## Current completion boundary

The available voice action can submit synthesis and returns a provider context ID plus provider artifact URL, but it exposes no status polling or binary-download action. Until the returned audio binaries are durably retrievable, these takes have not crossed the provider artifact boundary defined by `r2/AUDIO_PRODUCTION.md`.

Therefore:
- final chapter MP3: NOT ASSEMBLED
- `greg-again/audio/assets/v2/chapter-008.mp3`: NOT CREATED
- v2 manifest: NOT UPDATED
- public manifest: NOT UPDATED
- publication: NOT CLAIMED

## Exact next action

Recover/download the already-submitted 14 provider artifacts using the context IDs/URLs above without regenerating them. Associate them with take numbers 01–14, assemble in order, add approximately 2 seconds of chapter-tail silence, audition/verify seams and pronunciation, then reconcile the newest v2 manifest and public manifest and publish Chapter 008 only.
