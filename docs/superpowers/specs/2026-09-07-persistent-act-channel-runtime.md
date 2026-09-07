# Persistent Four-Act Search Runtime Addendum

**Status:** approved experimental correction

**Branch:** `architecture/long-form-story-compiler`

**Extends:** `2026-09-07-ai-native-long-form-story-compiler-design.md`

## Purpose

Preserve the current long-form experiment as four persistent temporal search channels while adding conservative shared communication between them.

The experiment is intentionally not a pool of disposable generic frontiers and not four independent manuscript writers.

It is one story trajectory through time:

```text
ONE STORY TRAJECTORY

[ ACT I ] [ ACT II ] [ ACT III ] [ ACT IV ]
    ^         ^          ^          ^
    |         |          |          |
 persistent local temporal search in every slab
    \_________ bidirectional constraints _________/
                 SHARED STORY STATE
              STORY SYNC + REHEARSAL
```

Each act keeps local speculative working memory and continues searching throughout the run. Shared state carries only cross-act constraints and discoveries mature enough to matter globally.

The system is solving for a coherent whole-book trajectory, not merely predicting the next chapter.

## Core rule

**Invent freely inside an act. Promote conservatively across acts.**

Local act state is permissive. Shared story state is conservative.

No later-act requirement automatically rewrites an earlier act. No earlier-act consequence automatically dictates a later event. The receiving act must test whether the constraint can be earned naturally from its accumulated local reality.

## Persistent temporal slabs

The current experiment requires exactly four persistent channels:

- `act-i`
- `act-ii`
- `act-iii`
- `act-iv`

Each channel is a persistent temporal slab of the same evolving story trajectory.

Every slab maintains an approximate:

```text
STATE IN
LOCAL SEARCH SPACE
STATE OUT
```

`STATE IN` describes what must, probably should, or might plausibly be true when entering that region.

`STATE OUT` describes what must, probably should, or might plausibly be true when leaving that region.

Boundary conditions may initially be uncertain and may contain competing local beliefs. They evolve as adjacent and distant acts discover stronger structure.

An act's job is not simply to generate scenes. Its job is to discover compelling lived trajectories that can transform its current STATE IN into a credible STATE OUT.

Each channel owns derived, rebuildable local working state such as:

- competing possibilities and local belief status
- state-in hypotheses
- state-out hypotheses
- local rehearsal discoveries
- act-specific unresolved questions
- local speculative facts
- local constraint responses
- provisional relationship / character states
- ideas not yet trusted globally

A channel is not canon and is not a separate manuscript authority.

The scheduler may vary compute allocation, but it must give every persistent act a baseline opportunity to continue searching during each scheduling epoch.

## Boundary negotiation

Adjacent act boundaries are explicit negotiation surfaces.

The STATE OUT of one slab and STATE IN of the next do not have to agree immediately.

Example:

```text
ACT II STATE OUT candidate:
heroine no longer trusts the guild

ACT III STATE IN candidate:
heroine relies on the guild politically
```

This is a `boundary contradiction`, not something to smooth over with generic connective prose.

The runtime should surface the contradiction and request search / REHEARSAL around the missing transition.

Possible resolutions include:

- earlier boundary adapts
- later boundary adapts
- a transitional state emerges
- one branch dies
- disagreement remains open pending evidence

Boundary states should gradually stabilize as the whole trajectory converges.

## Shared story state

Shared state is the communication surface between persistent channels. It remains derived editorial state and should reuse existing STORY SYNC authority rather than duplicating it.

It may carry:

- promoted discoveries
- repeated signals / strong threads / story truths
- cross-act contradictions
- boundary contradictions
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

- local possibility / belief update
- state-in hypothesis
- state-out hypothesis
- local rehearsal discovery
- local unresolved question
- shared discovery evidence
- forward consequence
- backward requirement
- contradiction
- boundary response
- constraint response

Every delta preserves source act, stable ID, provenance, dependencies where relevant, confidence where relevant, and the authority effect it is allowed to have.

Parallel act workers remain derived-only. Shared integration is serialized and conflict checked.

## Local beliefs, not premature global certainty

Each act may maintain several competing local beliefs.

Conceptually:

```text
ACT II local belief
branch A: plausible
branch B: plausible
branch C: weakening
branch D: rehearsal contradicted
```

Do not require a single global version immediately.

The architecture is message-passing-like rather than formal probabilistic belief propagation:

```text
local act belief
-> consequence / requirement / contradiction message
-> target act updates local search pressure
-> REHEARSAL produces evidence
-> STORY SYNC updates shared confidence
-> revised constraints flow again
```

Do not implement mathematical belief propagation unless later evidence shows it would materially help.

## Bidirectional obligations and long-range messages

Information flow is not restricted to neighboring slabs.

A later act may emit a backward requirement, for example:

```text
source: act-iv
target: act-i
requirement: an earlier reciprocal obligation must exist for this payoff to land
confidence: provisional
provenance: act-iv ending rehearsal
```

