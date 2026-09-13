# 3L SHORT-TAKE PRODUCTION AUTHORITY

## STATUS

This document governs preview-safe short-take audio production for 3L.

Current production frontier:

- Record 001: published separately under its existing Record 001 authority and v6 listening surface.
- Record 002: verified dual-voice assembled asset at `3l/assets/audio/record-002.mp3`.
- Record 003: verified dual-voice assembled asset at `3l/assets/audio/record-003.mp3`.
- Records 004+: not part of this production slice.

Records 002 and 003 use the locked two-identity routing:

- Greg / narration / remembered speakers → `deep`
- Ithar only → `normal`

The current Dragon production default is untreated:

- tempo 1.0
- pitch shift 0 semitones
- formant shift 0
- no Dragon post-processing
- preserve normal source timing except for semantic assembly pauses and clean seams

The final assembled assets add an approximately 2-second settling tail and use 192k final MP3 encoding.

---

## 1. PURPOSE

The short-take system exists to make long-form synthetic narration reproducible, inspectable, and recoverable without requiring one monolithic generation request.

The production unit is a preview-safe chunk, generally no more than about 500 characters.

Each chunk is generated independently, captured by its returned public preview URL, verified as valid audio, and then assembled from locked semantic speaker ownership.

Canon prose remains authority.

Production artifacts may segment, tag, or splice the prose, but may not change story wording or meaning.

---

## 2. SOURCE HIERARCHY

Use this order:

1. canonical manuscript record
2. locked semantic speaker/chunk plan
3. capture manifests
4. source verification receipt
5. assembled audio audit receipt
6. published MP3 asset

If any lower layer disagrees with a higher layer, the higher layer wins.

Do not repair disagreement by silently editing canon prose.

---

## 3. PREVIEW-SAFE CAPTURE RULE

For every generation call:

- provide the exact full chunk transcript
- provide the identical text as `preview_transcript`
- keep the preview transcript within the voice tool's preview-safe limit
- use the voice required by the locked chunk plan
- capture the returned `context_id`
- capture the returned `preview_url`
- record status only when the tool reports the take ready

Do not use a long full-chapter generation as a substitute for the preview-safe source set.

The preview URL is the reproducible source used by GitHub Actions for assembly.

---

## 4. SPEAKER-PURE ROUTING

A voice render is not a semantic speaker decision.

For mixed chunks, generate the exact same chunk text in each required voice, then let the semantic splice plan select only the regions owned by that speaker.

This means a mixed Greg/Ithar chunk commonly has:

- one `deep` render of the complete chunk
- one `normal` render of the complete chunk

The assembler chooses Greg-owned regions from the `deep` source and Ithar-owned regions from the `normal` source.

For Greg-only chunks, generate only `deep`.

Do not generate `normal` unnecessarily for a Greg-only chunk.

Do not infer speaker ownership from words such as “dragon,” “Ithar,” or dialogue proximity. Speaker ownership comes from the locked semantic spans.

---

## 5. NARRATION RULE

All narration belongs to Greg's audio identity, including narration whose grammatical subject is Ithar.

Examples such as:

- `Ithar waited.`
- `The dragon lowered his head.`
- `His eye narrowed.`

remain Greg narration.

Only words actually spoken by Ithar use the Dragon voice.

---

## 6. CAPTURE MANIFESTS

Capture manifests are append-only production evidence for a bounded chunk range.

Suggested naming:

`record-003-short-captures-021-025.json`

Each capture entry records at minimum:

- chunk number
- voice
- exact transcript
- context ID
- preview URL
- ready status

A capture manifest must not claim a source that was not actually returned by the generator.

---

## 7. SOURCE VERIFICATION

The source verifier must independently:

1. read the locked chunk plan
2. gather all capture manifests for that record
3. reject duplicate `(chunk, voice)` pairs
4. reject unknown chunks
5. reject voices not required by the plan
6. require exact transcript equality with the locked plan
7. require ready status
8. download every preview MP3
9. decode-check every MP3 with ffmpeg
10. obtain positive duration with ffprobe
11. record byte size and SHA-256
12. calculate the full expected capture set
13. report missing captures explicitly

