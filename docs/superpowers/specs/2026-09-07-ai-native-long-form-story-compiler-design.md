# AI-Native Long-Form Story Compiler Design

**Status:** approved architectural direction, implementation starting

**Branch:** `architecture/long-form-story-compiler`

**Upstream dependency:** PR #160 / `editor/rehearsal-simulation-engine`

**Purpose:** extend the existing PLG Brain Compiler, universal PERFORMANCE compiler, campaign infrastructure, REHEARSAL simulation, and Full Canon / Showcase split into a generic long-form story-synthesis surface that can grow a finite novel from a sparse project seed without requiring a human to specify every chapter or scene.

---

## 1. Goal

The target is not a conventional outline generator with prose generation attached.

The target is an AI-native narrative system that can hold an entire finite book in play, explore several possible causal shapes, use high-intensity actor rehearsal to discover behavior and events, converge toward a coherent story, render prose at scale, preserve useful off-stage canon, and curate the strongest reader-facing path through that canon.

Conceptually:

`SEED -> GLOBAL COMPILE / SEARCH -> NARRATIVE PRESSURE -> REHEARSAL -> GLOBAL RECONCILIATION -> PROSE -> CANON -> READER CURATION -> RECOMPILE`

This is a feedback system, not a one-way assembly line.

The first implementation must create the smallest useful substrate for experimentation. It must not pretend that the correct long-form search algorithm is already known.

Dragon Spotter may later serve as a clean benchmark project, but no Dragon Spotter-specific logic belongs in core infrastructure.

---

## 2. Existing architecture is the owner

Do not create a parallel narrative backend.

Build through the seams that already exist:

- `scripts/performance_production_funnel.py` owns scene extraction, scene identity, mechanical/semantic/PERFORMANCE derived layers, dependency invalidation, and task views.
- `scripts/performance_campaign.py` owns campaign-scale fan-out, bounded concurrency, caching, reduction, telemetry, and serialized integration.
- `scripts/brain_compiler.py` and `scripts/plg_ai_tools.py` own narrow task-aware context compilation and AI-facing entry points.
- PR #160 `scripts/rehearsal_engine.py` owns actor simulation, relationship memory, variance takes, performance channels, discovery provenance, and rehearsal return policy.
- `publishing/showcase_chapters.json` plus existing Showcase tooling already prove the distinction between Full Canon and reader visibility.
- `state/editorial/performance-roundtrip/` already proves that successful intermediate PERFORMANCE evidence can remain durable derived case law without becoming story authority.

The long-form layer is an orchestration and representation extension over those capabilities.

It must not duplicate them under new names.

---

## 3. Authority model

### 3.1 Final story authority

**CANON PROSE remains the final story authority.**

Once prose is accepted into canon, derived plot maps, state views, rehearsal findings, reader maps, and search hypotheses cannot override it.

Before prose exists for a new region, explicit project seed constraints and accepted structural decisions may constrain generation, but they remain project direction rather than prose canon.

### 3.2 Derived representations

The backend may maintain rebuildable/cached projections such as:

- book / act structure
- causal graph
- dramatic units
- narrative-pressure state
- character trajectory
- relationship trajectory
- world / setting view
- scene state
- PERFORMANCE / REHEARSAL
- screenplay-like performance render
- prose candidate
- reader-state view
- curation / Showcase view

These are reasoning surfaces, not competing manuscripts.

### 3.3 Candidate material

Pre-canon generative material must have explicit status. Candidate possibilities are not canon merely because a worker generated or rehearsed them.

Candidate lifecycle may include:

`possibility -> rehearsed -> selected structural candidate -> prose candidate -> accepted canon`

At any point material may instead become:

- rehearsal-only evidence
- hidden canon after prose acceptance
- merged/compressed visible material
- rejected material

---

## 4. Canon, character state, reader state, and visibility

The PLG Showcase experiment becomes a generic long-form capability.

### CANON

Everything that actually happened in the story, including material not shown to the reader.

### CHARACTER STATE

What an actor knows, believes, remembers, owns, wants, fears, has promised, and has experienced because of canon.

Character state may therefore include hidden canon.

### READER STATE

What the visible manuscript has actually established for the audience.

### READER / SHOWCASE

The curated visible path through canon.

A canon scene may be classified for the reader as:

- SHOW
- HIDE
- MERGE
- COMPRESS

A candidate may also be rejected before canon acceptance.

**HIDE is not failure.**

The system may generate a larger lived reality than the reader needs.

However, hidden canon must not create illegible visible prose. When a visible payoff depends on knowledge or development established only in hidden canon, reader-state validation must identify the gap and prefer the smallest sufficient visible setup rather than automatically restoring the hidden scene.

