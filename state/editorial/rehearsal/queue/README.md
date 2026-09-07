# Autonomous REHEARSAL Queue

This directory is the durable execution surface for the serial canon 061-491 REHEARSAL campaign.

## Current boundary

Canon 051-060 settled successfully before this queue becomes eligible to start. The first queue batch is 061-070.

Queue state:

`state/editorial/rehearsal/queue/canon-061-491.json`

Creative worker contract:

`state/editorial/rehearsal/queue/CODEX_REHEARSAL_CAMPAIGN.md`

Worker result schema:

`state/editorial/rehearsal/queue/worker-result.schema.json`

Integration workflow:

`.github/workflows/rehearsal-campaign-queue.yml`

## Start or resume

1. Read the queue state and identify the first non-settled batch.
2. If it is `pending`, use the current settled branch authority as the worker source authority and execute exactly that batch under `CODEX_REHEARSAL_CAMPAIGN.md`.
3. Write the schema-bound result to `state/editorial/rehearsal/queue/current-worker-result.json`.
4. Do not edit chapter prose directly. Committing the worker result triggers the serialized integration workflow.
5. The integration workflow validates the queue edge, compiles literal exact-source returns, runs the existing FREE return gate, validates the repository, commits the surviving prose or SOURCE WIN evidence, and settles exactly one batch.
6. Only after that settlement may the next batch be worked.

## Blocked state

A blocked batch stops the campaign. Never skip ahead.

Ordinary creative-worker failure may be retried once. Exact-source mismatch, hard-lock violation, authority conflict, or repository validation failure requires diagnosis at the blocked batch before any later chapter is rehearsed.

## Important limitation

GitHub Actions is the deterministic integration and queue-advancement layer. It does not invent the creative REHEARSAL take. An authorized model/Codex worker must produce each `current-worker-result.json` under the durable worker contract. Once that result exists, the apply/validation/settlement work runs independently of a chat session.
