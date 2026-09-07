# Persistent Four-Act Runtime Implementation Plan

**Goal:** Add the smallest executable runtime that preserves four persistent act-local search channels while using existing STORY SYNC as the conservative shared convergence layer.

## Constraints

- Exactly four persistent channels for this experiment: `act-i` through `act-iv`.
- Local act state is permissive and derived.
- Shared story state is conservative and derived.
- No local act can directly promote itself to story truth.
- No backward/forward obligation automatically mutates another act.
- Every scheduling epoch gives all four act channels baseline search work.
- Extra scheduling pressure may target contradictions, cross-act obligation collisions, high-value relationships, book-shaping discoveries, and high-heat rehearsal uncertainty.
- Reuse `story_sync_engine.py`; do not duplicate discovery authority.
- Preserve creator-taste work as a search signal only.

## Task 1: RED runtime contracts

Create `tests/test_persistent_act_runtime.py` covering:

1. runtime requires all four persistent act channels
2. local possibilities remain local after integration
3. Act IV backward requirement appears in Act I packet without rewriting Act I local state
4. Act I forward consequence appears in later target packet
5. conflicting constraint response stays unresolved and becomes shared contradiction / high-priority work
6. scheduler always emits baseline work for all four acts
7. extra work is added for constraint collisions without starving baseline work
8. shared discovery maturity is delegated to existing STORY SYNC
9. local act memories remain distinct while packets share promoted global state

Run focused test and confirm RED because the runtime module does not exist.

## Task 2: Minimal runtime module

Create `scripts/persistent_act_runtime.py` with:

- schemas / validators for runtime, local act state, shared obligations, and act deltas
- `compile_act_packet(runtime, act_id)`
- `integrate_deltas(runtime, deltas)` returning a new derived runtime snapshot
- `constraint_closure(runtime)`
- `schedule_work(runtime)`
- `sync_shared_story(runtime)` delegating to `story_sync_engine.sync_story`

Keep data structures JSON-serializable and inspectable.

## Task 3: AI-facing integration

Extend `scripts/plg_ai_tools.py` minimally with one derived-only entry point that can run a persistent-act runtime cycle from an object/path and return:

- shared STORY SYNC report
- four compiled act packets
- non-starving work schedule
- current constraint-closure report

Do not add canon-writing behavior.

## Task 4: Dragon Spotter bounded fixture

Create a small `state/experiments/dragon-spotter/persistent-act-runtime/` fixture with:

- four persistent act channels
- current first-bargain / reciprocity strong-thread material as shared discoveries where supported
- at least one Act IV backward requirement
- at least one Act I forward consequence
- one unresolved cross-act collision

Use it only to prove communication/convergence behavior, not to finalize story events.

## Task 5: Verification

Run focused persistent-act runtime tests plus STORY SYNC / creator-taste tests and the full repository unit suite through CI.

Leave PR #161 draft / unmerged unless separately authorized.