Visibility never changes whether an accepted event happened.

---

## 5. Compile wide, not only forward

The compiler must be able to reason across the whole finite book before every chapter is fixed.

It should support provisional dramatic units across multiple acts/regions simultaneously.

A dramatic unit may carry compact fields such as:

- stable candidate/unit ID
- region / act affinity
- state in
- active pressure
- actors / relationships involved
- relevant world conditions
- information available
- desired transformation class
- possible state out
- unresolved consequence created
- setup/payoff dependencies
- structural function
- confidence / maturity
- mutability
- provenance

These fields constrain dramatic work without specifying exact choreography.

Chapter boundaries are not required to be primary during search. Dramatic units may later merge, split, disappear, remain hidden, or resolve into chapters.

---

## 6. Experimental generation strategies

Do not hard-code one assumption about how a novel must be generated.

The long-form orchestration surface must make strategy selectable/swappable while sharing the same authority, representations, REHEARSAL, prose, and curation machinery.

At minimum preserve room for:

1. **sequential-biased**
   - earlier regions gain resolution first while later regions remain coarse but active.

2. **simultaneous multi-act**
   - multiple acts/regions develop concurrently and exchange constraints.

3. **global possibility search**
   - candidate pressures, consequences, setups, payoffs, and relationship movements may be proposed across the whole book and connected afterward.

4. **hybrid convergence**
   - broad exploration early, increasing concentration around a dominant causal thread as evidence accumulates.

The first implementation does not need a sophisticated optimizer for all modes. It does need a clean strategy boundary so experiments can change scheduling/search behavior without rewriting authority or rehearsal code.

---

## 7. Structural anchors are gravity, not an outline

A project may provide sparse long-range constraints such as:

- opening condition
- ending inversion / ending condition
- central story promise
- major character transformations
- broad act functions
- relationship progression expectations
- important reveal/payoff requirements
- genre / heat / tone constraints
- optional soft word-count range

These are search anchors.

They should bias what the compiler considers useful without dictating exact scenes.

The compiler should prefer the smallest amount of scaffolding that produces a finite, legible story.

---

## 8. Narrative pressure belongs in compilation

The compiler should produce pressure and transformation requirements rather than overcompiled event instructions.

Useful derived signals include:

- current structural region
- unresolved transformations
- unresolved consequences
- underfed arcs
- repeated/exhausted dynamics
- setup/payoff debt
- escalation range
- proximity to act turn
- proximity to ending condition
- candidate threads currently gaining support
- movement that is due but not yet event-specific

Preferred instruction style:

> The dragon gift must begin producing a human political consequence and the protagonist's professional state must move toward earned competence.

Avoid:

> Write a courtroom scene where the Crown confiscates the dragon gift.

**Compiler supplies pressure and boundaries. REHEARSAL searches behavior.**

---

## 9. Bidirectional constraint propagation

Long-form search must support both directions.

### Forward

`Given established causes and actor state, what can credibly follow?`

### Backward

`Given a promising later payoff or transformation, what earlier conditions are required to earn it?`

Later discoveries may create setup requirements in earlier mutable regions.

Earlier accepted canon constrains what later payoffs remain credible.

Do not rewrite accepted canon merely to rescue a late idea. Depending on authority/mutability, the system may:

- add the smallest sufficient earlier setup in mutable material
- choose a different payoff
- reject the late discovery
- explicitly request a canon revision rather than silently changing it

This bidirectional behavior should work across act boundaries.

---

## 10. PERFORMANCE / REHEARSAL is a primary story-search mechanism

REHEARSAL is not merely a polishing stage between plot and prose.

Some of the most important story discoveries should be expected to emerge while actors perform under pressure.

The compiler may provide:

- pressure
- actors
- state in
- desired transformation
- causal constraints
- relationship state
- world conditions
- structural function

It should deliberately leave behavioral and event-level uncertainty unresolved when safe.

**Compiler supplies pressure and boundaries.**

**REHEARSAL searches behavior.**

**Global compilation learns from what REHEARSAL discovers.**

### 10.1 High rehearsal heat

Rehearsal budget must be adaptive and may consume a large portion of total inference effort.

Increase heat/depth for:

- first major encounters
- negotiations
- major romantic crossings
- betrayals / confessions / confrontations
- act turns
- reversals
- major discoveries
- scenes with large downstream consequences
- scenes with high behavioral uncertainty
- scenes with several viable trajectories
- major payoffs that must feel earned
- moments where unusual chemistry or emergent behavior appears

Reduce heat when:

- behavior is tightly constrained
- material is connective
- repeated takes converge on the same solution
- further rehearsal produces cosmetic rather than structural variation

Do not prematurely optimize for minimum rehearsal cost.

