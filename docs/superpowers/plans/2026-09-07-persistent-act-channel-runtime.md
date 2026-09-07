# Persistent Four-Act Runtime Implementation Plan

**Goal:** Add the smallest executable runtime that preserves four persistent temporal slabs of one shared story trajectory while using existing STORY SYNC as the conservative shared convergence layer.

## Constraints

- Exactly four persistent channels for this experiment: `act-i` through `act-iv`.
- Each act maintains approximate `state_in`, local search, and `state_out` boundary hypotheses.
- Local act state is permissive and derived.
- Shared story state is conservative and derived.
- No local act can directly promote itself to story truth.
- No backward/forward obligation automatically mutates another act.
- Adjacent boundary mismatches are explicit contradictions, not silently smoothed prose.
- Long-range messages may skip acts in either temporal direction.
- Every scheduling epoch gives all four act channels baseline search work.
- Extra scheduling pressure may target boundary contradictions, cross-act obligation collisions, cross-direction agreement, high-value relationships, book-shaping discoveries, candidate endings, and high-heat rehearsal uncertainty.
- Reuse `story_sync_engine.py`; do not duplicate discovery authority.
- Preserve creator-taste work as a search signal only.
- Measure convergence primarily as temporal compatibility, not four-outline completion.

## Task 1: RED runtime contracts

Create `tests/test_persistent_act_runtime.py` covering:

1. runtime requires all four persistent act channels
2. every act contains `state_in`, local working memory, and `state_out`
3. local possibilities remain local after integration
4. Act IV backward requirement appears in Act I packet without rewriting Act I local state
5. Act I forward consequence may target Act IV directly
6. adjacent incompatible `state_out` / `state_in` boundaries surface as a boundary contradiction
7. uncertain behavioral bridges are returned as REHEARSAL targets instead of generic interpolation
8. conflicting constraint response stays unresolved and becomes high-priority work
9. independent cross-direction agreement increases search attention without becoming truth
10. scheduler always emits baseline work for all four acts, including convergence
11. extra work is added for collisions without starving baseline work
12. shared discovery maturity is delegated to existing STORY SYNC
13. local act memories remain distinct while packets share promoted global state
14. temporal-consistency report improves as boundary/obligation conflicts close

Run focused test and confirm RED because the runtime module does not exist.

## Task 2: Minimal runtime module

Create `scripts/persistent_act_runtime.py` with:

- schemas / validators for runtime, act slabs, boundary hypotheses, shared messages, and act deltas
- `compile_act_packet(runtime, act_id)`
- `integrate_deltas(runtime, deltas)` returning a new derived runtime snapshot
- `boundary_contradictions(runtime)`
- `constraint_closure(runtime)`
- `temporal_consistency(runtime)`
- `schedule_work(runtime)`
- `sync_shared_story(runtime)` delegating to `story_sync_engine.sync_story`

Keep data structures JSON-serializable and inspectable. Do not implement formal probabilistic belief propagation.

## Task 3: AI-facing integration

Extend `scripts/plg_ai_tools.py` minimally with one derived-only entry point that can run a persistent-act runtime cycle from an object/path and return:

- shared STORY SYNC report
- four compiled act packets
- non-starving work schedule
- boundary contradictions
- current constraint-closure report
- temporal-consistency report

Do not add canon-writing behavior.

## Task 4: Dragon Spotter bounded fixture

Create a small `state/experiments/dragon-spotter/persistent-act-runtime/` fixture with:

- four persistent temporal slabs with explicit state-in/state-out hypotheses
- current first-bargain / reciprocity material as shared discoveries where supported
- at least one Act IV backward requirement targeting Act I
- at least one Act I forward consequence targeting a distant later act
- one adjacent boundary contradiction
- one unresolved cross-act collision
- one cross-direction agreement signal

Use it only to prove communication/convergence behavior, not to finalize story events.

## Task 5: Verification

Run focused persistent-act runtime tests plus STORY SYNC / creator-taste tests and the full repository unit suite through CI.

Leave PR #161 draft / unmerged unless separately authorized.
