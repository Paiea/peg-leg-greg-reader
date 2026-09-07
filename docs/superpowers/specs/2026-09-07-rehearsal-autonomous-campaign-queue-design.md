# Autonomous REHEARSAL Campaign Queue Design

## Purpose

Carry the approved high-authority REHEARSAL calibration from canon 061 through 491 without requiring a chat session to supervise every ten-chapter batch.

The queue is an execution mechanism over the existing REHEARSAL lane. It does not create a new story authority or editorial doctrine.

## Core architecture

Use the repository's existing Codex campaign execution policy as the creative worker layer and the existing deterministic REHEARSAL return runner as the only prose-write path.

The sequence is strictly serial:

`061-070 -> 071-080 -> ... -> 481-490 -> 491`

Each batch begins from the settled branch authority produced by the preceding batch. No later batch may precompute against stale source authority.

## Batch worker contract

For each batch, the worker must:

1. Read exact current chapter HTML for the batch plus only the neighboring/contextual material required to preserve continuity.
2. Reuse fresh PERFORMANCE/REHEARSAL evidence and relationship memory where valid.
3. Rehearse at the approved 051-060 boundary-hunt heat.
4. Allow SOURCE WIN. There is no edit quota.
5. Emit a schema-bound discovery/result artifact and, only for surviving prose candidates, an exact-source return manifest.
6. Never mutate prose directly.
7. Hand the manifest to the existing `scripts/apply_rehearsal_returns.py` production gate.
8. Advance the queue only after the batch's prose application and repository validation settle green.

## Approved heat

The 061-491 campaign deliberately keeps the high calibration rather than cooling automatically.

Unlocked local surfaces may include:

- substantial short-exchange rewriting
- dialogue expansion or contraction
- interruption and overlap
- withheld or redirected answers
- changed local response order
- silence
- who closes an exchange
- scene-local blocking
- task continuation and object behavior
- reaction placement
- character-specific phrasing and rhythm
- plausible actor entrances/exits when locked reality permits them
- freer Nico private cognition, with the novelizer retaining only what improves first-person prose

Hard locks remain absolute:

- plot outcome
- established facts
- knowledge boundaries
- causality
- chronology
- economics
- earned competence
- injury/mobility/physical state
- major earned relationship milestones
- unresolved mystery state

## Boundary-hunt evidence

This campaign is intentionally testing where high rehearsal authority becomes harmful. The worker must preserve compact evidence when a take is rejected for being too hot.

Failure labels include:

- `overacted_theatre`
- `quip_inflation`
- `gratuitous_interruption`
- `prop_recursion`
- `movement_saturation`
- `overcompression`
- `character_caricature`
- `pov_crowding`
- `useful_repetition_destroyed`
- `cast_expansion_rejected`

A rejected hot take is evidence, not a reason to silently lower the global heat. Future batches stay at the approved heat unless a separate editorial decision changes calibration.

Repeated words, objects, or gestures are not failures merely because they repeat. Preserve repetition when it escalates irritation, pressure, rhythm, fixation, or payoff.

## Actor entrance rule

A character absent from source choreography is not automatically forbidden from a rehearsal.

Treat a new presence as an `actor_entrance_proposal`. Reject it only when locked geography, chronology, simultaneous state, knowledge, or another hard fact makes the presence impossible, or when the novel critic finds that the entrance harms the scene enough not to survive editorial return.

Truth is constrained. Staging is negotiable.

## Casting namespace safety

Canon character Kellan and the synthetic actor historically named Kellan must never be conflated. Until the synthetic actor registry is explicitly recast/renamed, manifests should identify the Jorren performer by role-safe identity such as `Jorren actor` rather than bare `Kellan`.

## Writable surfaces

Discovery categories such as `speaker_legibility` and `relationship_behavior` are evidence categories, not writable prose surfaces.

Return manifests must name actual writable surfaces such as:

- `dialogue`
- `paragraphing`
- `movement`
- `blocking`
- `silence`
- `interaction_timing`
- `reaction_placement`
- `object_handling`
- `local_exchange_shape`
- `tone`
- `internal_dialogue`
- `narration_rhythm`
- `attention_order`
- `sensory_emphasis`
- `memory_intrusion`

## Exact-source rule

Rendered or semantic beat boundaries are never trusted as literal storage boundaries.

Before a manifest is eligible for application, its `before` anchor must be materialized from literal current chapter HTML. No fuzzy matching. A mismatch stops that batch.

## Queue state

Persist one compact queue state artifact under `state/editorial/rehearsal/queue/` containing:

- schema/version
- target branch
- campaign range 061-491
- batch size 10
- current/next batch
- settled authority SHA
- status per batch: pending/running/applied/source_win/blocked
- manifest/report paths
- validation result
- retry count
- blocking reason when present

The queue is resumable. A rerun starts from the first non-settled batch and rechecks current authority before work.

## Failure and retry policy

Follow `state/editorial/CODEX_EXECUTION_POLICY.md`:

- retry ordinary worker failure at most once
- do not bypass permissions, quota, authentication, or sandbox boundaries
- do not widen scope
- do not invent new doctrine

Deterministic source mismatch, hard-lock violation, validation failure, or material authority conflict blocks advancement. The queue records the failure and stops rather than skipping ahead.

## Validation gate

A prose-writing batch must pass, in order:

1. schema/manifest validation
2. literal exact-source dry run
3. production apply through `apply_rehearsal_returns.py`
4. changed-chapter/diff-boundary verification
5. hard-surface leakage rejection
6. no-em-dash prose check
7. repository unit tests
8. PERFORMANCE roundtrip reference check
9. Showcase validation
10. `git diff --check`
11. serialized commit/push

A legitimate all-SOURCE-WIN batch records its result and advances without a prose commit after validating that no return manifest is required.

## Cost controls

- ten chapters per worker batch except final 491
- serial canon writes
- reuse fresh derived evidence
- deterministic source extraction before semantic reasoning
- no Best-of-N by default
- no duplicate attempts by default
- targeted second takes only when a concrete weakness warrants them
- compact schema-bound outputs instead of long narrative recaps

## Completion

The campaign is complete only when canon 491 is settled and queue state records every batch 061-491 as `applied` or `source_win`, with no blocked batch and final repository validation green.
