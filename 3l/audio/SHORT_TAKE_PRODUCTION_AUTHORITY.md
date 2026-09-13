# 3L SHORT-TAKE AUDIO PRODUCTION AUTHORITY

Status: **CURRENT PRODUCTION AUTHORITY**

This file governs synthetic audio capture and assembly for 3L. Where an older production note conflicts with this file, this file wins.

## Core rule

3L audio is built from **short, preview-safe canon chunks** and then assembled.

Do not use full-chapter synthesis as the production source.

The production path is:

**CANON PROSE → SEMANTIC SPEAKER ROUTING → ~29-SECOND CANON CHUNKS → DUAL VOICE CAPTURE → LOCAL SPEAKER SELECTION → CANON-ORDER ASSEMBLY → VERIFY → PUBLISH**

Canon prose remains the story authority.

## Canon chunk size

Target natural sequential chunks of roughly **20–29 seconds**.

For the current voice generator, keep each submitted chunk **preview-safe**, normally no more than about **500 characters**.

Preferred chunk boundaries, in order:

1. paragraph boundary
2. complete dialogue turn
3. complete sentence
4. clause boundary only when necessary

Do not split mid-sentence merely to make chunks equal length.

The goal is the same capture geometry that worked for Record 001: stable, roughly half-minute pieces that seam cleanly.

## Dual-render rule

For cave-frame material containing both Greg and Ithar, render the **same exact short canon chunk twice**:

- **GREG SOURCE** → `deep`
- **DRAGON SOURCE** → `normal`

Both captures use identical text and identical chunk boundaries.

This is intentionally local. A ~29-second chunk may be dual-rendered; an entire chapter may not.

The two renders are source material for that one short chunk. They are not two alternate chapter performances.

## Semantic speaker selection

Narration always belongs to Greg, including narration describing Ithar.

Greg's spoken dialogue belongs to Greg.

Ithar's actual spoken dialogue belongs to the Dragon voice.

All remembered characters remain Greg's audio identity unless a later authority explicitly expands the cast.

Within each short dual-render chunk, use semantic speaker routing to select audio spans from the matching source render:

- narrator / Greg span → select from `deep`
- Ithar span → select from `normal`

Speaker transitions should be placed at real paragraph/dialogue boundaries and snapped to nearby detected silence where possible.

Do not infer Dragon ownership merely because the paragraph discusses the dragon. Only Ithar's spoken words use the Dragon source.

## Why dual-render chunks

Do not create hundreds of microscopic 1–3 second synthesis calls merely because cave dialogue alternates rapidly.

That produces unstable voice starts and turns the chapter into a playlist of fragments.

Short dual-render chunks preserve:

- stable ~29-second synthesis windows
- the proven Record 001 seam geometry
- distinct Greg / Ithar generated voices
- local, auditable speaker replacement
- no need for full-chapter alignment

## Generator contract

For each short source render:

- `transcript` and `preview_transcript` must be **identical**
- the complete submitted text must fit within the preview-safe limit
- capture the returned playable `preview_url`
- record record number, chunk index, voice identity, exact transcript, context id, and preview URL
- the preview MP3 is the assembly source

Each chunk therefore normally has two capture receipts: one `deep`, one `normal`.

Do not use a long-form full-chapter `audio_url` as the production source.

## Current voice profiles

### Greg

- voice = `deep`
- tempo = **1.0**
- no pitch shift
- no formant shift

### Ithar

- voice = `normal`
- tempo = **1.0**
- pitch shift = **0 semitones**
- no formant shift
- no monster DSP

Dragon identity comes from prose, semantic speaker ownership, cadence, patience, and turn structure, not waveform distortion.

## Assembly

For every source preview MP3:

1. download it
2. ffprobe it before use
3. detect usable silence boundaries
4. map semantic speaker transitions for that chunk
5. cut Greg spans from the Greg source and Ithar spans from the Dragon source
6. concatenate those local spans back into the exact chunk order

Then concatenate completed chunks in canon order.

Assembly should:

- normalize technical format only as necessary
- preserve generated speech timing inside selected spans
- use only intentional seam silence
- avoid blanket dramatic pauses between chunks
- append approximately **2 seconds of settling silence** at chapter end
- encode the final chapter MP3
- ffprobe and decode-verify the finished asset
- record duration, byte size, and SHA-256

A seam is successful when the chapter sounds like one continuous performance rather than stitched source files.

## Canon fidelity

The ordered chunk transcripts must reproduce the chapter text exactly, excluding only non-spoken Markdown headings and production metadata.

Production-only speaker labels, chunk numbers, timing maps, and comments are never spoken and never render publicly.

Do not rewrite canon prose merely to make synthesis easier. A wording change belongs at canon authority.

## Website publication

Each record page keeps its prose and chapter audio together.

The separate Listening Archive remains the audio-first library.

Do not expose a playable chapter audio element until the assembled MP3 has passed decode verification. Partial captures remain internal production material.

## Superseded methods

The following are not current production methods:

- full-chapter Greg render + full-chapter Ithar render + post-hoc slicing
- one synthesis request for every tiny speaker turn
- pitch-shifted or slowed Dragon by default
- one mixed-speaker render used as the final two-voice performance
- long generated audio substituted for the short-take factory merely because it exists

## Current application

Records 002 and 003 are the first chapters after Record 001 to use this short dual-render authority from capture through publication.

## Verified production frontier

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

These are technical production facts, not a substitute for human listening judgment about aesthetic seam quality.

The assembler supports explicit `workflow_dispatch` in addition to push triggers so a verifier receipt committed by GitHub Actions can be assembled without manufacturing an unrelated follow-up change solely to retrigger the workflow.
