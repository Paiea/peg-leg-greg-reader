# DREAM + FORM Evolutionary Story Search Design

## Status

Approved architectural direction for PR #161 on `architecture/long-form-story-compiler`.

This design extends the settled long-form architecture without replacing it:

- STORY STATE = persistent memory
- ACT I-IV = persistent temporal perspectives
- REHEARSAL = uncertainty-directed experiment selection
- PERFORMANCE = embodied high-fidelity experiment
- STORY SYNC = conservative evidence reduction and convergence
- PROSE = rendering

The new layer is deliberately separated into a different cognitive regime:

- DREAM = generate without responsibility
- SYNC = believe only with evidence

The purpose is not to make the whole compiler less disciplined. The purpose is to create a hyper-divergent speculative population whose outputs remain non-authoritative until existing evidence machinery validates them.

## Goal

Exploit AI-native search to explore orders of magnitude more possible stories, representations, and scene realizations per finished novel while preserving conservative story truth and a hard bias toward completing long-form prose.

The forcing function is overnight novel generation. DREAM is successful only if it increases story quality per unit compute while still allowing the compiler to converge and render a complete manuscript. An endlessly interesting idea generator that prevents completion is a failure.

## Core invariants

1. DREAM candidates have no story authority.
2. Nothing moves directly from DREAM to STORY STATE.
3. STORY SYNC remains conservative and does not gain DREAM-specific promotion shortcuts.
4. Speculative branching is allowed to be extreme, but authority promotion still requires evidence.
5. The four persistent acts remain first-class temporal perspectives; DREAM populations are ephemeral search clouds spawned by acts, cross-act tensions, unresolved questions, or renderable intervals.
6. Dragon Spotter remains the bounded proving ground for this branch. Gravity-specific work remains project-local and must not be overwritten or generalized accidentally.
7. Generic compiler changes remain generic. Dragon-specific search lenses, seeds, constraints, candidate populations, evidence, and rendering experiments remain project-local.
8. No automatic canon write. `apply_survivors` remains the only canon-writing `plg_ai_tools` surface.
9. Rendering loops may update derived rendering memory and rendered-state ledgers, but cannot silently mutate STORY STATE.
10. If prose exposes a real causal/story gap, return the exact gap to REHEARSAL rather than restarting broad discovery.
11. FORM changes are first-class search operations. Representation itself is searchable.
12. Large search counts are conceptual exploration targets, not requirements to materialize or render thousands of full outlines.

## Why representation change is first-class

Repeated experiments have shown that changing form exposes information the previous representation could not. A structural hypothesis may look sound but fail under PERFORMANCE. A performed exchange may work but fail as prose. Compression may reveal that a beautiful scene contains no meaningful state transition. Backward retelling may expose missing prerequisites. Therefore the scheduler must search not only over story content but also over ways of representing and testing story content.

A candidate may move through forms such as:

- abstract causal graph
- timeline or state-transition chain
- counterfactual worldline
- backward prerequisite chain
- dialogue exchange
- screenplay/PERFORMANCE
- character interiority sketch
- compressed scene summary
- reader-experience description
- prose rendering
- backward retelling from state-out

Changing form produces evidence, not authority.

## Cognitive regimes

### DREAM

DREAM is allowed to be speculative, contradictory, weird, and wrong. Its job is to occupy conceptual territory the current story is not already converging toward.

DREAM may generate:

- character wants
- hidden motives
- mechanics
- reversals
- betrayals
- social structures
- relationship configurations
- setting constraints
- costs
- misunderstandings
- endings
- thematic ironies
- scene situations
- consequences
- secrets
- promises
- failures
- victories that worsen the problem
- apparently impossible transformations
- tiny Act I details with potential Act IV reach
- endings that make current Act I insufficient
- mechanisms capable of producing Act III transformations

DREAM may deliberately hallucinate against the current story by asking for mutually different ways the current trajectory could be wrong.

### STORY SYNC

STORY SYNC remains the immune system. It receives evidence reduced from selected DREAM survivors after cheap tests and REHEARSAL. It preserves contradictions, provenance, maturity, and conservative promotion rules.

DREAM says: `what if?`

SYNC says: `evidence?`

## Evolutionary search topology

