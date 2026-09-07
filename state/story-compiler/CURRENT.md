# Long-Form Story Compiler — CURRENT

**Status:** canonical continuation trailhead for the active experiment

**Architecture version:** `story-compiler/rehearsal-led-temporal-slabs-v2`

**Authority branch:** `architecture/long-form-story-compiler`

**Pull request:** draft PR #161, based on `editor/rehearsal-simulation-engine`

**Machine-facing sibling:** `state/story-compiler/CURRENT.json`

## Core model

The compiler is solving for one dramatically alive story trajectory through time rather than predicting the next chapter. Four persistent temporal perspectives maintain local speculative realities and boundary beliefs. They mainly identify consequential questions worth testing. **REHEARSAL is the broader experimental layer that chooses the cheapest useful test for an uncertain story hypothesis. PERFORMANCE is one high-fidelity behavioral representation available inside REHEARSAL, not the universal story representation.** STORY SYNC learns from repeated, independent, useful evidence and conservatively updates shared story state. Prose is downstream rendering. Accepted canon prose remains final story authority.

```text
STORY STATE = MEMORY
FOUR ACT CHANNELS = TEMPORAL PERSPECTIVES
REHEARSAL = EXPERIMENT SELECTION / ORCHESTRATION
PERFORMANCE = HIGH-FIDELITY EMBODIED BEHAVIOR TEST
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

Every scheduling epoch gives all four a cheap baseline heartbeat. Extra compute follows consequential uncertainty. Do not collapse them into one global planner, generic dynamic frontiers, or stateless workers yet.

**Invent freely inside an act. Promote conservatively across acts.**

## Shared Story IR / global state

Shared state is conservative derived memory, not canon. It carries cross-act information mature enough to matter globally:

- possibilities and discovery evidence
- `SPECULATION -> REPEATED SIGNAL -> STRONG THREAD -> STORY TRUTH`
- forward consequences
- backward requirements
- boundary / causal contradictions
- major character and relationship state
- unresolved shared questions
- hidden-canon and reader-state implications
- provenance and superseded assumptions

Local invention does not automatically enter shared truth. Parallel act work remains derived-only; shared integration is serialized and conflict checked.

## Temporal slabs and boundaries

Every act is a temporal slab with approximate:

```text
STATE IN
LOCAL SEARCH / REHEARSAL QUESTIONS
STATE OUT
```

An act's job is to discover a compelling lived trajectory that can transform its current `STATE IN` into a credible `STATE OUT`.

Adjacent `STATE OUT` / `STATE IN` mismatches are explicit boundary contradictions. Do not hide them with generic connective prose. Long-range messages may skip acts in either direction. Convergence means increasing temporal compatibility across the whole trajectory, not four completed outlines.

## Forward compiler rule

Ask:

> Given what this temporal region currently does under pressure, what consequences should later regions inherit or test?

Early rehearsal may imply candidate forward consequences such as remembered insults, maintained lies, obligation from gifts, changed reputation, attraction-driven avoidance, secrecy pressure, or learned reliance. Later acts receive these as probes, not commands, and test whether the consequence remains alive.

## Backward compiler rule

Ask:

> Given a promising later payoff, transformation, relationship state, or climax, what earlier conditions does the tested late behavior imply must probably have existed?

Late rehearsal may imply candidate backward requirements such as prior betrayal, shared routines, private language, learned trust, old control conflict, specific fear, accumulated resentment, or reciprocal obligation. Earlier acts test whether these arise naturally. A backward implication never becomes truth merely because one late experiment suggested it.

## REHEARSAL-led discovery

Structural generation should mostly create pressures, hypotheses, boundary states, unresolved transformations, competing possibilities, and questions worth testing.

An act repeatedly asks:

- what transformation is missing?
- what relationship movement is uncertain?
- what boundary state is not yet earned?
- what forward consequence needs testing?
- what backward requirement may be false?
- which competing possibility would materially alter the book?
- where do local beliefs conflict with another temporal slab?
- what promising state needs evidence?

Those become REHEARSAL targets.

### REHEARSAL chooses the experiment

Do not equate REHEARSAL with screenplay/PERFORMANCE.

Possible rehearsal modes include:

- compact plausibility probe
- state-transition test
- trajectory / worldline test
- forward-consequence test
- backward-prerequisite test
- counterfactual branch comparison
- temporal-distance rehearsal
- explicit PERFORMANCE / screenplay

Use the cheapest representation that can answer the uncertainty honestly.

### Fidelity escalation

```text
CHEAP PROBE
-> DEVELOPMENT REHEARSAL
-> HIGH-HEAT PERFORMANCE
```

Escalate when uncertainty, dramatic importance, or downstream consequence justifies it.

**PROBE:** basic plausibility, direction, causal viability, cheap branch rejection.

**DEVELOPMENT:** compare divergent behaviors or causal paths, discover consequences, connect temporal states, test important transformations.

**HIGH-HEAT PERFORMANCE:** embodied behavior is central and mistakes are expensive. Examples: dialogue ownership, attraction/chemistry, conflict, negotiation, avoidance, betrayal, confession, first encounters, relationship crossings, major emotional decisions, climaxes, ending candidates, severe cross-act contradictions.

Do not render every structural or causal question as screenplay.

### PERFORMANCE contract

When explicit PERFORMANCE is warranted, provide state in, active pressure, relevant character truth, environment/task when useful, ownership boundaries, forward/backward constraints, uncertainty being tested, and a required result only when genuinely locked.

Do not prescribe emotional or behavioral outcomes simply because the current structural trajectory wants them. If honest performance produces more distrust where the plan wanted trust, preserve that evidence and challenge the trajectory.

### Temporal / 4D rehearsal

REHEARSAL may test separated temporal coordinates before intervening prose exists. Early, middle, and late relationship/worldline states can be compared for continuity, missing transformations, implied history, implied future, and false-character requirements.

This may use cheap state/trajectory tests first. Escalate to PERFORMANCE only where embodied behavior is actually the uncertainty.

### Compact evidence and cooling

Do not keep every performed or probed token hot. After evaluation, reduce routine rehearsal to compact derived evidence such as:

- state change
- behavior discovered
- relationship movement
- causal consequence
- prerequisite
- contradiction
- candidate branch strengthened / weakened / invalidated
- unresolved question
- confidence
- provenance pointer

Preserve full rehearsal/PERFORMANCE artifacts only when materially useful as case law, high-value provenance, or later audit evidence.

## STORY SYNC role

STORY SYNC remains the convergence authority for derived story state. REHEARSAL/PERFORMANCE evidence does not automatically determine truth. One excellent take remains one take.

SYNC evaluates independent recurrence, dramatic usefulness, cross-act compatibility, forward/backward agreement, challenge survival, contradiction, retrofit cost, causal reach, reader promise, and character truth. Viable divergence remains alive until evidence earns convergence.

## Creator-taste role

Creator taste is a bounded search heuristic only. It may modestly change what viable questions receive extra REHEARSAL attention and preserves a creator-surprise lane during exploration/compare. It cannot rescue invalid branches, alter discovery authority, promote story truth, remove the four-act baseline heartbeat, or gain authority during convergence.

The evidence/storage layer exists. Search-priority integration still has RED contracts and is not yet complete at this capture.

## Efficiency / hot-vs-cold memory

Keep hot:

- current four act-local states
- active boundaries
- open high-value questions
- current forward/backward messages
- compact recent rehearsal evidence
- active STORY SYNC discoveries / contradictions

Let go cold:

- routine full rehearsal/PERFORMANCE transcripts after reduction
- superseded local branches that no longer affect current search
- historical reasoning already captured by provenance
- prose-scale structural speculation with no active question attached

Historical full evidence remains addressable by provenance when useful.

## Implemented now

- generalized `scripts/story_sync_engine.py`
- discovery maturity, contradictions, forward/backward propagation, hidden-canon/reader checks, unresolved questions, provenance, convergence phases, REHEARSAL queue
- `scripts/plg_ai_tools.py` `sync_story` derived-only entry point
- creator-taste evidence storage/rebuild; search-priority compatibility seam remains unfinished
- `scripts/persistent_act_runtime.py`
- exactly four persistent temporal slabs
- explicit state-in/state-out hypotheses
- adjacent boundary contradiction detection
- long-range forward consequences and backward requirements
- local constraint responses
- cross-direction agreement attention
- non-starving baseline scheduler
- temporal-consistency reporting
- derived delta integration
- delegation of shared maturity back to STORY SYNC
- bounded Dragon Spotter first-bargain HIGH-HEAT PERFORMANCE evidence
- focused STORY SYNC + persistent-runtime suite green at the first runtime implementation head

## Still hypothesis / not yet proven

- four persistent temporal perspectives outperform simpler dynamic workers
- REHEARSAL-led question selection can reliably reduce planner dependence
- ideal cheap/development/high-heat escalation policy
- temporal/4D rehearsal materially improves relationship and transformation continuity
- backward implied-history extraction can avoid retrofit sludge
- compact evidence can replace routine transcripts without losing useful story memory
- persistent baseline heartbeat remains useful late in convergence
- exact point where converged lived story is stable enough for sustained prose rendering

## Active experiment

**Dragon Spotter** is the bounded proving ground. Existing first-bargain material is evidence, not frozen outline.

Current high-heat artifact:

`state/experiments/dragon-spotter/story-sync/first-bargain-rehearsal.json`

Strong current hypotheses include reciprocal dragon obligation and observation-driven improvisation constrained by real Scholar knowledge. Land restoration versus relic restitution, treasure form, and late professional identity remain deliberately unresolved.

## Current unresolved architecture questions

- minimal structured REHEARSAL target contract that lets the orchestrator choose probe/development/PERFORMANCE without prescribing outcomes
- compact evidence schema that captures forward consequences and backward implications from any rehearsal mode
- escalation rules from cheap probe to development to high-heat PERFORMANCE
- full-evidence retention threshold for permanent case law
- how creator-taste search priority combines with the persistent-act scheduler after its current RED seam is green
- when story truth is stable enough to trigger prose rendering

## Exact next executable step

1. Finish the already-isolated creator-taste compatibility seam so the full repository suite is green without increasing taste authority.
2. Write RED runtime tests for a generic REHEARSAL target contract whose `experiment_mode` can be plausibility, state-transition, trajectory, forward, backward, counterfactual, temporal-distance, or PERFORMANCE, with `PROBE / DEVELOPMENT / HIGH_HEAT` escalation.
3. Implement the smallest adapter in `persistent_act_runtime.py` that turns open act/boundary/message uncertainty into those targets and consumes compact returned evidence into derived deltas for STORY SYNC.
4. Add one derived-only runtime-cycle entry point in `plg_ai_tools.py`.
5. Run the existing Dragon Spotter first-bargain evidence through the loop without restarting story state or writing canon prose.

Do not build another planning engine before evidence shows REHEARSAL cannot discover the missing structure.

## Historical trail

- `docs/superpowers/specs/2026-09-07-ai-native-long-form-story-compiler-design.md`
- `docs/superpowers/specs/2026-09-07-persistent-act-channel-runtime.md`
- `docs/superpowers/specs/2026-09-07-persistent-four-act-convergence-design.md`
- `docs/superpowers/specs/2026-09-07-creator-taste-prior-design.md`
- `state/experiments/dragon-spotter/story-sync/`

Fresh chats should start here, then open older material only for specific provenance or implementation details.
