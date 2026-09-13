# Record 001 Long-Turn Dragon v3 Recipe

Status: experimental listening candidate. Do not promote to main authority until listen-back approval.

## Why this exists

The mixed-speaker splice experiment duplicated dialogue because semantic text ownership was mapped onto approximate waveform boundaries. This version removes that failure mode entirely.

## Performance rule

Write and capture speaker-pure audio.

- Greg narration and Greg dialogue use `deep`.
- Dragon uses `fancy`.
- Dragon should speak in fewer, longer turns.
- Between Dragon turns, use Greg reaction, silence, staring, head movement, eye movement, posture, or other nonverbal scene behavior instead of unnecessary one-line ping-pong.
- Preserve short exchanges when they materially improve the scene, but do not make them the default rhythm.
- Never generate a take containing both Greg and Dragon.

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

These values can be adjusted later without regenerating voice captures.

## Capture rule

The dramatic performance has 26 blocks. Preview-size limits split some long blocks into technical chunks, producing 36 total captures.

Technical chunks never cross a speaker boundary. When one dramatic turn requires multiple captures, concatenate the same-speaker chunks with the 80 ms continuation pause.

For capture, use identical `transcript` and `preview_transcript` text so the downloadable preview MP3 is the exact source used in assembly.

## Record 001 production corrections

The capture manifest is authoritative for this experiment where it differs from the prose spike:

- Block 006 does not claim the Dragon already knows about the horse.
- Block 007 begins with Greg's body and Line explanation. Horse material remains later in Block 016.
- `The dragon goes still.` is Greg-owned nonverbal narration at the end of Block 018.
- Block 019 contains only the Dragon speech `When?`.

## Files

- performance spike: `3l/performance/record-001.audio-v3-long-turn.md`
- exact capture binding + pauses: `3l/audio/experiments/record-001-long-turn-v3-captures.json`
- deterministic assembler: `scripts/build_3l_long_turn_candidate.py`
- disposable build workflow: `.github/workflows/3l-record-001-long-turn-v3.yml`
- listening candidate: `3l/assets/audio/record-001-long-turn-v3.mp3`
- verification receipt: `3l/audio/verification/record-001-long-turn-v3.json`

## Verified build shape

- 26 dramatic blocks
- 36 speaker-pure capture files
- 12 Dragon turns
- 17 Fancy Dragon technical chunks
- 19 Deep Greg technical chunks
- 0 mixed-speaker clips
- 0 waveform speaker-boundary inference

If listen-back succeeds, this pattern should become the starting production shape for future 3L records. If it fails, keep it labeled as an experiment and change the performance layer before building more infrastructure.
