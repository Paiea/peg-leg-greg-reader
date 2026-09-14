# 3L SHORT-TAKE AUDIO PRODUCTION AUTHORITY

Status: **CURRENT PRODUCTION AUTHORITY**

This file governs synthetic audio capture and assembly for 3L. Where an older production note conflicts with this file, this file wins.

## Core rule

3L audio is built from **short, preview-safe canon chunks** and then assembled.

Do not use full-chapter synthesis as the production source.

The production path is:

**CANON PROSE → SEMANTIC SPEAKER ROUTING → PREVIEW-SAFE CHUNKS → REQUIRED VOICE CAPTURES → LOCAL SPEAKER SELECTION → CANON-ORDER ASSEMBLY → VERIFY → PUBLISH**

Canon prose remains the story authority.

## Dialogue territory rule

Greg owns the account. Ithar owns the examination.

A Dragon entrance is a production seam and must earn that seam.

- Prefer a few sustained Ithar territories over repeated short alternation.
- Routine questions may be carried by Greg narration when canon says so.
- Short Dragon lines survive when the shortness itself matters.
- Sustained Ithar speech may span multiple prose paragraphs. The router must keep the entire open quotation in the Dragon role until its closing quotation mark.
- Do not flatten a multi-paragraph Ithar speech into one paragraph merely to make the audio system easier.
- Do not create a Greg-to-Dragon splice inside an attribution sentence such as narration followed by `he said` or `he asked` when canon can provide a clean boundary.
- Every Record 002–010 contains at least one deliberate Ithar checkpoint.

The manuscript owns the territory shape. Production follows it.

## Audio identities

There are only two recurring audio identities in the current 3L system.

### Greg identity

Use the Greg identity for:

- all narration
- Greg's spoken dialogue
- young Greg
- older Greg
- all remembered-life characters unless a later authority explicitly expands the cast

Profile:

- voice = `deep`
- tempo = 1.0
- no pitch shift
- no formant shift

### Dragon identity

Use the Dragon identity only for Ithar's actual spoken dialogue.

Profile:

- voice = `normal`
- tempo = 1.0
- pitch shift = 0 semitones
- no formant shift
- no monster DSP

The Dragon should sound different because he speaks differently, not because the waveform was bent.

## Canon chunk size

Target natural sequential chunks of roughly 20–29 seconds.

For the current voice generator, every submitted source capture must be preview-safe, normally no more than about **500 characters**.

Preferred chunk boundaries, in order:

1. paragraph boundary
2. complete dialogue turn
3. complete sentence
4. clause boundary only when necessary

Do not split mid-sentence merely to make chunks equal length.

If an oversize paragraph must be split, preserve its already-resolved semantic speaker spans. Never re-infer speaker ownership after the split.

## Required-voice capture rule

The generated short-dual plan is the executable routing contract.

Each chunk contains:

- exact transcript
- exact character count
- semantic speaker spans
- `required_voices`
- whether the chunk needs both identities

Capture only the voices listed in `required_voices`.

For a mixed cave-frame chunk, render the **same exact chunk transcript twice**:

- Greg source → `deep`
- Dragon source → `normal`

For a Greg-only chunk, capture only `deep`.

For a Dragon-only chunk, capture only `normal`.

Workers and assemblers do not decide the speaker from nearby prose. The plan has already decided it.

## Generator contract

For every source capture:

- `transcript` and `preview_transcript` must be identical
- the complete submitted text must fit the preview-safe limit
- use the exact transcript from the current plan
- do not rewrite punctuation, wording, names, or sentence order
- capture the returned playable `preview_url`
- record record number, chunk index, voice identity, exact transcript, context id, preview URL, and returned full-audio URL when available
- the preview MP3 is the preferred assembly source

A capture is stale if its transcript or required voice does not exactly match the current plan.

## Semantic speaker selection

Narration always belongs to Greg, including narration describing Ithar.

Greg's spoken dialogue belongs to Greg.

Ithar's actual spoken dialogue belongs to Dragon.

Remembered-life characters belong to Greg.

Within a mixed chunk, select spans from the matching source render according to the plan:

- Greg span → `deep` source
- Ithar span → `normal` source

Speaker transitions should occur at the plan's semantic boundaries and be snapped to nearby real silence where possible.

Do not infer Dragon ownership merely because a paragraph mentions the dragon.

## Assembly

For every source preview MP3:

1. download it
2. ffprobe it before use
3. detect usable silence boundaries
4. map semantic transitions from the plan
5. select Greg spans from `deep` and Ithar spans from `normal`
6. concatenate local spans back into exact chunk order
7. concatenate completed chunks in canon order

Assembly should:

- normalize technical format only as necessary
- preserve generated timing inside selected spans
- use intentional seam silence only
- avoid blanket dramatic pauses between chunks
- append approximately 2 seconds of settling silence at chapter end
- encode the final chapter MP3
- ffprobe and decode-verify the finished asset
- record duration, byte size, and SHA-256

A seam is successful when the chapter sounds like one continuous performance rather than stitched source files.

## Canon fidelity

The ordered chunk transcripts must reproduce the chapter text exactly apart from non-spoken Markdown headings and production metadata.

Production-only speaker labels, worker claims, chunk numbers, timing maps, and comments are never spoken and never render publicly.

Do not rewrite canon prose merely to make synthesis easier. A wording change belongs at canon authority before production begins.

## Parallel worker rule

Parallel workers are capture workers, not editors or architects.

They may:

- read the current frozen work order
- generate only their assigned captures
- verify their own returned receipts
- write only their assigned worker manifest
- report failures without improvising

They may not:

- edit manuscript prose
- change speaker ownership
- change chunk boundaries
- change voice profiles
- add DSP
- assemble or publish the chapter
- reuse stale captures without an explicit coordinator decision
- modify another worker's manifest or claim

The coordinator owns plan generation, work partitioning, reconciliation, assembly, verification, and publication.

See `3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md` for the detailed five-worker contract.

## Website publication

Each record page keeps its prose and chapter audio together.

The separate Listening Archive remains the audio-first library.

Do not expose replacement chapter audio until the assembled MP3 has passed decode verification.

Partial captures remain internal production material.

## Superseded methods

The following are not current production methods:

- full-chapter Greg render plus full-chapter Ithar render plus post-hoc slicing
- one synthesis request for every microscopic speaker turn
- pitch-shifted or slowed Dragon by default
- one mixed-speaker render used as the final two-voice performance
- long generated audio substituted for the short-take factory merely because it exists
- worker-side speaker inference
- worker-side prose repair

## Current regeneration status

Records 002 and 003 were previously published from an older dialogue shape. Those audio assets and their historical capture manifests remain valid evidence of the older production run, but they are **stale against the dialogue-territory rebuild**.

Do not treat the prior 002/003 hashes, durations, or capture-complete flags as current production authority for the revised canon.

The revised workflow is:

1. regenerate 002/003 short-dual plans from current canon
2. freeze the plans and five-worker work order
3. capture all required sources through bounded workers
4. reconcile receipts
5. assemble and verify replacement MP3s
6. publish only after verification
