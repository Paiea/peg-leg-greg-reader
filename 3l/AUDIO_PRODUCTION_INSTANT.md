# 3L Audio Production — Instant Path

Status: active production protocol for future 3L records after the prose/performance plan is approved.

## Purpose

Make routine 3L audio production boring enough for Instant.

Normal Chat owns story judgment, prose, speaker ownership, performance structure, and any unusual delivery decisions. Instant is the production worker. It should not redesign the scene while generating audio.

## Locked voice contract

- Greg narration: `deep`
- Greg dialogue: `deep`
- Ithar / Dragon dialogue: `normal`
- Dragon DSP: none
- Tempo: natural
- No mixed-speaker TTS captures
- `transcript` and `preview_transcript` must be identical for every technical capture
- Use the public `preview_url` returned by AI Voice Generator as the assembly asset
- Do not depend on the AI Doc Maker full-audio page. Full files require an authenticated browser session and are not available to GitHub Actions.

## Authority chain

1. **Canon manuscript**
   - Story authority.
   - Example: `3l/manuscript/record-001.md`

2. **Audio plan**
   - Production authority for speaker ownership, dramatic runs, technical chunks, and pauses.
   - Must be derived only after the manuscript is approved.
   - Future records should store this explicitly as data. Do not infer speakers during capture.

3. **Capture ledger**
   - Ordered one-to-one list of public preview assets for the plan's technical chunks.
   - A capture ID is complete only when AI Voice Generator returns `status: ready` and a public `preview_url`.
   - Retry only missing/failed capture IDs. Never regenerate the whole record because one capture failed.

4. **Assembler receipt**
   - Mechanical proof of what was built: source hash, plan hash, asset count, verified asset count, duration, byte size, and output SHA256.

5. **Listening approval**
   - The generated file is experimental until listened to.
   - Do not replace public/canon audio solely because the workflow is green.

## Production sequence

### Phase A — Freeze the creative source

Before generating any voice:

- manuscript is approved for the listening test;
- speaker ownership is explicit;
- Greg/Dragon voice mapping is locked;
- dramatic pauses are defined;
- no prose editing occurs during routine capture.

If any of those are unresolved, stop production and return to Normal Chat.

### Phase B — Build the audio plan

The plan should contain, at minimum:

```json
{
  "record": "002",
  "source_path": "3l/manuscript/record-002.md",
  "source_sha256": "...",
  "greg_voice": "deep",
  "dragon_voice": "normal",
  "dragon_dsp": "none",
  "final_tail_ms": 2000,
  "chunks": [
    {
      "id": "001",
      "dramatic_run": 1,
      "part_in_run": 1,
      "voice": "deep",
      "text": "...",
      "pause_after_ms": 80
    }
  ]
}
```

### Dramatic run vs technical chunk

These are deliberately different concepts.

A **dramatic run** is one continuous speaker turn in the performance. Ithar may hold the floor for one or two minutes.

A **technical chunk** exists only because the public preview capture surface is roughly 30 seconds. Split a long dramatic run into preview-safe chunks, normally <= 430 characters, at natural sentence boundaries.

Technical splits must not change the dramatic structure.

Default seam policy:

- same dramatic run continuation: 80 ms
- ordinary run / speaker boundary: 280 ms
- deliberate larger beat: encode explicitly in the plan, normally 450–1000 ms
- final settling tail: 2000 ms

## Phase C — Instant capture loop

Instant should do exactly this:

1. Read the approved plan.
2. Read the current capture ledger.
3. Compute missing chunk IDs.
4. For each missing ID:
   - use `voice_id = chunk.voice`;
   - send the full `chunk.text` as `transcript`;
   - send the exact same `chunk.text` as `preview_transcript`;
   - require `status: ready`;
   - record the returned public preview asset immediately.
5. Do not recapture IDs already present unless explicitly asked.
6. When ledger count equals plan chunk count, hand off to assembly.

The worker should report progress as `captured / total`, not narrate every implementation detail.

## Phase D — Generic assembly

Use:

`python scripts/assemble_3l_preview_audio.py`

The assembler owns only mechanical work:

- require asset count == plan chunk count;
- require unique asset IDs;
- download public preview MP3s;
- reject missing/tiny/non-decoding files;
- ffprobe every source;
- normalize every source to mono 44.1 kHz PCM before concatenation;
- insert plan-defined pauses;
- add final tail;
- encode the final MP3;
- write a receipt with hashes, counts, size, and duration.

The assembler must never infer a speaker or modify prose.

## Phase E — Verification gate

A production run is mechanically complete only when fresh verification proves:

- every planned chunk has a public asset;
- every public asset downloads;
- every source decodes;
- final audio decodes;
- receipt says `asset_count == verified_asset_count`;
- final duration > 0;
- final byte size > 0;
- final SHA256 exists.

A green workflow proves mechanical integrity, not artistic approval.

## Phase F — Listen and promote

Listen to the complete assembled record.

Classify findings as:

- **PROSE** — wording/headspace/story issue; return to Normal Chat and invalidate affected chunks.
- **PERFORMANCE PLAN** — wrong speaker boundary or pause; update plan and rebuild only affected captures if text changes.
- **VOICE CAPTURE** — bad take/pronunciation; recapture only affected chunk IDs.
- **ASSEMBLY** — seam/level/file problem; fix assembler without rewriting prose.

Only after listen-back approval should the file be promoted to public/site authority.

## Do not repeat the Record 001 dead ends

- Do not scrape AI Doc Maker full-audio pages in GitHub Actions.
- Do not wait on authenticated full-file URLs.
- Do not use approximate waveform timing to separate mixed speakers.
- Do not generate mixed-speaker source takes.
- Do not use pitch/tempo treatment for Ithar. Raw `normal` is the current Dragon voice.
- Do not manually redesign the chapter while running routine captures.
- Do not regenerate already-good chunks when one chunk fails.

## Record 001 exception

Record 001 predates the explicit-plan rule and has a temporary reproducible parser:

`scripts/derive_3l_record_001_preview_plan_v6.py`

That parser is intentionally chapter-specific. Do **not** extend it into a book-wide speaker-inference engine.

For Record 002 onward, create the explicit audio plan as part of the approved performance pass.

## Instant handoff prompt

Use a prompt like this for routine production:

> Continue 3L audio production for Record N from current repository authority. Read `3l/AUDIO_PRODUCTION_INSTANT.md`. Do not redesign prose, voices, speaker ownership, or pauses. Resolve the approved audio plan and current capture ledger. Generate only missing capture IDs with `transcript == preview_transcript` and the plan's voice. Record each returned public preview asset immediately. When the ledger is complete, run the generic assembler, verify the receipt and final MP3, and report exact failed IDs if anything blocks completion.

## Design principle

**Normal Chat decides what the performance is. Instant manufactures the approved performance. GitHub Actions proves the manufactured file is mechanically valid. Human listening decides whether it is good.**