```text
STORY STATE
    |
    +--> ACT I DREAM cloud
    +--> ACT II DREAM cloud
    +--> ACT III DREAM cloud
    +--> ACT IV DREAM cloud
    +--> cross-act contradiction clouds
    +--> unresolved-question clouds
    |
    v
DIVERSE SPECULATIVE POOL
    |
CLUSTER / NEAR-DUPLICATE SUPPRESSION
    |
NOVELTY PRESSURE
    |
MUTATION / CROSSOVER / FORM SHIFT
    |
CHEAP CAUSAL KILL
    |
HIGH-VALUE DIVERSE SURVIVORS
    |
REHEARSAL / PERFORMANCE
    |
STORY SYNC
    |
CONVERGED DERIVED STORY STATE
    |
LOCAL DREAM FOR RENDERABLE INTERVALS
    |
RENDER -> EVALUATE -> DIRECTED MUTATION / REPROMPT -> RERENDER
    |
COMPARE -> RETAIN -> RENDERED-STATE LEDGER -> ADVANCE
```

## Candidate contract

Every DREAM candidate must carry at minimum:

- stable candidate id
- source act / cross-act pressure / interval / unresolved question
- parent ids and mutation provenance
- speculative content
- current representation form
- mutation operator used
- search lens used
- explicit authority = `none`
- contradictions with current state, if any
- estimated conceptual distance from current population
- cheap causal test results
- surprise estimate
- causality estimate
- reach estimate
- information-gain-from-form-change estimate when applicable
- current status: generated / duplicate-suppressed / rejected / survivor / sent-to-rehearsal

No candidate field can promote story maturity directly.

## Search lenses

Search lenses are ephemeral mutation biases, not persistent agents or authorities. Initial generic lenses include:

- romance
- horror / catastrophic failure
- comedy
- mechanical exploitation
- social consequences
- reversals
- mundane human behavior
- strange-but-causal possibilities
- anti-default / genre-default destruction
- reader desire
- protagonist dread
- unconsidered consequences

Projects may add project-local lenses. Generic runtime must not encode Dragon-specific lenses or facts.

## Novelty pressure and clustering

Generating many completions from one prompt tends to produce semantic cousins. DREAM therefore values coverage of unexplored conceptual territory rather than raw sample count.

The engine must:

1. cluster near-duplicate candidates
2. heavily discount dense familiar clusters
3. preserve candidates from conceptually distant clusters
4. preserve representation diversity as well as content diversity
5. prevent one genre-default family from consuming all survivor slots
6. reward candidates whose combination of surprise, causality, and reach justifies more compute

A practical prioritization score is based on:

`surprise x causality x reach`

with additional novelty-distance and form-information-gain bonuses.

Surprise alone does not justify compute. Bizarre but causally unsupported candidates die cheaply.

## Mutation and crossover

The engine should achieve large search breadth through recursive divergence rather than 10,000 full outlines.

Supported content mutations should include:

- reverse causal arrow
- swap who pays a cost
- change who wants an outcome
- make success worsen the problem
- partially revive a rejected hypothesis
- move a discovery between acts
- replace apparent problem with deeper problem
- turn reward into constraint
- turn enemy action into unintended cooperation
- remove assumed explanation
- make hidden motive unnecessary
- cross unrelated survivors from distant clusters

Supported FORM SHIFT operators should include:

- ABSTRACT
- EMBODY
- COMPRESS
- EXPAND
- INVERT
- TEMPORAL_SHIFT
- POV_SHIFT
- PERFORM
- RENDER
- RETELL_BACKWARD

Operators remain generic. Specific prompts and examples remain project-local.

## Four-act adversarial DREAM

The four persistent acts should be able to hallucinate against each other:

- Act IV generates endings or identity states that make current Act I insufficient.
- Act I generates minor causes or details with large possible Act IV reach.
- Act III generates transformations that currently appear impossible.
- Act II searches for mechanisms capable of producing those transformations.

Cross-pollination then deliberately combines candidates from different acts and distant clusters before cheap causal testing.

This makes the act topology an evolutionary search population without collapsing the acts into stateless workers.

## Cheap causal kill

Most speculative candidates must die before REHEARSAL or PERFORMANCE.

Cheap filters should reject candidates that:

