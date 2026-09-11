# Chapter 010 Audio Score v2 Verification

## Source and identity

- [x] Correct spoken authority: `r2/assets/audio-score/ch010.md`
- [x] Source blob SHA recorded: `bf0e024b5117ad519d24cc2ed3ce629b3afbcf05`
- [x] Chapter identity: `ga-010`, number `10`, current title `What Moved`
- [x] Clean written rendition was not edited

## Spoken coverage and take order

- [x] 25 ordered provider-facing transcripts locked in `greg-again/audio/v2/takes/010/take-map.md`
- [x] Take map follows the Audio Score from opening through the final ellipsis landing once, in source order
- [x] No intentional score passage was removed or repeated at a seam
- [x] Dialogue ownership, four-unit order, prices/terms references, names, and other factual bindings were preserved from the score
- [x] Pronunciation authority respected with provider-only `ma-na` and `Vayle` substitutions

## Artifact verification

- [x] All 25 preview MP3 artifacts captured durably
- [x] Every take passed `ffprobe`
- [x] Deterministic ascending take order used for assembly
- [x] Final MP3 passed `ffprobe`
- [x] Final duration: `591.480000` seconds
- [x] Final MP3 SHA-256: `b0c65a9d96985703d693d05516439ca2a83bf10d9d722e01b7854221d9356474`
- [x] Final asset path: `greg-again/audio/assets/v2/chapter-010.mp3`
- [x] Approximately two-second settling tail added after the assembled spoken content

## Publication

Manifest and public-route reconciliation are the final publication step. These boxes become authoritative only from the reconciled shared authority, not from a stale branch snapshot.

- [ ] `greg-again/audio/v2/manifest.json` reconciled
- [ ] `greg-again/audio/manifest.json` Chapter 010 routed to `assets/v2/chapter-010.mp3`
- [ ] route verified from reconciled authority

## Listen-back boundary

No subjective listening claim is made here. If human listen-back identifies a concrete cadence/pronunciation failure, repair only that local take or score passage and preserve all unaffected provider work.