### 10.2 Divergent takes

High-value units should support genuinely divergent takes, not paraphrases of one predetermined event.

Takes may differ in initiation, withdrawal, leverage, misunderstanding, concessions, timing, attraction, disclosure, outcome path, and consequences while respecting hard boundaries.

### 10.3 Rehearsal can challenge structure

Repeated or strong performance evidence may report that a compiled possibility:

- requires false behavior
- creates weak chemistry
- resolves pressure too easily
- produces a stronger unintended consequence
- reveals a better relationship
- belongs to another POV/actor
- makes a planned unit unnecessary
- exposes a better causal route

Before prose hardens, those discoveries may propagate forward, backward, sideways across trajectories, and across acts.

### 10.4 Temporal-distance rehearsal

The system may rehearse representative early, middle, and late moments of the same relationship/actor trajectory before all intervening material is fixed.

This can reveal abrupt, weak, or repetitive transformations and feed revised constraints back into global compilation.

### 10.5 Preserve important rehearsal evidence

Do not archive every disposable take.

Preserve successful intermediate evidence when a rehearsal materially determines surviving canon prose or a consequential structural branch.

This remains derived editorial case law, never story authority.

---

## 11. Finding the thread without infinite search

Global possibility search is an experiment, not doctrine.

When enabled, the system may generate candidate material across the book and look for causal/emotional/thematic connections afterward.

A promising thread is one that increasingly connects several needs at once, for example:

- protagonist transformation
- relationship development
- plot causality
- world conflict
- setup/payoff
- thematic recurrence
- act movement

Material that connects multiple dimensions should be eligible for more rehearsal/search attention.

Novelty alone is not enough.

Disconnected possibilities should receive less attention unless later evidence connects them.

### Convergence pressure

Exploration must not run forever.

As confidence grows, increasingly favor:

- causal reuse
- consequences of established choices
- payoff of existing promises
- deepening established relationships
- completion of major transformations
- material supporting a dominant causal structure

Increasingly disfavor:

- unrelated new factions
- unrelated mysteries
- repeated versions of established dynamics
- emergency world rules invented to solve a local problem
- late subplot proliferation

Search strategy owns how quickly this exploration-to-convergence pressure increases.

---

## 12. Temporary overgeneration

The system may generate/rehearse more dramatic material than the final visible manuscript requires.

This is intentional.

Overgenerated material may later be:

- selected into visible canon
- accepted as hidden canon
- merged
- compressed
- retained only as rehearsal evidence
- rejected

Do not force every generated unit to justify a visible chapter before the story shape is known.

Do not confuse abundance with canon acceptance.

---

## 13. Derived world / character / scene state

Do not require humans to maintain giant mutable state databases.

Where practical, derive state from accepted canon plus explicit project constraints.

Useful views include:

### World

Locations, geography, institutions, customs, recurring objects, treaties, economic/political facts, and other durable setting knowledge.

### Character

Knowledge, beliefs, relationships, possessions, injuries, promises, debts, attraction, loyalties, secrets, competence, and current goals.

### Scene

Who is present, where they are, immediate objective, active pressure, relevant props, available information, and boundary state.

These may be cached for efficiency but remain rebuildable/disposable.

Canon revision must invalidate affected derived views.

### Local invention promotion

Use:

**Invent freely locally. Promote conservatively globally.**

Incidental texture does not automatically become global setting authority.

Promote inventions when they recur, become causal, are referenced later, or materially constrain future work.

---

## 14. Whole-book recompilation

The architecture is intentionally cyclic:

`GLOBAL COMPILE -> REHEARSAL -> GLOBAL RECOMPILE -> TARGETED REHEARSAL -> PROSE`

Rehearsal discoveries should be able to reshape unresolved regions before polished prose is generated unnecessarily.

Once substantial prose exists, the compiler can also project the manuscript into diagnostic views and target weak regions instead of rewriting everything blindly.

Possible diagnostics include:

- act shape
- protagonist transformation
- actor trajectory
- romance / relationship progression
- conflict escalation
- world consistency
- reader knowledge
- pacing / repetition
- POV ownership
- voice
- continuity

Do not implement an uncontrolled infinite self-edit loop. Every recursive mission needs explicit pass/budget/convergence bounds.

---

## 15. Parallelism and ordering

Existing campaign infrastructure already supports bounded fan-out and serialized integration. Reuse it.

Independent candidate units or act regions may be explored/rehearsed concurrently when their boundary conditions permit.

Parallel workers remain derived-only.

Canon integration remains serialized and conflict-checked.

The system must not require prose word 1 through word 150,000 to be generated by one sequential invocation.

Once boundary conditions are sufficiently stable, prose regions may be rendered independently and reconciled at seams.