A record is source-complete only when:

- verified capture count equals planned capture count
- `complete = true`
- `missing = []`

Do not assemble an incomplete record.

---

## 8. SEMANTIC SPLICE ASSEMBLY

The assembler consumes the verified source receipt, not unverified capture manifests directly.

For a mixed chunk:

- collapse adjacent semantic spans with the same role into speaker regions
- align region text against the identical full-chunk renders
- cut only at actual role transitions
- select Greg regions from `deep`
- select Ithar regions from `normal`
- concatenate regions in canonical order

Do not create micro-cuts at every sentence when speaker ownership has not changed.

The point of semantic splice assembly is to preserve natural source cadence while changing voices only where the speaker actually changes.

---

## 9. AUDIO PROCESSING AUTHORITY

For Records 002 and 003:

- Greg voice: `deep`
- Dragon voice: `normal`
- tempo: 1.0
- pitch: 0 semitones
- formant shift: 0
- Dragon post-processing: false

Do not reintroduce the earlier audition treatments into these records.

Do not slow Ithar merely to make him sound older.

Do not lower Ithar merely to make him sound monstrous.

The writing, semantic identity, patience, and cadence carry the distinction.

---

## 10. FINAL ASSET VERIFICATION

After assembly:

- decode-check the final MP3 with ffmpeg
- record duration
- record byte size
- record SHA-256
- confirm audio processing metadata matches authority
- confirm settling tail and output bitrate settings
- write an assembled-audio audit receipt
- commit the MP3 and audit together

The final audit is the proof artifact for the published MP3.

---

## 11. CURRENT VERIFIED RESULTS

### Record 002 · THE CLAIMANT

- source captures: 64 / 64 verified
- source complete: true
- chunks: 33
- mixed chunks: 31
- final duration: 881.737143 seconds
- final bytes: 21,162,362
- final SHA-256: `5aea20e8d197b8f0125ca46b2e397006d6e07fdeb1bc4e08fbfda78c06229d95`
- final asset: `3l/assets/audio/record-002.mp3`

### Record 003 · THE BARGAINER

- source captures: 62 / 62 verified
- source complete: true
- chunks: 32
- mixed chunks: 30
- final duration: 881.658776 seconds
- final bytes: 21,160,481
- final SHA-256: `c0e98b27b943fb75a49b30eacd33d398f821aa1cd308b60cb1958ce4a22db0ea`
- final asset: `3l/assets/audio/record-003.mp3`

These results are production facts, not listening-quality judgments. Human listening can still identify aesthetic seam or performance issues even when technical verification is green.

---

## 12. SITE PUBLICATION

When a final verified asset exists, the corresponding record page and Listening Archive may point directly to:

`../assets/audio/record-XXX.mp3`

Do not label a record “audio in production” after its verified asset has been published to the same branch.

Site tests should verify:

- the MP3 exists
- the record page references it
- the Listening Archive references it
- autoplay is not enabled
- stale production-status text is absent

---

## 13. WORKFLOW RULE

The source verifier and assembler are separate gates.

GitHub does not trigger a second workflow from a commit made by another workflow using the default `GITHUB_TOKEN` in every push-chain scenario. Therefore the assembler supports explicit `workflow_dispatch` in addition to path-triggered pushes.

If a complete verifier receipt was committed by Actions but assembly did not automatically start, manually dispatch the assembler rather than modifying unrelated production files merely to create another push event.

---

## 14. STOP CONDITIONS

Stop and investigate instead of assembling when any of the following occurs:

- transcript mismatch
- duplicate capture key
- missing required voice
- source URL does not download
- ffmpeg cannot decode a source
- source duration is suspicious
- verified count does not equal planned count
- semantic span ownership is ambiguous
- final audit hash does not match the committed asset
- processing metadata violates current authority

Evidence before assertion.
