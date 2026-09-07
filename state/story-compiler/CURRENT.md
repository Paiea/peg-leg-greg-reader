# Long-Form Story Compiler — CURRENT

**Status:** canonical continuation trailhead for the active experiment

**Architecture version:** `story-compiler/rehearsal-led-temporal-slabs-v1`

**Authority branch:** `architecture/long-form-story-compiler`

**Implementation authority at capture:** `cc80278a3706cfa3974d556b9f316205cb8cdc51`

**Pull request:** draft PR #161, based on `editor/rehearsal-simulation-engine`

## Core model

The compiler is solving for one dramatically alive story trajectory through time rather than predicting the next chapter. Four persistent temporal perspectives maintain local speculative realities and boundary beliefs. They mainly identify consequential questions worth executing. REHEARSAL is the primary semantic simulation environment where characters actually live through pressures. Forward consequences and backward prerequisites may emerge from performance. STORY SYNC learns from repeated, independent, useful evidence and conservatively updates shared story state. Prose is downstream rendering, not the search engine.

```text
STORY STATE = MEMORY
FOUR ACT CHANNELS = TEMPORAL PERSPECTIVES
REHEARSAL = SEMANTIC COMPUTATION / SIMULATION
STORY SYNC = LEARNING + CONVERGENCE
PROSE = RENDERING
```

## Persistent four-act topology

Exactly four persistent channels remain active for this experiment:

```text
[ ACT I ] [ ACT II ] [ ACT III ] [ ACT IV ]
```

Each keeps derived local state:

- `state_in` boundary hypotheses
- local speculative beliefs / competing trajectories
- unresolved questions
- recent compact rehearsal evidence
- incoming forward consequences
- incoming backward requirements
- `state_out` boundary hypotheses

Every scheduling epoch gives all four a cheap baseline heartbeat. Extra compute follows consequential uncertainty. Do not collapse them into one global planner or stateless workers yet.

## Shared Story IR / global state

Shared state is conservative derived memory, not canon. It carries only cross-act information mature enough to matter globally:

- possibilities and discovery evidence
- SPECULATION → REPEATED SIGNAL → STRONG THREAD → STORY TRUTH maturity
- forward consequences
- backward requirements
- boundary / causal contradictions
- major character and relationship state
- unresolved shared questions
- hidden-canon and reader-state implications
- provenance and superseded assumptions

Local invention does not automatically enter shared truth. Parallel act work remains derived-only; shared integration is serialized and conflict checked.

## Forward compiler rule

Ask:

> Given what this temporal region currently does under pressure, what consequences should later regions inherit or test?

Early REHEARSAL may imply candidate forward consequences such as remembered insults, maintained lies, obligation from gifts, changed reputation, attraction-driven avoidance, secrecy pressure, or learned reliance. Later acts receive these as probes, not commands, and test whether the consequence remains alive.

## Backward compiler rule

Ask:

> Given a promising later payoff, transformation, relationship state, or climax, what earlier conditions does honest performance imply must probably have existed?

Late REHEARSAL may imply candidate backward requirements such as prior betrayal, shared routines, private language, learned trust, old control conflict, specific fear, accumulated resentment, or reciprocal obligation. Earlier acts test whether these arise naturally. A backward implication never becomes truth merely because one late performance suggested it.

## Temporal slabs / boundary states

Every act is a temporal slab with approximate:

```text
STATE IN
LOCAL SEARCH / REHEARSAL QUESTIONS
STATE OUT
```

Adjacent `STATE OUT` / `STATE IN` mismatches are explicit boundary contradictions. Do not hide them with generic connective prose. Long-range messages may skip acts in either direction. Convergence means increasing temporal compatibility across the whole trajectory, not four completed outlines.

## REHEARSAL-led execution model

Structural generation should mostly create pressures, hypotheses, boundary states, unresolved transformations, competing possibilities, and questions worth testing.

An act repeatedly asks:

- what transformation is missing?
- what relationship movement is uncertain?
- what boundary state is not yet earned?
- what forward consequence needs testing?
- what backward requirement may be false?
- which competing possibility would materially alter the book?
- where do local beliefs conflict with another temporal slab?
- what promising state needs behavioral evidence?

Those become REHEARSAL targets.

REHEARSAL receives only enough constraint to make the experiment meaningful: state in, active pressure, environment/task when useful, relevant character truth, ownership boundaries, genuinely locked result if one exists, forward/backward constraints, and the uncertainty being tested. It must not be told what emotion or behavior must happen unless that outcome is actual authority. Honest failure of a desired trajectory is evidence against the trajectory.

### Heat levels

- `PROBE`: cheap plausibility / direction / rejection test.
- `DEVELOPMENT`: compare divergent behaviors, consequences, relationships, or missing transitions.
- `HIGH_HEAT`: selective expensive work for first encounters, major romance shifts, betrayals, confessions, negotiations, reversals, discoveries, climaxes, ending candidates, severe contradictions, constraint collisions, high downstream consequence, or high behavioral uncertainty.

Do not max heat on routine connective moments.

### Temporal / 4D rehearsal

REHEARSAL may test representative interactions at separated temporal coordinates before intervening prose exists. Early, middle, and late performances can be compared for identity continuity, missing transformations, implied history, implied future, and false-character requirements. This is derived evidence, not canon.