- directly contradict established story truth without an explicit counterfactual purpose
- require unsupported foundational mythology, factions, powers, villains, or institutions solely to function
- merely rename an existing candidate
- duplicate a dense familiar cluster
- provide surprise without causal foothold
- have negligible reach and negligible local usefulness relative to compute cost

Candidates that are strange but causally plausible should survive long enough to be rehearsed.

## Compute allocation

Compute should scale with uncertainty, narrative importance, and expected information gain.

Examples:

- bridge interval: small DREAM population, one render if acceptable
- first major bargain: large conceptual population, multiple cheap rehearsals, PERFORMANCE when embodied uncertainty warrants it, multiple prose realizations
- climax: high search and render budget

The scheduler should prefer more compute where a candidate can change multiple dimensions at once: mechanics, characterization, social value, progression, relationships, theme, or ending structure.

## REHEARSAL chooses representation as well as hypothesis

REHEARSAL must eventually be able to ask two questions:

1. What uncertainty is most valuable to reduce?
2. What representation is the cheapest useful way to expose it?

Examples:

- structural boundary uncertainty -> state-transition form
- long-range trajectory uncertainty -> worldline form
- relationship/trust uncertainty -> PERFORMANCE
- prose-only weakness -> targeted prose mutation
- unclear causal skeleton hidden by good prose -> COMPRESS or ABSTRACT
- missing prerequisite -> RETELL_BACKWARD / backward prerequisite form

Changing form is an experiment-selection decision, not a canon decision.

## Rendering DREAM loop

Once an interval is safe to render, the same evolutionary engine operates locally at smaller scale.

```text
renderable interval
  -> local DREAM realization concepts
  -> cluster and novelty filter
  -> select diverse few
  -> render candidates
  -> evaluate failure class
  -> directed mutation / targeted reprompt
  -> optional form shift if repeated prose attempts are uninformative
  -> rerender
  -> compare
  -> retain best derived candidate
  -> update rendering memory and rendered-state ledger
  -> advance
```

Reprompting is a directed mutation operator. It must preserve locked story state unless evaluation identified a genuine story gap.

## Rendering failure routing

Evaluation must diagnose failure class rather than emit only a quality score.

### Prose failure

Examples: clunky, repetitive, exposition-heavy, weak sensory grounding, pacing, dialogue ownership, voice drift.

Route: targeted reprompt / directed prose mutation.

### Performance failure

Examples: generic behavior, missing chemistry, unearned emotional exchange.

Route: PERFORMANCE or EMBODY form shift, then rerender.

### Story failure

Examples: motivation unsupported, transition unearned, causal contradiction.

Route: exact gap to REHEARSAL, then STORY SYNC, then resume rendering. Do not restart broad discovery.

### Continuity failure

Examples: wrong knowledge state, impossible location/state, premature reveal.

Route: correct derived rendering packet/state ledger, then rerender.

## Rendering memory

Retained rendering lessons may persist in a separate derived rendering-memory channel. Examples include effective voice or scene-realization lessons. Rendering memory cannot promote story truth or mutate persistent story state.

## Completion pressure

The system must have explicit stopping and forward-motion behavior.

Broad search stops when additional discovery information gain falls below cost. Rendering accepts adequate prose rather than endlessly polishing low-value intervals. High-value scenes get larger budgets. Specialist manuscript audits operate after a complete candidate draft and propose bounded repairs. Editing stops when successive audits mostly produce KEEP / no meaningful improvement.

Completion is therefore another convergence problem:

`declining information gain -> stop searching / stop editing`

## Five implementation updates

### Update 1: DREAM + FORM contract

Build the generic derived-only speculative candidate schema, search-lens contract, mutation provenance, representation-form contract, and authority guardrails. Add project-local Dragon fixtures proving that speculative content cannot mutate story truth.

### Update 2: Diversity and novelty engine

Build clustering / near-duplicate suppression, novelty pressure, representation-diversity preservation, survivor quotas, and generic scoring hooks for surprise, causality, reach, novelty distance, and form information gain.

### Update 3: Evolution and FORM SHIFT loop

Build recursive seed -> mutate -> crossover -> assumption reversal -> cross-act collision -> form shift -> cheap causal elimination. Preserve provenance across generations and avoid materializing thousands of full outlines.

