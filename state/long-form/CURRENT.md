# Long-Form Runtime CURRENT

**Architecture:** `persistent-four-act-rehearsal-led/v1`

**Authority branch:** `architecture/long-form-story-compiler`

**Implementation head before this continuation snapshot:** `cc80278a3706cfa3974d556b9f316205cb8cdc51`

**Machine-facing state:** `state/long-form/CURRENT.json`

## Core model

One finite story trajectory is explored through four persistent temporal slabs: ACT I, ACT II, ACT III, ACT IV. Each slab keeps permissive local beliefs and approximate `STATE IN -> lived local trajectory -> STATE OUT` boundaries. The slabs mostly identify high-value story questions. REHEARSAL is the primary semantic execution environment used to discover believable behavior, consequences, relationship movement, implied history, and implied future. STORY SYNC conservatively learns from repeated evidence and updates shared cross-act story state. Prose is downstream rendering. Accepted canon prose remains final story authority.

## Persistent topology

Do not replace the four channels with generic dynamic frontiers yet.

- ACT I: persistent local temporal search
- ACT II: persistent local temporal search
- ACT III: persistent local temporal search
- ACT IV: persistent local temporal search

Every act receives a nonzero baseline heartbeat. Extra compute follows boundary contradictions, forward/backward collisions, important relationship transitions, book-shaping uncertainty, ending candidates, and high-value REHEARSAL work.

**Invent freely inside an act. Promote conservatively across acts.**

## Shared Story IR

Shared state is conservative derived memory, not canon. It carries promoted discoveries, repeated signals / strong threads / story truths, forward consequences, backward requirements, boundary contradictions, major relationship/character state, hidden-canon and reader-state implications, and provenance.

Local possibilities do not become shared truth merely because they exist.

## Directional compiler rules

**Forward:** after lived behavior is rehearsed, extract candidate later consequences/opportunities. Later acts test whether they remain alive.

**Backward:** after a promising late state/payoff is rehearsed, extract candidate earlier prerequisites implied by the behavior. Earlier acts test whether those conditions arise naturally.

Messages are pressure, not commands. A receiving act may support, conflict, find a third path, reject the source candidate, or leave the requirement untested.

## Temporal boundaries

Each act maintains approximate `STATE IN` and `STATE OUT` hypotheses. Adjacent mismatches are explicit boundary contradictions. Do not smooth them with generic connective prose. REHEARSE the missing behavioral bridge and let the performed intermediate state challenge either side.

## REHEARSAL-led execution

Act channels should mostly ask questions worth rehearsing rather than endlessly expanding outlines.

Feed REHEARSAL state, pressure, relevant character truth, environment/task where useful, ownership boundaries, directional constraints, and the uncertainty being tested. Do not prescribe an emotional/behavioral outcome unless it is genuinely locked.

Heat:

- **PROBE:** cheap plausibility/direction test
- **DEVELOPMENT:** compare divergent behavior and connect temporal states
- **HIGH HEAT:** major encounters, romance transitions, negotiations, reversals, climaxes/endings, severe constraint collisions, high downstream consequence

REHEARSAL may operate temporally: early/middle/late coordinates of a relationship or trajectory can be tested before intervening prose exists. Late behavior may imply candidate earlier history; early behavior may imply candidate future consequences.

Reduce routine rehearsal into compact derived evidence. Preserve full rehearsal only when it materially matters as case law/provenance.

## STORY SYNC

STORY SYNC remains the convergence authority for derived beliefs. REHEARSAL evidence does not automatically become truth.

Promotion remains:

`SPECULATION -> REPEATED SIGNAL -> STRONG THREAD -> STORY TRUTH`

SYNC weighs independent recurrence, dramatic usefulness, cross-act compatibility, forward/backward agreement, survived challenge, contradiction, causal reach, reader/audience promise, and character truth. Viable divergence remains alive until evidence earns convergence.

## Creator taste

Creator taste only affects what plausible material deserves more search/rehearsal. It cannot override canon, character truth, causality, audience promise, or strong repeated rehearsal evidence. Creator-surprise remains counter-pressure.

The evidence/storage layer exists. Search-priority integration still has RED contracts and is not yet complete.

## Hot / cold memory

- **Cold:** GitHub canon/specs/provenance/important rehearsal case law
- **Warm:** compact shared Story IR plus persistent act-local state
- **Hot:** one task-specific act/rehearsal packet and only relevant exact evidence

Do not make normal workers reread the repository, whole manuscript, full creator evidence ledger, or every rehearsal transcript.

## Implemented now

- generalized STORY SYNC confidence/provenance/convergence
- viable-branch preservation, contradiction tracking, event-driven sync
- forward/backward propagation plans
- hidden-canon versus reader-state checks
- REHEARSAL feedback targets
- creator-taste evidence storage/rebuild
- `persistent_act_runtime.py` with four slabs, explicit boundaries, long-range messages, boundary contradictions, non-starving scheduling, temporal-consistency report, and delegation to STORY SYNC
- Dragon Spotter first-bargain high-heat rehearsal evidence

## Still hypothesis / unresolved

The four-slab topology, all-act heartbeat, temporal-consistency metric, REHEARSAL-led question generation, 4D rehearsal, backward implied-history extraction, and creator-taste search improvement remain experiments rather than proven architecture.

The most important missing executable seam is compact **act question -> REHEARSAL -> evidence/forward/backward implication -> STORY SYNC** orchestration.

## Active project experiment

Dragon Spotter remains pre-canon. Current high-heat first-bargain evidence is at:

`state/experiments/dragon-spotter/story-sync/first-bargain-rehearsal.json`

Current strong hypotheses include reciprocal dragon obligation and observation-driven improvisation constrained by real Scholar knowledge. Land restoration versus relic restitution, treasure form, and late professional identity remain deliberately unresolved.

## Exact next step

Implement a minimal REHEARSAL-led seam in `persistent_act_runtime.py`:

1. compile rehearsal questions from each act's unresolved transformation/boundary/message pressure
2. assign PROBE / DEVELOPMENT / HIGH HEAT
3. accept compact rehearsal findings
4. reduce them into state change / behavior / relationship movement / contradiction / branch effect / candidate forward consequence / candidate backward requirement
5. feed only earned shared evidence and messages into existing STORY SYNC
6. expose one derived-only runtime-cycle call in `plg_ai_tools.py`
7. test it against the existing Dragon Spotter first-bargain evidence without restarting project state

Do not start prose generation before this seam is working.

## Historical references

- `docs/superpowers/specs/2026-09-07-ai-native-long-form-story-compiler-design.md`
- `docs/superpowers/specs/2026-09-07-persistent-act-channel-runtime.md`
- `docs/superpowers/specs/2026-09-07-persistent-four-act-convergence-design.md`
- `docs/superpowers/specs/2026-09-07-creator-taste-prior-design.md`