### Compact rehearsal evidence

Do not keep every performed token hot. After evaluation, reduce routine rehearsals to compact derived evidence:

- state change
- behavior discovered
- relationship movement
- causal consequence
- prerequisite
- contradiction
- branch strengthened / weakened / invalidated
- unresolved question
- confidence
- provenance pointer

Preserve full performance artifacts only when materially useful as case law, high-value provenance, or later audit evidence.

## STORY SYNC role

STORY SYNC remains the convergence authority for derived story state. It evaluates independent recurrence, dramatic usefulness, cross-act compatibility, forward/backward agreement, challenge survival, contradiction, retrofit cost, causal reach, reader promise, and character truth. One excellent REHEARSAL take remains one take.

STORY SYNC should consume compact rehearsal evidence and update confidence / propagation without silently averaging disagreements away.

## Creator-taste role

Creator taste is a bounded search heuristic only. It may modestly change what viable questions receive extra REHEARSAL attention and preserves at least one creator-surprise lane during exploration/compare. It cannot rescue invalid branches, alter discovery authority, promote story truth, remove the four-act baseline heartbeat, or gain authority during convergence.

## Efficiency / hot-vs-cold memory

Keep hot:

- current four act-local states
- active boundaries
- open high-value questions
- current forward/backward messages
- compact recent rehearsal evidence
- active STORY SYNC discoveries / contradictions

Let go cold:

- routine full rehearsal transcripts after reduction
- superseded local branches that no longer affect current search
- historical reasoning already captured by provenance
- prose-scale structural speculation with no active question attached

Historical full evidence remains addressable by provenance when useful.

## Implemented now

- generalized `scripts/story_sync_engine.py`
- STORY SYNC maturity, contradictions, forward/backward propagation, hidden-canon / reader checks, unresolved questions, provenance, convergence phases, and REHEARSAL queue
- `scripts/plg_ai_tools.py` `sync_story` derived-only entry point
- creator-taste prior / overlay machinery and tests, with a remaining compatibility seam in the full suite at capture
- `scripts/persistent_act_runtime.py`
- exactly four persistent temporal slabs
- explicit state-in/state-out hypotheses
- adjacent boundary contradiction detection
- long-range forward consequences and backward requirements that may skip acts
- local constraint responses
- cross-direction agreement attention
- non-starving baseline scheduler
- temporal-consistency reporting
- derived delta integration
- delegation of shared maturity back to STORY SYNC
- focused STORY SYNC + persistent-runtime suite green: 46 tests at capture

## Still hypothesis / not yet proven

- that four persistent temporal perspectives outperform simpler dynamic workers
- that REHEARSAL can reliably discover enough structure to reduce planner dependence
- ideal PROBE / DEVELOPMENT / HIGH_HEAT budget ratios
- how much full rehearsal evidence deserves permanent case-law retention
- whether temporal / 4D rehearsal materially improves relationship and transformation continuity
- how aggressively compact evidence can replace transcripts without losing useful implied history
- whether convergence signals should remain inspectable heuristics or eventually gain a lightweight score
- exact point where story truth is stable enough for sustained prose rendering

## Active experiments

1. **Dragon Spotter** — bounded proving ground for persistent four-act, bidirectional, REHEARSAL-led story discovery. Existing first-bargain / reciprocity material is evidence, not a frozen outline.
2. **Peg-Leg Greg architecture extraction** — source of the existing REHEARSAL, performance round-trip, hidden-canon, creator-taste, and STORY SYNC machinery. Canon prose remains separate authority.

## Current unresolved architectural questions

- What minimal structured REHEARSAL target contract gives enough context without prescribing behavior?
- What compact evidence schema best captures both forward consequences and backward implications from one performance?
- When should a temporal contradiction trigger PROBE vs DEVELOPMENT vs HIGH_HEAT?
- What evidence threshold justifies retaining a full transcript as permanent case law?
- How should multiple temporal rehearsal coordinates share character state without becoming a global outline?

## Exact next executable step

1. Finish the already-isolated creator-taste compatibility seam so the full repository suite is green without increasing taste authority.
2. Write RED runtime tests for a REHEARSAL-led target contract with `PROBE / DEVELOPMENT / HIGH_HEAT`, compact rehearsal-evidence reduction, forward/backward implication extraction, and temporal multi-coordinate targets.
3. Implement the smallest adapter in `persistent_act_runtime.py` that converts open boundary / causal / relationship uncertainty into those targets and consumes compact returned evidence into derived deltas for STORY SYNC.
4. Add one Dragon Spotter fixture proving the loop end-to-end without writing canon prose.

Do not build another planning engine before this experiment produces evidence that REHEARSAL cannot discover the missing structure.

## Historical trail underneath this file

- `docs/superpowers/specs/2026-09-07-ai-native-long-form-story-compiler-design.md`
- `docs/superpowers/specs/2026-09-07-persistent-act-channel-runtime.md`
- `docs/superpowers/plans/2026-09-07-persistent-act-channel-runtime.md`
- `state/experiments/dragon-spotter/story-sync/`

Fresh chats should start here, then open older material only when a specific provenance or implementation detail is needed.