### Update 4: REHEARSAL / STORY SYNC bridge

Allow only selected DREAM survivors to become explicit rehearsal targets or evidence questions. Extend experiment selection so representation can be chosen deliberately. Preserve current conservative maturity rules and forbid DREAM-specific authority promotion.

### Update 5: Rendering DREAM loop

Extend the existing bounded rendering seam into local DREAM -> render -> evaluate -> directed mutation/reprompt -> optional form shift -> compare -> retain -> advance. Add forward-motion budgets, rendering memory, exact gap escape to REHEARSAL, and project-local Dragon proving runs.

## Dragon proving strategy

Dragon Spotter should prove the architecture without contaminating the generic engine.

Use the current BROAD DISCOVERY COMPLETE state. Do not reopen broad Cycle 7 discovery merely because DREAM exists. Instead:

1. run a bounded DREAM population around the first-dragon bargain
2. demonstrate duplicate suppression and conceptual diversity
3. demonstrate at least one useful form shift
4. route only high-value survivors to existing REHEARSAL/PERFORMANCE machinery if necessary
5. render a bounded candidate sequence
6. evaluate and directed-reprompt locally
7. compare candidates and retain derived evidence only
8. if the slice works, widen into rolling long-form rendering rather than continuing to over-optimize the first scene

Preserve existing Dragon constraints, including:

- dragon seeks restoration of workable reciprocal order through costly voluntary human compliance, not sentimental apology or Greg validation
- Greg competence comes from observation plus Scholar constraint, not secret expertise
- mutual-indispensability remains STORY TRUTH
- operational-reliance-before-personal-trust remains mature and romance must not accelerate
- material/coin-like treasure remains the favored noncanon first-gift rendering default while land/relic remain explicit alternatives unless rendering supplies decisive evidence
- no convenient new cross-polity institution solely to solve the ending

## Testing strategy

Each update must use TDD and add focused unit tests before implementation. Tests must prove authority boundaries, deterministic reduction behavior where appropriate, diversity behavior, mutation provenance, form-shift routing, REHEARSAL integration, rendering failure routing, forward-motion budgets, and no canon mutation.

After every update:

- run focused relevant tests
- run the full repository suite
- verify concurrent Gravity fixtures still pass
- re-fetch moving branch authority before writes
- preserve PR #161 as open, draft, and unmerged

## Success criteria

The architecture is successful when it can demonstrate all of the following:

1. A wide speculative population can be generated without altering STORY STATE.
2. Dense semantic cousin clusters are suppressed in favor of conceptual diversity.
3. Recursive mutation/crossover explores more conceptual territory than repeated same-prompt sampling.
4. FORM SHIFT produces measurable information gain in at least one proving case.
5. Selected survivors can enter REHEARSAL without bypassing STORY SYNC authority rules.
6. Local rendering DREAM can generate, evaluate, mutate/reprompt, compare, retain, and advance.
7. Genuine story gaps escape cleanly back to REHEARSAL instead of being papered over by prose.
8. Adequate low-value intervals advance cheaply while high-value intervals receive more compute.
9. The compiler remains capable of stopping discovery and moving toward a complete manuscript.
10. No Dragon- or Gravity-specific assumptions enter generic compiler code.

## Non-goals

- generating 10,000 full outlines
- making DREAM candidates canon
- replacing the four persistent acts with stateless agents
- weakening STORY SYNC maturity thresholds to reward novelty
- adding new foundational worldbuilding merely to justify speculative candidates
- solving every unresolved story choice before prose
- endlessly polishing one scene instead of completing the book
- automatic canon publication

## Final pipeline

```text
SEED
  -> minimum STORY STATE
  -> persistent ACT I-IV temporal search
  -> DREAM populations
  -> cluster / novelty pressure
  -> mutate / crossover / FORM SHIFT
  -> cheap causal kill
  -> REHEARSAL / PERFORMANCE
  -> STORY SYNC
  -> convergence gate
  -> local rendering DREAM
  -> render
  -> diagnose
  -> directed mutation / reprompt / FORM SHIFT when useful
  -> compare
  -> retain
  -> rendered-state ledger
  -> advance
  -> complete draft
  -> specialist audits
  -> bounded repairs
  -> diminishing returns gate
  -> complete
```
