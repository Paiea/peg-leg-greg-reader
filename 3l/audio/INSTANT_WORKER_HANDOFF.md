# 3L FIVE-INSTANT-WORKER HANDOFF

Use this handoff only after the generated five-worker work order exists and passes validation.

Current branch:

`3l/dialogue-territory-rebuild-002-010`

Current authority:

`3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md`

## Coordinator dispatch

Open five separate Instant-worker chats/tasks.

Give each worker the same base instruction below, changing only `WORKER_NUMBER` from 1 through 5.

Do not give one worker two worker numbers.

Do not let workers share or rebalance captures.

## Copy/paste worker prompt

```text
Continue 3L short-take audio capture in:

Paiea/peg-leg-greg-reader

Branch:
3l/dialogue-territory-rebuild-002-010

You are Instant audio capture worker WORKER_NUMBER of 5.

Your job is mechanical production only. Do not edit prose, routing, chunking, voices, architecture, assembly, or publication.

Read and obey:

1. 3l/audio/PARALLEL_INSTANT_WORKER_AUTHORITY.md
2. 3l/audio/SHORT_TAKE_PRODUCTION_AUTHORITY.md
3. 3l/audio/workers/records-002-003-instant-WORKER_NUMBER-work-order.json

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

3l/audio/workers/records-002-003-instant-WORKER_NUMBER-captures.json

Follow the exact return schema in PARALLEL_INSTANT_WORKER_AUTHORITY.md.

Your return manifest must account for every assigned capture as success or explicit failure.

Do not touch another worker's files.
Do not assemble audio.
Do not publish audio.
Do not modify the master work order.
Do not claim chapter completion.

Finish your entire assigned slice in this run as far as the available tools allow.
```

## Worker-specific files

Worker 1 reads:

`3l/audio/workers/records-002-003-instant-1-work-order.json`

and writes:

`3l/audio/workers/records-002-003-instant-1-captures.json`

Worker 2 reads:

`3l/audio/workers/records-002-003-instant-2-work-order.json`

and writes:

`3l/audio/workers/records-002-003-instant-2-captures.json`

Worker 3 reads:

`3l/audio/workers/records-002-003-instant-3-work-order.json`

and writes:

`3l/audio/workers/records-002-003-instant-3-captures.json`

Worker 4 reads:

`3l/audio/workers/records-002-003-instant-4-work-order.json`

and writes:

`3l/audio/workers/records-002-003-instant-4-captures.json`

Worker 5 reads:

`3l/audio/workers/records-002-003-instant-5-work-order.json`

and writes:

`3l/audio/workers/records-002-003-instant-5-captures.json`

## Coordinator after return

Do not manually splice together worker prose or trust a worker summary.

Reconcile the five JSON receipt manifests against:

`3l/audio/records-002-003-five-worker-work-order.json`

The coordinator then owns:

- exact coverage audit
- duplicate/stale capture rejection
- URL/download verification
- ffprobe
- semantic span extraction from `deep` / `normal` sources
- chunk assembly
- chapter assembly
- approximately 2-second settling tail
- final decode/hash verification
- website publication

The five workers are a capture factory, not five co-authors.
