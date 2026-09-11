# Chapter 005 — Provider Artifact Registry

Audio Score source: `r2/assets/audio-score/ch005.md`
Audio Score blob SHA: `843bee0da9f81deb4fa4e8dff3d6a50b77591332`
Voice: `deep`

All twelve takes were submitted as independent voice-generation requests. Successful synthesis must be recovered from these provider identities before any regeneration is attempted.

| Take | Provider context ID | Provider recovery URL | Submission status |
|---|---|---|---|
| 01 | `9799c33446f54e5c975b7acef7ce8fb4` | `https://www.aidocmaker.com/g0/audio?name=9799c33446f54e5c975b7acef7ce8fb4` | queued |
| 02 | `26aee1987b184f67952bd405fd72ddd0` | `https://www.aidocmaker.com/g0/audio?name=26aee1987b184f67952bd405fd72ddd0` | queued |
| 03 | `493fb3432b454c4c9e7a63a82b231c5b` | `https://www.aidocmaker.com/g0/audio?name=493fb3432b454c4c9e7a63a82b231c5b` | queued |
| 04 | `9a42ebd9307a462ab269bb80964907ca` | `https://www.aidocmaker.com/g0/audio?name=9a42ebd9307a462ab269bb80964907ca` | queued |
| 05 | `32aa814b8a4c4b0984b3c270c85db947` | `https://www.aidocmaker.com/g0/audio?name=32aa814b8a4c4b0984b3c270c85db947` | queued |
| 06 | `a150a159a281403f9b613e69def6abe0` | `https://www.aidocmaker.com/g0/audio?name=a150a159a281403f9b613e69def6abe0` | queued |
| 07 | `5c0b41f4294c4dbba4a4fd2a1121adf3` | `https://www.aidocmaker.com/g0/audio?name=5c0b41f4294c4dbba4a4fd2a1121adf3` | queued |
| 08 | `b19b8b21218545c89969064f2aa4d131` | `https://www.aidocmaker.com/g0/audio?name=b19b8b21218545c89969064f2aa4d131` | queued |
| 09 | `efb3ed74ad714e08b0bdc6bb49ed31b8` | `https://www.aidocmaker.com/g0/audio?name=efb3ed74ad714e08b0bdc6bb49ed31b8` | queued |
| 10 | `a57fd56e3681467080413db0668f864e` | `https://www.aidocmaker.com/g0/audio?name=a57fd56e3681467080413db0668f864e` | queued |
| 11 | `6e449d27f8ac4fbe86303858b6ca5efb` | `https://www.aidocmaker.com/g0/audio?name=6e449d27f8ac4fbe86303858b6ca5efb` | queued |
| 12 | `5bf1bab0c77441049cfc5379c84a4706` | `https://www.aidocmaker.com/g0/audio?name=5bf1bab0c77441049cfc5379c84a4706` | queued |

Provider-facing substitutions used:
- Take 03: `mana` -> `ma-na`
- Takes 05, 08, 10, 12: `Vale` -> `Vayle`

Artifact-boundary note: this worker can submit synthesis and receives provider context IDs/recovery URLs, but the available voice action exposes no status/download call for retrieving the completed binary. A direct recovery attempt through the working environment could not cross the provider boundary. Do not regenerate these takes merely to solve transfer plumbing.
