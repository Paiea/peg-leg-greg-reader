# 3L FIVE-INSTANT-WORKER HANDOFF

Use this after `3l/audio/CURRENT_INSTANT_WORK_ORDER.json` exists on `main` and the frontier tests are green.

## Dispatch

Open five separate Instant chats and paste the exact same prompt into all five.

Do not assign worker numbers. Do not alter the prompt between chats. Each chat claims its own slot atomically from the current frozen run.

## Copy/paste worker prompt

```text
Continue 3L short-take audio capture in:

Paiea/peg-leg-greg-reader

Branch:
main

You are one of five parallel Instant audio capture workers.

Do not ask the user for a worker number. Claim your worker slot automatically from the repository before generating any audio.

Your job is mechanical production only. Do not edit prose, routing, chunking, voices, architecture, assembly, or publication.

Read and obey:

1. 3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md
2. 3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md
3. 3l/audio/CURRENT_INSTANT_WORK_ORDER.json

AUTOMATIC CLAIM:

- read CURRENT_INSTANT_WORK_ORDER.json from main
- read its referenced master_work_order and verify source_sha, run_label, and worker_count match
- consider candidate slots 1, 2, 3, 4, 5 in order
- for each slot, resolve claim_template, work_order_template, and return_manifest_template using the current source_sha, run_label, and candidate slot
- if that slot's return manifest already exists on main, skip it
- attempt to create the resolved claim file on main using create-only semantics
- never overwrite or update an existing claim
- if claim creation succeeds, that is your worker slot; stop scanning immediately
- if the claim path already exists, continue to the next slot
- if main moved during the create operation, refresh main and retry that same slot once; if the claim now exists, continue to the next slot
- if all five slots are already claimed or completed, stop without generating audio and report that the current run has no unclaimed worker slot

After you successfully claim one slot:

- read ONLY the resolved work-order JSON for your claimed slot
- that work-order JSON is your executable capture list
- do not claim a second slot

For EVERY item in its `captures` array:

- call the AI voice generator
- use the exact `transcript`
- use the exact same text for `preview_transcript`
- if `voice` is `deep`, use voice_id `deep`
- if `voice` is `normal`, use voice_id `normal`
- do not rewrite, shorten, annotate, or add performance directions
- capture the returned context_id, preview_url, audio_url, and generator status
- one exact retry is allowed only if a call fails without a usable receipt
- otherwise continue through your entire assigned list

Write ONLY the return manifest resolved for your claimed slot from return_manifest_template.

Follow the exact return schema in PARALLEL_INSTANT_WORKER_AUTHORITY.md.

Your return manifest must account for every assigned capture as success or explicit failure.

Commit that one return manifest to main.

Other than your create-only claim file and your own return manifest:

- do not touch another worker's files
- do not assemble audio
- do not publish audio
- do not modify the current pointer or master work order
- do not claim chapter completion

Finish your entire claimed slice in this run as far as the available tools allow.
```

## What happens after the five chats

You do not need to number the chats or manually sort their returned URLs.

The claim files guarantee exclusive worker ownership for the frozen `source_sha`. When all five worker manifests exist on `main`, `.github/workflows/3l-parallel-worker-pipeline.yml` automatically reconciles the receipts, verifies the preview MP3s, assembles every complete record, refreshes the record pages and Listening Archive, commits the verified audio frontier, and requests a Pages rebuild.

If a worker has a failed capture, only the affected record stays in `Audio rebuild in production`; verified written records remain published.
