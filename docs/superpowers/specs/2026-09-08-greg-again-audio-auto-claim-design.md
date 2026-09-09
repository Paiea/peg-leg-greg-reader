# Greg, Again Audio Auto-Claim Design

## Purpose

Make parallel Greg, Again audio production self-routing so fresh chats do not need manually assigned chapter ranges.

The repository remains the coordination authority. A worker must discover what audio is complete, what audio work is already claimed, and what written chapters exist before it starts synthesis.

## Design goals

- allow several fresh chats to receive the same short starter prompt
- prevent two workers from intentionally producing the same chapter range
- preserve current GitHub authority over stale chat assumptions
- avoid a shared mutable queue file as the primary lock
- keep current proven Greg, Again narration and Audio Finish doctrine unchanged
- preserve existing per-chapter audio branches during transition
- keep human prompting small

## Core coordination model

Use GitHub branches as durable claims.

A new protocol-native batch claim uses:

`audio/greg-again-batch-NNN-MMM`

where `NNN` and `MMM` are zero-padded first and last chapter numbers in the claimed range.

Default batch size is 3 chapters.

Examples:

- `audio/greg-again-batch-008-010`
- `audio/greg-again-batch-011-013`
- `audio/greg-again-batch-014-016`

Branch creation is the claim operation. A worker must not begin synthesis until its claim branch exists.

If creation fails because the branch already exists, the worker refreshes GitHub state and computes the next available batch rather than fighting or overwriting the existing claim.

## Authority inputs

Before claiming work, a worker reads current `main` and resolves:

1. completed audio chapters from `greg-again/audio/manifest.json`
2. current written Greg, Again frontier from current written authority
3. active Greg, Again audio branches
4. active Greg, Again audio pull requests when useful for distinguishing live WIP from historical branches
5. current audio production doctrine, narrator authority, pronunciation authority, and current source chapter surfaces for the range it ultimately owns

The worker must never claim beyond the written frontier.

## Availability algorithm

A chapter is unavailable if any of the following is true:

- it is already published in the current audio manifest
- it is covered by an active protocol-native batch claim branch
- current durable WIP clearly shows another audio worker already producing that exact chapter

The worker scans upward from the first unpublished written chapter and chooses the earliest available contiguous range up to the default batch size of 3.

If fewer than 3 written chapters are available before the written frontier, the worker may claim the smaller tail range.

Do not skip an earlier free chapter merely to create prettier multiples of three.

## Transitional compatibility

Existing audio production branches such as:

`audio/greg-again-ch8-evidence-before-certainty`

remain valid durable WIP and must not be overwritten, renamed, or treated as abandoned merely because they predate this protocol.

A protocol-native worker treats an existing live per-chapter branch as reserving that exact chapter.

Because pre-protocol workers may have received multi-chapter instructions before this protocol existed, a fresh worker must also inspect obvious current WIP/handshake evidence before assuming adjacent chapters are free. When ownership is genuinely ambiguous, prefer avoiding overlap over maximizing batch size.

The protocol applies cleanly to newly claimed work and does not require active workers to restart.

## Claim safety

A worker may create only its own new claim branch.

It must never:

- force-update another worker's claim branch
- delete another worker's branch
- steal an apparently idle claim automatically
- assume silence means abandonment
- regenerate published chapters merely to normalize production history

Abandoned or mistaken claims require explicit release/reassignment by the user or an integration worker with clear authority.

## Production inside a claim

Once a claim is established, the worker owns only that chapter range.

It follows current repository audio authority for:

- primary narrator and voice choice
- Shared Greg Surface
- processing space
- provider-safe take boundaries
- pronunciation
- audio-only repair rules
- assembly
- verification
- publication

Current settled doctrine is not redesigned by the auto-claim feature.

Voice-generation jobs should be queued aggressively when the provider/tool permits independent submissions. Provider throttling, serialization, or quota limits do not change chapter ownership.

## Shared-file integration

The worker may prepare and publish its owned chapter artifacts, but shared files such as the master audio manifest must be reconciled against the newest GitHub authority immediately before modification.

Never replace a newer whole manifest with a stale branch copy.

When neighboring workers have landed newer entries, preserve them and add only the current worker's verified chapters.

The same rule applies to shared reader/audio catalog surfaces.

## Completion

A batch is complete only when its owned chapters have been produced, verified, and durably published or merged according to current repository workflow.

Published manifest entries are the durable completion authority.

The claim branch may remain historically present after merge. Future workers determine availability from published state plus live WIP, not merely from branch-name existence forever.

## Minimal fresh-chat starter

The preferred human prompt is:

> Continue Greg, Again audio production from current GitHub authority.
>
> Auto-claim the next available audio batch using the repository audio production protocol, then produce, verify, publish, and leave the next handshake.
>
> Preserve newer authority and do not overlap another worker.

A fresh worker must derive its actual chapter range from GitHub rather than asking the human to assign it.

## Files to integrate after approval

Implementation should remain small:

- add `state/experiments/greg-again/audio/PRODUCTION.md` as the durable audio production and auto-claim protocol
- update root `AGENTS.md` with a Greg, Again Audio route pointing to that file
- update `state/HANDSHAKE_PROTOCOL.md` with the minimal audio re-prompt

Do not add a queue database, scheduler, daemon, or new application subsystem unless later evidence proves branch-as-claim insufficient.
