# Greg, Again — Audio Production Protocol

This file owns parallel audio-production coordination for R2 / Greg, Again.

It does **not** replace `r2/PIPELINE.md`. The pipeline owns Shared Greg Surface, Audio Finish, processing space, POV, and medium-specific repair. This file owns worker routing, claiming, provider submission, verification, publication, and handoff.

## Default worker behavior

A fresh audio worker should not ask the human which chapters it owns unless GitHub state is genuinely ambiguous.

If the human did not explicitly assign a range, the worker must:

1. inspect current `main`
2. read root `AGENTS.md`
3. read `r2/PIPELINE.md`
4. read this file
5. inspect `greg-again/audio/manifest.json`
6. inspect current Greg, Again written authority / written frontier
7. inspect live Greg, Again audio branches and open PRs
8. compute the earliest available contiguous batch
9. create the claim branch
10. verify the claim still does not overlap newer work
11. only then begin synthesis

Current GitHub authority outranks chat history and stale handoff text.

## Default batch size

The default auto-claimed batch is **3 chapters**.

A worker may claim a smaller tail batch when fewer than 3 written chapters are available before the written frontier.

Do not skip an earlier free chapter merely to create prettier multiples of three.

A worker that has explicitly been assigned a different non-overlapping range may honor that assignment after checking current GitHub state.

## Protocol-native claim branches

New automatic claims use:

`audio/greg-again-batch-NNN-MMM`

Examples:

- `audio/greg-again-batch-012-014`
- `audio/greg-again-batch-015-017`
- `audio/greg-again-batch-018-020`

Creating the branch is the claim operation.

A protocol-native worker must not begin voice synthesis until its claim branch exists.

If branch creation fails because the ref already exists, refresh GitHub state and compute the next available batch. Never force-update or overwrite the existing claim.

## What counts as unavailable

A chapter is unavailable when any of the following is true:

- it is already published in the current `greg-again/audio/manifest.json`
- it is covered by an existing protocol-native batch claim whose unpublished chapters have not been explicitly released
- a live pre-protocol Greg, Again audio branch clearly owns that chapter
- an open Greg, Again audio PR clearly owns that chapter
- other current durable WIP makes ownership clear

When ownership is genuinely ambiguous, avoid overlap rather than maximizing batch size.

Never claim beyond the current authoritative written frontier.

## Transitional compatibility

Audio workers already running before this protocol remain valid.

Existing per-chapter branches such as:

`audio/greg-again-ch8-evidence-before-certainty`

reserve their exact chapter while that work remains live or unpublished.

Do not rename, restart, absorb, or regenerate those workers merely to normalize branch naming.

At protocol adoption time, Chapters 8–11 already had separate live ownership signals. New workers should respect whatever the newest GitHub state shows rather than assuming those exact chapters remain current forever.

## No automatic stealing

A worker must never:

- delete another worker's claim branch
- force-update another worker's claim branch
- assume an apparently idle branch is abandoned
- steal work because a PR is slow
- regenerate published chapters to normalize production history

An abandoned or mistaken claim requires explicit release or reassignment by the human or a clearly authorized integration worker.

## Working inside a claimed batch

The claim defines ownership, not a requirement to finish all chapters in one giant transaction.

Within a 3-chapter batch, produce and verify chapters sequentially enough that each completed chapter can cross a durable boundary. A worker may prepare later chapters while provider jobs for an earlier chapter are processing, but it must not let partial preparation overwrite newer story or audio authority.

For every owned chapter:

1. resolve the current authoritative Shared Greg Surface / written source
2. apply current `r2/PIPELINE.md` Audio Finish doctrine
3. preserve current narrator / voice / pronunciation authority
4. split into provider-safe performance takes only as needed
5. generate voice takes
6. assemble the chapter audio
7. verify text coverage, take order, seams, playability, title, duration, and route
8. reconcile shared catalog / manifest files against newest GitHub authority
9. publish the verified chapter durably

Do not redesign settled audio philosophy merely because a worker owns several chapters.

## Provider queueing

Voice-generation jobs are independent production work when their transcripts are already locked.

Queue multiple independent provider-safe takes without unnecessary serial waiting when the available voice tool permits it.

Within a claimed batch, the worker may also prepare or submit later owned chapter takes while earlier owned chapter jobs are processing, provided:

- exact transcript-to-take mapping is preserved
- chapter ownership is already claimed
- provider quota / rate limits are respected
- no wording is changed merely to make queueing easier
- completed output can still be traced deterministically to chapter and take

Provider throttling, serialization, or quota exhaustion does not release chapter ownership.

The current short-take / stitched workflow remains valid. Do not pay a regeneration tax merely to make older chapters match a newer provider convenience.

## Shared-file reconciliation

Parallel workers may all eventually need shared files such as:

- `greg-again/audio/manifest.json`
- R2 audio/catalog routing
- reader chapter audio metadata

Immediately before modifying a shared file:

1. refresh current `main`
2. inspect newer neighboring audio merges
3. preserve every valid newer entry
4. add or change only the current worker's owned chapters

Never restore a stale whole-file copy over newer audio publication.

A worker may merge current `main` into its branch or otherwise reconcile according to repository workflow before publication.

## Verification

For every published chapter verify at minimum:

- source text is fully represented with no accidental omission
- no source segment is duplicated at take seams
- take order is correct
- audio is playable
- pronunciation authority is preserved
- chapter number and title match current reader/catalog authority
- duration metadata is recorded when required
- manifest/catalog entries point to the correct artifact
- neighboring workers' chapters were not overwritten

When one local take fails, prefer repairing the smallest responsible take rather than regenerating the whole chapter.

## Completion authority

Published entries in `greg-again/audio/manifest.json` are the durable proof that audio chapters are complete.

A historical claim branch may remain after merge. Its existence does not make already-published chapters unfinished.

For any unpublished chapter still covered by an unreleased claim, preserve that ownership until explicit release or completion.

## Handoff

At the end of a batch, report compactly:

- claimed range
- completed / published chapters
- any chapter still in progress
- provider quota / throttling issue, if any
- branch / PR / merge state
- next available range only if current GitHub state makes it clear

Then leave the normal repository handshake.

## Minimal fresh-chat starter

> Continue Greg, Again audio production from current GitHub authority.
>
> Auto-claim the next available audio batch using `r2/AUDIO_PRODUCTION.md`, then produce, verify, publish, and leave the next handshake.
>
> Preserve newer authority and do not overlap another worker.

A fresh worker should derive its actual chapter range from GitHub rather than asking the human to assign it.
