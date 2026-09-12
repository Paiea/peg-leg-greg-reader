# R2 Codex Audio Efficiency Overlay

This file applies only when Codex is working on R2 / Greg, Again audio production or audio-pipeline implementation.

It overlays `r2/PIPELINE.md` and `r2/AUDIO_PRODUCTION.md`. It does not replace or rewrite their story, audio, claiming, synthesis, assembly, or publication semantics.

## Core rule

R2 audio may use parallel production at the project level without turning one Codex session into a multi-agent swarm.

Default Codex posture:

**one primary Codex agent -> one bounded audio target -> verify -> stop**

Do not spawn Codex subagents unless the Mana task packet explicitly sets `PARALLELISM: YES`.

## Distinguish the three kinds of parallelism

### 1. Project-level worker parallelism

Several independently launched workers may own different chapters when current audio-production authority allows it.

This is external orchestration. It does not imply that one Codex session should create those workers internally.

### 2. Provider / take parallelism

Inside one claimed chapter, independent short voice takes may be queued or submitted concurrently when the provider permits it.

This is provider-job concurrency. It is not Codex-agent concurrency.

### 3. Codex subagent parallelism

This is OFF by default for R2 audio.

Authorize it only when independent sidecar work clearly saves more than its duplicated context/reconciliation cost. Examples might include two non-overlapping audits of separate scripts or independent checks with mechanically reconcilable outputs.

Do not authorize subagents for:
- understanding one audio pipeline
- producing one chapter
- resolving one authority question
- editing overlapping manifests/scripts
- architecture/product discovery
- work where one result blocks the next

## Context loading

For a bounded R2 audio task, normally load only:

1. root `AGENTS.md`
2. `state/editorial/CODEX_EXECUTION_POLICY.md`
3. `state/CODEX_TASK_PACKET.md`
4. `r2/PIPELINE.md`
5. `r2/AUDIO_PRODUCTION.md`
6. this overlay
7. exact source/state/scripts required by the target

For Audio Score v2, add only the relevant current Audio Score docs such as `r2/AUDIO_SCORE.md`, `r2/AUDIO_SCORE_PRODUCTION.md`, and `r2/AUDIO_PRONUNCIATION.md` when synthesis/pronunciation requires them.

Do not preload unrelated manuscript, reader, visual, or editorial brains merely because they exist.

## Efficiency rules

- Prefer existing deterministic scripts/indexes/state resolution over rediscovering repository layout.
- Use targeted searches and file ranges instead of dumping large files or logs.
- Preserve successful expensive synthesis when downstream deterministic plumbing fails.
- During implementation, run the smallest useful check first; run the broader relevant verification at the durable boundary.
- Do not start another chapter, repair, refactor, or pipeline improvement after the approved target verifies.

## Handoff

Return compact evidence to Mana:

- target completed or blocked
- files/state changed
- verification performed
- expensive artifacts preserved
- one or two constraints that matter for the next decision

Then stop.