---

## 16. Finite-book gravity and stop conditions

A novel must be able to end.

Support project-level ending conditions / transformations and broad act-turn conditions.

Chapter count alone is never progression authority.

Word count is soft pacing gravity only.

The long-form compiler should detect when a dramatic question is exhausted: if a state has been convincingly demonstrated and new material only repeats it, increase pressure, transform the state, merge/compress the material, or turn the structural region.

A book is eligible to stop when its declared book-level transformation and originating dramatic problem have been sufficiently resolved, even if larger world questions remain open.

---

## 17. Search strategy versus authority

Generation strategy is execution policy, not story authority.

Changing from sequential-biased to global-search or hybrid mode must not require rewriting canon/state contracts.

The first implementation should therefore separate:

- durable project anchors
- candidate/global story representation
- strategy scheduling/prioritization
- rehearsal packet construction
- rehearsal evidence
- canon acceptance
- reader visibility

This separation is the primary architectural requirement for experimentation.

---

## 18. Initial implementation scope

The first slice should build generic deterministic contracts and packet builders rather than pretending to autonomously write a 150k novel immediately.

Initial primitives:

1. long-form project seed / structural-anchor validation
2. candidate dramatic-unit representation
3. forward/backward dependency representation
4. global compile/search state representation
5. named swappable generation strategies
6. exploration/convergence phase policy
7. adaptive rehearsal-heat policy
8. narrow model-facing global and rehearsal-pressure packet builders
9. candidate lifecycle and reader visibility states
10. reader-state dependency validation primitive
11. AI-facing entry point through the existing tool surface
12. durable long-form trailhead / status surface

These are coordination contracts. Semantic/model workers will later populate their intelligent fields.

Do not implement a fake deterministic novelist.

---

## 19. Explicit non-goals for first slice

Do not:

- write Dragon Spotter
- generate 150k words in CI
- merge PR #160 calibration prose into `main`
- create a second actor/rehearsal engine
- create a competing manuscript authority
- create a giant setting database
- create an autonomous infinite self-edit loop
- hard-code four acts as universal
- assume global possibility search is the winning strategy
- retire PLG's existing sequential Manuscript Engine

PLG's established one-chapter forward-production workflow must remain valid.

The new long-form mode is an additional orchestration capability for finite-book synthesis experiments.

---

## 20. Dependency on PR #160

This architecture begins from PR #160 because high-heat rehearsal is central and #160 is the current live owner of that capability.

The long-form branch must not fork/copy `rehearsal_engine.py` into another implementation.

Until #160 is accepted/reconciled:

- the long-form branch may depend on its rehearsal contracts;
- long-form commits should avoid modifying experimental PLG calibration prose unless required by upstream synchronization;
- the eventual integration plan must separate reusable rehearsal infrastructure from intentionally overtuned calibration prose;
- if #160 changes rehearsal schemas, long-form code should reconcile to the current owner rather than freezing a stale copy.

---

## 21. Validation

Use small synthetic fixtures.

At minimum validate:

- project anchors remain sparse and do not require scene outlines
- unknown generation strategy is rejected
- strategy changes do not mutate authority data
- candidate units can exist across multiple regions simultaneously
- forward and backward constraints can coexist
- accepted canon is not silently mutated by backward setup requests
- exploration/convergence phase changes prioritization policy without canon mutation
- rehearsal heat increases for high-leverage/high-uncertainty material
- rehearsal heat decreases for connective/converged material
- divergent takes share frozen boundary/memory authority where required
- hidden canon remains valid character-state evidence
- reader-state validation detects a visible payoff whose only setup is hidden
- visibility changes do not change canon status
- local invented detail is not globally promoted without promotion evidence
- derived views can be invalidated/recompiled
- PLG existing PERFORMANCE and Showcase tests remain green

TDD applies to every production behavior.

---

## 22. Success criteria

The infrastructure build succeeds when a future fresh worker can take an approved sparse novel seed and, without inventing a new backend:

1. compile a global candidate story representation;
2. choose an experimental search strategy;
3. issue pressure/rehearsal work across multiple unresolved book regions;
4. spend heavy rehearsal budget where behavioral discovery is valuable;
5. feed rehearsal discoveries back into unresolved structure;
6. represent forward and backward causal requirements;
7. converge rather than proliferate forever;
8. render selected material toward prose/canon through existing authority gates;
9. keep useful canon hidden from the reader when appropriate;
10. validate that the reader still has enough evidence for visible outcomes;
11. stop when finite-book conditions are satisfied;
12. reproduce the process from repository authority after the originating chat is gone.

The system should make `write this book from the seed using the backend` a plausible mission without requiring the human to manually prompt every chapter.