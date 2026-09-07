# Persistent Four-Act Search Runtime Addendum

**Status:** approved experimental correction

**Branch:** `architecture/long-form-story-compiler`

**Extends:** `2026-09-07-ai-native-long-form-story-compiler-design.md`

## Purpose

Preserve the current long-form experiment as four persistent temporal search channels while adding conservative shared communication between them.

The experiment is intentionally not a pool of disposable generic frontiers and not four independent manuscript writers.

It is:

```text
ACT I persistent local search  \
ACT II persistent local search  \
ACT III persistent local search ---> SHARED STORY STATE <--> STORY SYNC / REHEARSAL
ACT IV persistent local search  /
```

Each act keeps local speculative working memory and continues searching throughout the run. Shared state carries only cross-act constraints and discoveries mature enough to matter globally.

## Core rule

**Invent freely inside an act. Promote conservatively across acts.**

Local act state is permissive. Shared story state is conservative.

No later-act requirement automatically rewrites an earlier act. No earlier-act consequence automatically dictates a later event. The receiving act must test whether the constraint can be earned naturally from its accumulated local reality.

## Persistent channels

The current experiment requires exactly four persistent channels:

- `act-i`
- `act-ii`
- `act-iii`
- `act-iv`

Each channel owns derived, rebuildable local working state such as:

- competing possibilities
- local rehearsal discoveries
- act-specific unresolved questions
- local speculative facts
- local constraint responses
- ideas not yet trusted globally

A channel is not canon and is not a separate manuscript authority.

The scheduler may vary compute allocation, but it must give every persistent act a baseline opportunity to continue searching during each scheduling epoch.

## Shared story state

Shared state is the communication surface between persistent channels. It remains derived editorial state and should reuse existing STORY SYNC authority rather than duplicating it.

It may carry:

- promoted discoveries
- repeated signals / strong threads / story truths
- cross-act contradictions
- forward consequences
- backward requirements
- major character / relationship state
- unresolved shared questions
- hidden-canon implications
- reader-state implications
- provenance and superseded assumptions

Shared state must remain more conservative than local state.

## Story IR / delta contract

Act workers return small structured deltas rather than replacing whole acts or the whole book.

Useful delta classes include:

- local possibility
- local rehearsal discovery
- local unresolved question
- shared discovery evidence
- forward consequence
- backward requirement
- contradiction
- constraint response

Every delta preserves source act, stable ID, provenance, dependencies where relevant, and the authority effect it is allowed to have.

Parallel act workers remain derived-only. Shared integration is serialized and conflict checked.

## Bidirectional obligations

A later act may emit a backward requirement, for example:

```text
source: act-iv
target: act-i
requirement: an earlier reciprocal obligation must exist for this payoff to land
```

The target act receives this as a probe, not an instruction.

It may respond:

- `supported`: local reality can naturally earn it
- `conflict`: local reality resists it
- `third_path`: a different setup could satisfy both sides
- `reject_source`: the later candidate should probably adapt instead
- `untested`: more search / rehearsal is required

Forward consequences use the same principle in the opposite direction.

Unresolved disagreement must remain visible to STORY SYNC / REHEARSAL rather than being silently averaged away.

## Constraint closure

Constraint closure means testing whether cross-act obligations can coexist with the accumulated local realities.

It does **not** mean forcing all constraints to close.

When an obligation collides with a target act, preserve the collision and schedule higher-value work around it. Possible outcomes include:

- earlier story adapts
- later story adapts
- a third solution emerges
- candidate dies
- explicit canon revision is requested if accepted canon is implicated

## Scheduler

The scheduler is intentionally non-starving for this experiment.

Every scheduling epoch includes baseline local-search work for all four acts.

Extra compute may be allocated to:

- major contradictions
- forward/backward constraint collisions
- high-value relationship transitions
- book-shaping discoveries
- unresolved high-heat REHEARSAL questions
- candidate endings with strong support
- strong threads needing adversarial testing

This baseline requirement is experimental. Do not optimize it away until evidence shows persistent act-local search is not useful.

## Rehearsal and sync

REHEARSAL remains shared story laboratory. Any act may submit candidates, and discoveries may affect the shared state rather than returning only to the source act.

STORY SYNC remains the owner of discovery maturity and divergence-preserving convergence.

The persistent-act runtime must call / consume existing STORY SYNC behavior rather than implementing a second promotion system.

## Creator taste

Creator taste remains a search heuristic only. It may influence extra rehearsal/search allocation inside an already viable act channel, but cannot remove the baseline search opportunity from another act or override story / character / causal authority.

Creator-surprise lanes remain valid counter-pressure.

## Success criterion

The first experiment asks:

> Can four persistent temporal regions of the same book dream toward one another until REHEARSAL and STORY SYNC cause their local possibilities to converge into one coherent story?

Do not replace this topology with generic dynamic frontiers before the experiment produces evidence that the persistent channels are unnecessary.
