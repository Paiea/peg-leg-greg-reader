# 3L PARALLEL INSTANT WORKER AUTHORITY

Status: **CURRENT FIVE-WORKER CAPTURE AUTHORITY**

This file governs parallel Instant-model audio capture for the current 3L written frontier.

It is subordinate to canon manuscript authority, `3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md`, the current frozen master work order, and the generated short-dual plans.

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

Workers own only automatic slot claiming, exact capture execution, and receipt recording.

## Stable dispatch pointer

Every worker starts from:

`3l/audio/CURRENT_INSTANT_WORK_ORDER.json`

That file identifies the current frozen run and contains:

- `master_work_order`
- `run_label`
- `source_sha`
- `worker_count`
- `work_order_template`
- `return_manifest_template`
- `claim_template`

Workers must not hard-code a worker number and must not ask the user for one.

## Automatic slot claim

All five chats receive the same prompt.

Each worker claims exactly one slot using create-only GitHub file creation on `main`.

1. Read `3l/audio/CURRENT_INSTANT_WORK_ORDER.json` from `main`.
2. Read the referenced `master_work_order` and verify that its `source_sha`, `run_label`, and `worker_count` match the pointer.
3. Consider slots `1, 2, 3, 4, 5` in that order.
4. For each candidate slot, resolve the pointer templates with the exact current `source_sha`, `run_label`, and slot number.
5. If that slot's return manifest already exists on `main`, skip the slot.
6. Attempt to create the resolved claim path using create-only semantics. Never update or overwrite a claim file.
7. If claim creation succeeds, that slot is yours. Stop scanning immediately.
8. If creation fails because the claim path already exists, continue to the next slot.
9. If creation fails only because `main` moved during the write, refresh `main` and retry the same candidate slot once. After refresh, if the claim path exists, continue to the next slot.
10. If no slot can be claimed, stop without generating audio and report that the current five-worker run is already fully claimed or completed.

The claim path is namespaced by the frozen run's `source_sha`, so claims from a later regenerated frontier do not collide with this run.

### Claim file schema

A successful worker writes exactly one claim file before any voice generation:

```json
{
  "status": "claimed",
  "worker_id": "instant-3",
  "slot": 3,
  "source_sha": "<exact pointer source_sha>",
  "run_label": "<exact pointer run_label>",
  "work_order": "<resolved work_order_template>",
  "return_manifest": "<resolved return_manifest_template>"
}
```

Do not invent timestamps, chat identifiers, or user metadata. The claim exists only to guarantee exclusive slot ownership.

## Current frozen run

Repository:

`Paiea/peg-leg-greg-reader`

Branch workers write to:

`main`

The current master path and worker slice paths are resolved through `3l/audio/CURRENT_INSTANT_WORK_ORDER.json`.

Each worker reads exactly the slice for the slot it successfully claimed. The slice is executable authority and already contains every exact capture call.

## Voice contract

- `deep` = Greg identity
- `normal` = Ithar / Dragon identity
- tempo = 1.0
- pitch shift = 0
- formant shift = 0
- no Dragon DSP

Workers may not choose another voice or alter performance settings.

## Capture contract

For every object in the claimed worker slice `captures` array:

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

Each `(record, chunk_index, voice)` tuple belongs to exactly one frozen worker slice. A worker owns only the slice whose slot it successfully claimed.

Workers may not claim a second slot, regenerate another worker's capture, rebalance assignments, or modify another worker's files.

The master work order is validated for complete coverage, whole-chunk ownership, zero overlap, and near-equal capture load before dispatch.

## Allowed writes

A worker may write only two files for the current frozen run:

1. its own create-only claim file resolved from `claim_template`
2. its own return manifest resolved from `return_manifest_template`

Workers must not edit manuscripts, plans, routing files, authority, scripts, workflows, final MP3s, website files, the current pointer, the master work order, another worker's claim, or another worker's return manifest.

## Return manifest schema

```json
{
  "status": "complete",
  "worker_id": "instant-3",
  "work_order": "<resolved claimed work-order path>",
  "source_sha": "<copied from work order>",
  "assigned_capture_count": 52,
  "successful_capture_count": 52,
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

Actual worker ID and assigned counts come from the claimed worker work order. Do not copy the example values blindly.

If any capture fails after the exact retry, top-level status becomes `partial`, the failed assignment remains represented, and `failures` contains concise evidence.

## Worker completion

A worker is finished only when every assigned capture in its claimed slice is represented as success or explicit failure and its one resolved return manifest is committed to `main`.

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

If a worker claims a slot and then cannot finish its slice, do not have a normal worker overwrite or steal that claim. Recovery should be a separate bounded retry/release action so duplicate captures cannot be created accidentally.
