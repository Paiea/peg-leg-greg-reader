# 3L PARALLEL INSTANT WORKER AUTHORITY

Status: **CURRENT FIVE-WORKER CAPTURE AUTHORITY**

This file governs parallel Instant-model audio capture for the current 3L written frontier, Records 002–010.

It is subordinate to canon manuscript authority, `3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md`, and the frozen generated short-dual plans.

## Purpose

Five Instant workers perform repetitive synthetic voice capture. They are production labor, not editors or architects.

The coordinator owns:

- canon prose
- Dragon territory and speaker routing
- chunk boundaries
- worker partitioning
- reconciliation
- verification
- assembly
- publication

Workers own only exact capture execution and receipt recording.

## Current frozen run

Repository:

`Paiea/peg-leg-greg-reader`

Branch workers write to:

`main`

Master work order:

`3l/audio/records-002-010-five-worker-work-order.json`

Worker slices:

- `3l/audio/workers/records-002-010-instant-1-work-order.json`
- `3l/audio/workers/records-002-010-instant-2-work-order.json`
- `3l/audio/workers/records-002-010-instant-3-work-order.json`
- `3l/audio/workers/records-002-010-instant-4-work-order.json`
- `3l/audio/workers/records-002-010-instant-5-work-order.json`

Each worker reads exactly one slice. The slice is executable authority and already contains every exact capture call.

## Voice contract

- `deep` = Greg identity
- `normal` = Ithar / Dragon identity
- tempo = 1.0
- pitch shift = 0
- formant shift = 0
- no Dragon DSP

Workers may not choose another voice or alter performance settings.

## Capture contract

For every object in the worker slice `captures` array:

1. call the approved AI voice generator
2. pass the exact `transcript`
3. pass the exact same text as `preview_transcript`
4. use the exact listed `voice`
5. record the returned receipt before continuing

Do not add labels, directions, SSML, pauses, annotations, or rewritten punctuation.

A successful capture records:

- record
- chunk index
- voice
- exact transcript
- exact preview transcript
- context ID
- preview URL
- full audio URL when returned
- generator status
- worker status `success`

The preview URL is the preferred assembly source.

## Retry rule

If a generator call fails without a usable receipt, one exact retry is allowed with the same transcript and voice.

If the retry also fails, record that assignment as failed and continue. Never substitute another voice or altered text.

## Ownership

Each `(record, chunk_index, voice)` tuple belongs to exactly one worker. Workers may not claim, regenerate, rebalance, or modify another worker's assignment.

The master work order is validated for complete coverage, whole-chunk ownership, zero overlap, and near-equal capture load before dispatch.

## Allowed write

Each worker may write only its own return manifest:

- instant-1 → `3l/audio/workers/records-002-010-instant-1-captures.json`
- instant-2 → `3l/audio/workers/records-002-010-instant-2-captures.json`
- instant-3 → `3l/audio/workers/records-002-010-instant-3-captures.json`
- instant-4 → `3l/audio/workers/records-002-010-instant-4-captures.json`
- instant-5 → `3l/audio/workers/records-002-010-instant-5-captures.json`

Workers must not edit manuscripts, plans, routing files, authority, scripts, workflows, final MP3s, or website files.

## Return manifest schema

```json
{
  "status": "complete",
  "worker_id": "instant-1",
  "work_order": "3l/audio/workers/records-002-010-instant-1-work-order.json",
  "source_sha": "<copied from work order>",
  "assigned_capture_count": 53,
  "successful_capture_count": 53,
  "failed_capture_count": 0,
  "captures": [
    {
      "record": "002",
      "chunk_index": 1,
      "voice": "deep",
      "transcript": "<exact work-order transcript>",
      "preview_transcript": "<same exact text>",
      "context_id": "<returned id>",
      "preview_url": "<returned playable preview URL>",
      "audio_url": "<returned full-audio URL when available>",
      "generator_status": "<returned status>",
      "status": "success"
    }
  ],
  "failures": []
}
```

Actual assigned counts come from each worker work order. Do not copy the example count blindly.

If any capture fails after the exact retry, top-level status becomes `partial`, the failed assignment remains represented, and `failures` contains concise evidence.

## Worker completion

A worker is finished only when every assigned capture is represented as success or explicit failure and its one return manifest is committed to `main`.

Workers do not assemble or publish audio and do not claim chapter completion.

## Automatic coordinator pipeline

When worker return manifests land on `main`, `.github/workflows/3l-parallel-worker-pipeline.yml` waits until all five expected manifests exist. It then:

1. validates each return against its frozen assignment
2. reconciles successful captures by record
3. downloads, decodes, ffprobes, and hashes every returned preview source
4. writes record verification receipts
5. assembles every record whose required captures are complete
6. records the exact current plan SHA in each finished audio audit
7. regenerates record pages and the Listening Archive
8. exposes audio only when the asset and audit match the current plan
9. commits the verified frontier to `main`
10. requests a GitHub Pages rebuild

A stale MP3 with the correct filename is not publishable. The reader requires a verified audit matching the current plan hash.

## Failure behavior

If one worker returns a failed capture, the pipeline may verify the other captures but that affected record remains incomplete and its current written page stays published with `Audio rebuild in production` instead of stale audio.

The coordinator can later issue a bounded retry for only the missing capture.
