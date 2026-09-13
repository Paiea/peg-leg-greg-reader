# 3L FIVE-INSTANT-WORKER HANDOFF

Use this after `3l/audio/records-002-010-five-worker-work-order.json` exists on `main` and the frontier tests are green.

## Dispatch

Open five separate Instant chats. Give each worker the same prompt below, changing only `WORKER_NUMBER` to 1, 2, 3, 4, or 5.

Do not combine worker numbers and do not let workers rebalance assignments.

## Copy/paste worker prompt

```text
Continue 3L short-take audio capture in:

Paiea/peg-leg-greg-reader

Branch:
main

You are Instant audio capture worker WORKER_NUMBER of 5.

Your job is mechanical production only. Do not edit prose, routing, chunking, voices, architecture, assembly, or publication.

Read and obey:

1. 3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md
2. 3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md
3. 3l/audio/workers/records-002-010-instant-WORKER_NUMBER-work-order.json

The worker work-order JSON is your executable capture list.

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

Write ONLY your assigned return manifest:

3l/audio/workers/records-002-010-instant-WORKER_NUMBER-captures.json

Follow the exact return schema in PARALLEL_INSTANT_WORKER_AUTHORITY.md.

Your return manifest must account for every assigned capture as success or explicit failure.

Commit that one return manifest to main.

Do not touch another worker's files.
Do not assemble audio.
Do not publish audio.
Do not modify the master work order.
Do not claim chapter completion.

Finish your entire assigned slice in this run as far as the available tools allow.
```

## What happens after the five chats

You do not need to manually sort the returned URLs.

When all five worker manifests exist on `main`, `.github/workflows/3l-parallel-worker-pipeline.yml` automatically reconciles the receipts, verifies the preview MP3s, assembles every complete record, refreshes the record pages and Listening Archive, commits the verified audio frontier, and requests a Pages rebuild.

If a worker has a failed capture, only the affected record stays in `Audio rebuild in production`; verified written records remain published.