The target act receives this as a probe, not an instruction.

It may respond:

- `supported`: local reality can naturally earn it
- `conflict`: local reality resists it
- `third_path`: a different setup could satisfy both sides
- `reject_source`: the later candidate should probably adapt instead
- `untested`: more search / rehearsal is required

Forward consequences use the same principle in the opposite direction.

ACT I may constrain ACT IV directly when a foundational rule or choice has long-range consequences. ACT IV may pressure ACT I directly when a promising payoff requires an early prerequisite.

Unresolved disagreement must remain visible to STORY SYNC / REHEARSAL rather than being silently averaged away.

## Forward and backward compilation

Every persistent slab can participate in both directions.

Forward pass asks:

> Given this region's current state and discoveries, what consequences or opportunities should later temporal regions inherit?

Backward pass asks:

> Given this region's promising payoff or transformation, what conditions should earlier temporal regions establish?

ACT I may naturally produce more forward consequences and ACT IV more backward requirements, while ACT II / III may do substantial work in both directions. These are tendencies, not hard-coded rules.

## Constraint closure

Constraint closure means testing whether cross-act obligations and boundary conditions can coexist with the accumulated local realities.

It does **not** mean forcing all constraints to close.

When an obligation or boundary collides with a target act, preserve the collision and schedule higher-value work around it. Possible outcomes include:

- earlier story adapts
- later story adapts
- a third solution emerges
- candidate dies
- explicit canon revision is requested if accepted canon is implicated

## REHEARSAL as trajectory execution test

A globally attractive trajectory can still require false character behavior.

Whenever two temporal constraints imply an uncertain behavioral bridge, REHEARSE it instead of interpolating vaguely.

Example:

```text
ACT II boundary:
she still distrusts him

ACT III desired state:
they operate as an intimate team
```

Do not resolve this with `relationship gradually improves`.

Treat the missing transformation as a search problem. REHEARSAL should attempt actual behavior under pressure and report what intermediate state, if any, emerges naturally.

REHEARSAL is therefore a local execution / test environment for proposed sections of the whole temporal trajectory.

## Cross-direction agreement

When independent temporal slabs discover compatible structure, increase attention without automatically promoting truth.

Example:

- ACT I independently creates pressure toward hiding a strange ability after public attention becomes dangerous.
- ACT IV independently needs a late reveal that the true scale of that ability was concealed.

That temporal agreement is useful evidence that the compiler may have found part of the real thread.

STORY SYNC still owns promotion authority. Cross-direction agreement primarily earns more testing / rehearsal attention.

## Scheduler

The scheduler is intentionally non-starving for this experiment.

Every scheduling epoch includes baseline local-search work for all four acts.

Extra compute may be allocated to:

- major contradictions
- boundary contradictions
- forward/backward constraint collisions
- cross-direction agreement worth pressure-testing
- high-value relationship transitions
- book-shaping discoveries
- unresolved high-heat REHEARSAL questions
- candidate endings with strong support
- strong threads needing adversarial testing

This baseline requirement is experimental. Do not optimize it away until evidence shows persistent act-local search is not useful.

## Rehearsal and STORY SYNC

REHEARSAL remains the shared story laboratory. Any act may submit candidates, and discoveries may affect shared state rather than returning only to the source act.

STORY SYNC remains the owner of discovery maturity and divergence-preserving convergence.

The persistent-act runtime must call / consume existing STORY SYNC behavior rather than implementing a second promotion system.

## Temporal consistency / convergence

Convergence should be measured as increasing compatibility across the whole temporal trajectory, not merely by completing four outlines.

Useful convergence signals include:

- adjacent STATE OUT / STATE IN boundaries increasingly agree
- long-range setup/payoff requirements are satisfied naturally
- forward consequences reach believable later states
- backward requirements find plausible earlier causes
- fewer major boundary contradictions remain
- relationship trajectories require fewer unexplained jumps
- character transformations contain plausible intermediate states
- later candidates require fewer retroactive repairs
- repeated passes across all four channels produce increasingly compatible versions of the same overall trajectory

Do not invent a heavy numerical optimizer yet. Produce a small inspectable temporal-consistency report first.

## Creator taste

Creator taste remains a search heuristic only. It may influence extra rehearsal/search allocation inside an already viable act channel, but cannot remove the baseline search opportunity from another act or override story / character / causal authority.

Creator-surprise lanes remain valid counter-pressure.

## Success criterion

The first experiment asks:

> Can four persistent temporal perspectives develop local story realities, repeatedly exchange causal and prerequisite information, and converge on one dramatically alive trajectory through the whole novel?

Do not replace this topology with generic dynamic frontiers, one global planner, or stateless act workers before the experiment produces evidence that the persistent temporal slabs are unnecessary.

## Core principle

Do not ask only:

**What happens next?**

Also ask:

**What must have happened before?**

And ultimately:

**What whole trajectory through these four temporal regions can satisfy both directions while remaining dramatically alive?**
