# 3L PARALLEL INSTANT WORKER AUTHORITY

Status: **CURRENT FIVE-WORKER CAPTURE AUTHORITY**

This file governs parallel Instant-model audio capture for 3L.

It is subordinate only to:

1. canon manuscript authority
2. `3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md`
3. the frozen generated short-dual plans

If an older worker prompt conflicts with this file, this file wins.

## Purpose

Use five fast workers to perform repetitive synthetic voice capture without giving them editorial or architectural freedom.

The coordinator owns all reasoning-heavy work:

- canon prose
- speaker routing
- Dragon territory
- chunk boundaries
- work partitioning
- reconciliation
- assembly
- verification
- publication

The Instant workers own only **capture execution and receipt recording**.

## Frozen work order

For the current Records 002–003 run, the coordinator generates:

- master: `3l/audio/records-002-003-five-worker-work-order.json`
- worker 1: `3l/audio/workers/records-002-003-instant-1-work-order.json`
- worker 2: `3l/audio/workers/records-002-003-instant-2-work-order.json`
- worker 3: `3l/audio/workers/records-002-003-instant-3-work-order.json`
- worker 4: `3l/audio/workers/records-002-003-instant-4-work-order.json`
- worker 5: `3l/audio/workers/records-002-003-instant-5-work-order.json`

Each worker must read exactly one worker slice.

The worker slice is executable authority. It already contains:

- record number
- chunk index
- exact transcript
- exact preview transcript
- required voice
- chunk semantic spans for audit context
- assigned output receipt path

Workers do not inspect neighboring chunks to infer intent.

## Voice contract

Only two voice identities exist in this run:

- `deep` = Greg identity
- `normal` = Ithar / Dragon identity

Both use normal source timing.

No worker may:

- change tempo
- pitch shift
- formant shift
- add DSP
- select another synthetic voice
- rewrite text to improve pronunciation

If pronunciation is imperfect, capture the assigned source exactly and report it. Pronunciation repair belongs to the coordinator.

## Capture call contract

For every object in the worker slice `captures` array:

1. call the approved voice generator exactly once unless the call errors before producing a usable receipt
2. use `voice` as the generator voice
3. use the exact `transcript`
4. use the exact same text as `preview_transcript`
5. do not add speaker labels, directions, pauses, SSML, comments, or surrounding text
6. record the returned receipt before moving to the next assignment

Expected generator mapping:

- work-order voice `deep` → generator `voice_id="deep"`
- work-order voice `normal` → generator `voice_id="normal"`

A successful receipt should record when returned:

- record
- chunk index
- voice
- exact transcript
- exact preview transcript
- context ID
- preview URL
- full audio URL
- generator status

The playable preview URL is the preferred later assembly source.

## Retry rule

Do not improvise around tool failures.

If a call fails without producing a usable capture receipt:

- one exact retry is allowed
- use the same transcript and same voice
- record the failed attempt if identifying information exists

If the retry also fails:

- mark that capture `failed`
- continue with the remaining assigned captures
- include the failure in the worker return manifest

Do not substitute a different voice, shortened transcript, or altered punctuation.

## Ownership rule

Each `(record, chunk_index, voice)` tuple belongs to exactly one worker.

Workers must not:

- claim unassigned captures
- regenerate another worker's capture
- modify another worker's work order
- modify another worker's return manifest
- rebalance work among themselves

The generated master work order is validated for complete coverage and zero overlap before workers are dispatched.

## Allowed repository writes

A worker may write only its assigned return manifest:

- instant-1 → `3l/audio/workers/records-002-003-instant-1-captures.json`
- instant-2 → `3l/audio/workers/records-002-003-instant-2-captures.json`
- instant-3 → `3l/audio/workers/records-002-003-instant-3-captures.json`
- instant-4 → `3l/audio/workers/records-002-003-instant-4-captures.json`
- instant-5 → `3l/audio/workers/records-002-003-instant-5-captures.json`

Workers may not edit:

- manuscript files
- audio plans
- Dragon routing files
- authority files
- scripts
- workflows
- final MP3 assets
- website files
- the master five-worker work order

## Return manifest schema

Each worker return manifest must be one JSON object shaped like:

```json
{
  "status": "complete",
  "worker_id": "instant-1",
  "work_order": "3l/audio/workers/records-002-003-instant-1-work-order.json",
  "source_sha": "<copied from work order when present>",
  "assigned_capture_count": 17,
  "successful_capture_count": 17,
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

If any capture fails after the allowed exact retry:

- top-level `status` becomes `partial`
- the failed assignment remains represented
- `failures` records record/chunk/voice plus concise tool error evidence

Do not omit failures to make a manifest look complete.

## Completion rule

A worker is finished only when:

- every assigned capture has either a success receipt or an explicit failure entry
- counts reconcile with the work order
- the worker return manifest has been written to its exact assigned path
- no unassigned repository files were changed

Workers do **not** assemble audio.

Workers do **not** publish audio.

Workers do **not** declare Records 002 or 003 complete.

## Coordinator reconciliation

After all five workers return, the coordinator must verify:

1. five expected worker manifests exist
2. every assigned capture appears exactly once
3. no unassigned capture appears
4. transcript and preview transcript exactly equal frozen work-order text
5. voice equals frozen work-order voice
6. successful captures have usable receipt identifiers/URLs
7. failures are explicitly surfaced

Only after reconciliation may the coordinator download/ffprobe sources, assemble semantic spans, append the settling tail, verify final MP3s, and publish.

## Core worker instruction

**Do the calls. Record the receipts. Do not make decisions.**
