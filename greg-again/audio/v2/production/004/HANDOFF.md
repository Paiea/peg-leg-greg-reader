# Audio Score v2 Chapter 004 Handoff

- **Chapter claimed:** 004 — `Thirty Days`
- **Claim branch:** `audio/v2-greg-again-ch004-auto`
- **Audio Score source:** `r2/assets/audio-score/ch004.md`
- **Audio Score blob SHA:** `7c2f4b9cdf40fe8035568fa7e503bff4589780fe`
- **Takes:** 13 locked; all 13 submitted once to `deep`; provider context IDs / artifact URLs recorded in `STATUS.md`
- **Takes generated / captured:** provider responses returned `queued`; completion cannot be polled with the available action and binaries have not crossed the durable artifact boundary
- **Final MP3:** not assembled
- **v2 manifest:** unchanged; chapter must not be marked complete yet
- **Public manifest:** unchanged; Chapter 004 still uses its existing v1 route
- **Audio Score repair:** none
- **Reusable lesson:** no new doctrine promoted. The score segmented cleanly at cadence/action boundaries; no evidence yet from human listen-back to justify a score change.
- **Exact blocker:** current voice tooling exposes submission plus provider context/artifact URL, but no status/download action. This runtime still cannot resolve the provider host, so take binaries cannot be recovered directly here.

## Assembly authorization and binary-drop contract

Keoni explicitly authorized completing assembly and promoting Chapter 004 into current audio authority once the take binaries are available. No second approval is required for the already-defined Chapter 004 publication steps after verification.

Recover the existing provider artifacts without regenerating successful synthesis. Store the thirteen binaries as:

- `greg-again/audio/v2/takes/004/take-01.mp3`
- `greg-again/audio/v2/takes/004/take-02.mp3`
- `greg-again/audio/v2/takes/004/take-03.mp3`
- `greg-again/audio/v2/takes/004/take-04.mp3`
- `greg-again/audio/v2/takes/004/take-05.mp3`
- `greg-again/audio/v2/takes/004/take-06.mp3`
- `greg-again/audio/v2/takes/004/take-07.mp3`
- `greg-again/audio/v2/takes/004/take-08.mp3`
- `greg-again/audio/v2/takes/004/take-09.mp3`
- `greg-again/audio/v2/takes/004/take-10.mp3`
- `greg-again/audio/v2/takes/004/take-11.mp3`
- `greg-again/audio/v2/takes/004/take-12.mp3`
- `greg-again/audio/v2/takes/004/take-13.mp3`

Once all thirteen real MP3s exist:

1. Verify every file is playable and corresponds to its locked transcript/provider identity.
2. Audition seams and repair only a genuinely failed local take. Preserve acceptable takes.
3. Assemble strictly `01 → 13`, with no crossfades/music/effects and no duplicate seam text.
4. Ensure the final listener-facing chapter has about 2 seconds of settling silence after the final spoken word.
5. Write the verified result to `greg-again/audio/assets/v2/chapter-004.mp3`.
6. Refresh current GitHub authority before shared-file writes.
7. Reconcile `greg-again/audio/v2/manifest.json`, preserving sibling workers' newer entries, and mark Chapter 004 complete with its source identity, duration, and take metadata.
8. Reconcile `greg-again/audio/manifest.json` and switch **only Chapter 004** to `assets/v2/chapter-004.mp3`, preserving stable chapter identity/title/image metadata and unrelated newer changes.
9. Verify the public route resolves to and plays the v2 Chapter 004 MP3.
10. Update verification/production evidence and integrate the completed Chapter 004 work into the resolved Audio Score authority.

Do not publish or update either manifest before the assembled MP3 passes verification.
