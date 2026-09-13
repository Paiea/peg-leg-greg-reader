# Record 001 Long-Turn Dragon v3 Recipe

Status: experimental listening candidate. The 26-block past-tense recapture has been assembled and mechanically verified, but still requires human listen-back before promotion.

## Why this exists

The mixed-speaker splice experiment duplicated dialogue because semantic text ownership was mapped onto approximate waveform boundaries. This version removes that failure mode entirely by generating speaker-pure clips first and joining them with explicit pause metadata.

## Performance rule

Write and capture speaker-pure audio.

- Greg narration and Greg dialogue use `deep`.
- Dragon uses `fancy`.
- Greg narration, action, observation, and internal framing use past tense.
- Direct dialogue keeps the tense natural to what the speaker is saying.
- Dragon should speak in fewer, longer turns where the scene allows it.
- Preserve short exchanges when they materially improve the scene.
- Never generate one audio clip containing both Greg and Dragon.

The current performance source remains 26 dramatic blocks. Technical capture chunks exist only to satisfy preview-size limits and do not change the dramatic block structure.

## Dragon treatment

Apply one deterministic transform to every Dragon clip:

- pitch: `-3.25` semitones
- pitch ratio: `0.8288406503840438`
- tempo: `1.0`
- formant: `preserved`
- rubberband quality mode: `pitchq=quality`

Greg receives no pitch or tempo treatment.

## Pause policy

Pauses are assembler metadata, not punctuation tricks.

- same-speaker technical chunk continuation: `80 ms`
- ordinary turn change: approximately `220-320 ms`
- deliberate Dragon silence / stare: approximately `450-700 ms`
- major reveal beat: approximately `900-1400 ms`
- final settling tail: `2000 ms`

Pause values can be adjusted later without regenerating voice captures.

## Capture rule

For each generated clip:

- use the full speaker-pure chunk as `transcript`
- use the identical text as `preview_transcript`
- keep each technical chunk preview-safe, approximately 500 characters or less
- use `deep` for Greg and narration
- use `fancy` for Dragon before deterministic pitch treatment

The current past-tense build uses 37 technical captures across the same 26 dramatic blocks.

### Block 019

Block 019 is still one dramatic block, but it contains two speaker-pure technical clips:

1. Greg narration: `The dragon went still.` followed by an `80 ms` continuation pause.
2. Dragon speech: `When?` followed by the block's `800 ms` dramatic pause.

This preserves the prose/block structure without putting narrator text in the Dragon voice or generating a mixed-speaker take.

## Current reproducible files

- performance source: `3l/performance/record-001.audio-v3-long-turn.md`
- exact past-tense capture binding + pauses: `3l/audio/experiments/record-001-past-26block-v3-captures.json`
- deterministic assembler: `scripts/build_3l_past_26block_candidate.py`
- build workflow: `.github/workflows/3l-record-001-past-26block.yml`
- listening candidate: `3l/assets/audio/record-001-past-26block-v3.mp3`
- verification receipt: `3l/audio/verification/record-001-past-26block-v3.json`
- experiment branch: `3l/record-001-clean-speaker-v2`
- successful workflow run: `34742919726`

The older `record-001-long-turn-v3.mp3` and its original capture manifest are pre-tense historical artifacts and are not the current listening candidate.

## Verified past-tense build shape

- narration tense: past
- 26 dramatic blocks
- 37 speaker-pure technical captures
- 12 Dragon turns
- 15 Fancy Dragon technical chunks
- 22 Deep Greg technical chunks
- 0 mixed-speaker clips
- 0 waveform speaker-boundary inference
- Dragon pitch: `-3.25` semitones
- Dragon tempo: `1.0`
- candidate duration: `588.912` seconds
- candidate SHA256: `51e11df69f862bd5224ea1832480d58013215c7244d13f1c107a9f5e1cdd3627`

The GitHub workflow verified the manifest shape, downloaded all 37 exact captures, assembled the candidate, decoded the result successfully, and wrote the verification receipt. A separate local check of the downloaded artifact reproduced the same duration, byte size, and SHA256 and decoded the MP3 without errors.

If listen-back succeeds, this pattern should become the starting production shape for future 3L records. If it fails, keep it labeled as an experiment and change the performance layer before promoting more infrastructure.
