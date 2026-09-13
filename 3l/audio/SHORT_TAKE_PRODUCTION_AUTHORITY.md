# 3L SHORT-TAKE AUDIO PRODUCTION AUTHORITY

Status: **CURRENT PRODUCTION AUTHORITY**

This file governs synthetic audio capture and assembly for 3L. Where an older production note conflicts with this file, this file wins.

## Core rule

3L audio is built from **short, preview-safe takes** and then assembled.

Do not use full-chapter synthesis as the production source. Do not generate a full Greg chapter and a full Ithar chapter and attempt to carve them into the final performance afterward.

The production path is:

**CANON PROSE → SEMANTIC SPEAKER ROUTING → SHORT TAKES → PREVIEW MP3 CAPTURE → CANON-ORDER ASSEMBLY → VERIFY → PUBLISH**

Canon prose remains the story authority.

## Take size

Target natural takes of roughly **20–29 seconds**.

For the current voice generator, keep each submitted take **preview-safe**, normally no more than about **500 characters**.

The take does not need to reach 29 seconds. Speaker ownership and a clean semantic boundary are more important than filling the time limit.

Preferred boundaries, in order:

1. paragraph boundary
2. complete dialogue turn
3. complete sentence
4. clause boundary only when necessary

Do not split mid-sentence merely to make takes equal length.

## Speaker purity

Every generated take has exactly **one audio identity**.

Current identities:

- **GREG VOICE** → `deep`
- **DRAGON VOICE / ITHAR** → `normal`

Narration always belongs to Greg, including narration about Ithar.

All remembered characters also remain Greg's audio identity unless a later authority explicitly changes the cast model.

When the semantic speaker changes, end the current take and start another take even when this produces a short take.

Never put Greg/narrator words into a Dragon take. Never put Ithar's spoken words into a Greg take.

## Generator contract

For every production capture:

- `transcript` and `preview_transcript` must be **identical**
- the complete submitted text must fit within the preview-safe limit
- capture the returned playable `preview_url`
- record the voice identity, canon anchor, take index, and preview URL in the production ledger
- the preview MP3 is the assembly source

Do not treat a long-form `audio_url` as the canonical assembly source when the corresponding production take was designed around preview capture.

## Dragon treatment

Current Ithar production profile:

- voice = `normal`
- tempo = **1.0**
- pitch shift = **0 semitones**
- no formant shift
- no monster DSP

Current Greg production profile:

- voice = `deep`
- tempo = **1.0**
- no post-hoc pitch or formant manipulation by default

Dragon identity comes from prose, semantic speaker ownership, patience, cadence, and turn structure, not waveform distortion.

## Assembly

Download the captured preview MP3s and place them in exact canon order.

Assembly should:

1. ffprobe every source take before use
2. normalize technical format only as necessary for concatenation
3. preserve the generated speech timing inside each take
4. insert only intentional seam silence, not blanket dramatic pauses
5. concatenate in exact canon order
6. append approximately **2 seconds of settling silence** at chapter end
7. encode the final chapter MP3
8. ffprobe/decode-verify the final asset
9. record duration, file size, and SHA-256 in verification output

A seam is successful when it sounds like one continuous reading rather than a playlist of clips.

## Canon fidelity

Take transcripts collectively must reproduce the spoken/narrated chapter text in order.

Production-only speaker labels, take numbers, comments, and beat instructions never render publicly and are never spoken.

Do not rewrite canon prose merely to make synthesis easier. If a pronunciation or synthesis problem requires a wording change, that is a separate editorial decision and must be made at canon authority, not silently inside audio production.

## Website publication

Each record page keeps the written prose and its chapter audio together.

The separate Listening Archive remains the audio-first library.

A record must not show a playable chapter audio element until an assembled chapter MP3 has passed decode verification. Partial captures may be tracked internally but must not masquerade as the finished chapter.

## Superseded methods

The following are not current production methods:

- full-chapter Greg render + full-chapter Ithar render + post-hoc semantic slicing
- pitch-shifted or slowed Dragon by default
- mixed-speaker takes generated with one voice
- long generated audio used merely because it exists when the short-take preview factory is the intended source

## Current application

Records 002 and 003 are the first chapters after Record 001 to use this authority from capture through final publication.
