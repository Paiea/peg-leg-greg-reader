# Persistent Four-Act Convergence Design

**Status:** approved experimental architecture

**Branch:** `architecture/long-form-story-compiler`

**Purpose:** preserve four persistent temporal search channels while using shared Story IR, STORY SYNC, bidirectional constraints, and REHEARSAL as communication/convergence machinery between them.

## 1. Experimental question

The first long-form experiment is intentionally unusual:

> Can four persistent temporal regions of the same book effectively dream toward one another until STORY SYNC and REHEARSAL cause their local possibilities to converge into one coherent story?

Do not optimize this property away before the experiment produces evidence.

## 2. Persistent topology is an invariant

The orchestration layer must preserve exactly four persistent act-local search channels for this experiment:

- ACT I
- ACT II
- ACT III
- ACT IV

These are not temporary frontiers and are not replaced by a generic dynamic frontier pool.

Every act retains its own local speculative working memory and receives some baseline opportunity to continue searching even when another act currently contains stronger discoveries.

The scheduler may allocate extra compute unevenly, but it must not starve an act entirely.

## 3. Local Act State

Each act owns a permissive, speculative working state.

Local Act State may contain:

- competing possibilities
- local rehearsal discoveries
- act-specific unresolved questions
- local relationship or character hypotheses
- provisional setup/payoff ideas
- speculative causal routes
- local contradictions
- ideas that are useful to keep exploring but are not yet globally trusted

Local state is deliberately allowed to be messy.

**Core rule: Invent freely inside an act. Promote conservatively across acts.**

An idea existing in ACT III local state does not make it shared story truth.

## 4. Shared Story State

Shared Story State is conservative and cross-act.

It may contain:

- promoted discoveries
- strong threads / story truths
- accepted cross-act constraints
- forward consequences
- backward obligations
- major relationship state
- major character state
- shared causal dependencies
- contradictions requiring cross-act attention
- reader-state / hidden-canon obligations when relevant

Shared state is communication authority for the search process, not final prose authority.

Canon prose remains final story authority once accepted.

## 5. Bidirectional constraint traffic

### Forward consequences

Earlier acts may emit consequences that constrain later acts.

Example:

ACT I establishes a costly promise. Shared Story State records the consequence. ACT II–IV must account for that promise or explicitly challenge the assumption through STORY SYNC.

### Backward requirements

Later acts may discover promising payoffs or transformations and emit requirements toward earlier acts.

Example:

ACT IV discovers a powerful ending payoff requiring an earlier trust fracture. That requirement is sent to ACT I or ACT II as a candidate obligation.

The receiving act does **not** simply obey it.

It tests whether its accumulated local reality can naturally support the requirement.

If not, preserve the disagreement.

REHEARSAL / STORY SYNC should then determine whether:

- the earlier story adapts
- the late payoff adapts
- a third solution emerges
- the candidate dies

Constraints are proposals and pressures until earned by evidence and promotion.

## 6. Constraint closure

A cross-act constraint collision is a first-class search target.

Closure may occur when:

- both sides become mutually compatible
- one side adapts
- a third branch resolves the conflict
- a candidate is invalidated
- accepted canon makes one side impossible

Do not average contradictory local possibilities into mush.

Preserve the disagreement until evidence justifies resolution.

## 7. Scheduling policy

Every act receives a baseline search allocation each scheduling cycle.

Extra compute may be allocated toward:

- major contradictions
- forward/backward constraint collisions
- high-value relationship transitions
- book-shaping discoveries
- important REHEARSAL uncertainty
- candidate endings with strong support

The exact numerical budget is an execution policy and may change during experimentation.

The invariant is that baseline act-local search remains nonzero for all four acts.

Creator-taste search priors, convergence confidence, and other heuristics may redistribute **extra** attention but may not eliminate a persistent act channel.

## 8. STORY SYNC role

STORY SYNC is the conservative cross-act communication layer.

It should:

- inspect local act outputs
- promote only sufficiently supported discoveries into Shared Story State
- route forward consequences and backward requirements
- identify cross-act contradictions
- request targeted REHEARSAL where evidence is weak or contradictory
- preserve viable divergence
- record constraint-closure status

It should not:

- replace act-local working memory
- select one act as the only active frontier
- convert every local idea into shared truth
- silently rewrite accepted canon

## 9. REHEARSAL role

REHEARSAL pressure should rise where local and shared realities disagree.

High-value targets include:

- cross-act causal collisions
- relationship transitions whose earlier and later versions do not connect cleanly
- candidate endings that require unsupported earlier state
- major discoveries with insufficient challenge evidence
- cases where two acts imply incompatible character behavior

REHEARSAL returns evidence. STORY SYNC decides whether evidence is strong enough to alter shared state.

## 10. Minimal first implementation

The first executable slice should add only:

1. explicit four-act local state representation
2. shared story state representation
3. forward consequence and backward requirement records
4. cross-act constraint collision reporting
5. baseline-per-act scheduling allocation
6. bonus heat allocation for high-value cross-act targets
7. tests proving no act can be starved
8. tests proving late-act backward requirements do not automatically mutate earlier local state
9. tests proving local discoveries do not become shared truth merely because they exist
10. integration with existing STORY SYNC report without creating a second canon authority

Do not add generic dynamic frontiers in this slice.

## 11. Success criteria

The experiment is correctly preserved when:

- all four act channels remain present and searchable throughout the run
- each act can hold unresolved local possibilities independently
- cross-act discoveries communicate through explicit shared constraints rather than direct mutation
- later acts can pressure earlier acts without commanding them
- earlier acts can constrain later acts through forward consequences
- collisions remain inspectable until resolved
- extra compute follows important evidence while every act retains baseline search
- creator taste and convergence heuristics influence scheduling but cannot collapse the four-channel topology

## Core principle

**Four persistent local dreamers. One conservative shared story. Bidirectional pressure between them. Evidence earns convergence.**
