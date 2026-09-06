# Universal PERFORMANCE Compiler Design

**Status:** DESIGN DRAFT — user-approved architecture; awaiting written-spec review before implementation planning

**Owner:** existing `editor/performance-production-funnel` branch / PR #143

**Purpose:** evolve the existing PERFORMANCE production funnel so screenplay-style performance compilation becomes cheap enough to run across every chapter/scene, while preserving canon as the sole story authority and using the resulting shared scene representation to simplify older editorial machinery over time.

---

## 1. Goal

The long-term target is not a smarter filter that decides which scenes deserve screenplay treatment.

The target is to make the screenplay transform cheap enough that **screening costs more than simply running it**.

The existing flow is approximately:

`CANON -> CHEAP SCREEN -> MAYBE DRAMATIC/PERFORMANCE/SCREENPLAY -> MAYBE REVERSE EDIT -> CANON PATCH`

The evolved flow should be:

`CANON -> SCENE EXTRACTION -> RICH CHEAP IR -> PERFORMANCE IR -> SCREENPLAY EVERY SCENE -> COMPARISON -> MAYBE DEEP REVERSE EDIT -> MAYBE CANON PATCH`

The expensive gate moves toward the end of the pipeline.

A `SOURCE WIN` scene may still receive a screenplay render. The conclusion is made after the transform, not before it.

The architecture should also create a stronger reusable primitive for dialogue, continuity, illustration, compression, Showcase curation, and future editorial passes. A successful new primitive should reduce the number of older systems that need to rediscover the same scene facts independently.

---

## 2. Hard authority boundary

**CANON PROSE remains the only story authority.**

The compiler is derived editorial machinery.

No scene IR, semantic inference, PERFORMANCE frame, screenplay, comparison, diagnostic score, cached result, or successful roundtrip archive may silently establish canon facts or override current prose.

Use this epistemic order:

1. **CANON FACT** — directly present in current authoritative prose or another explicitly owning canon surface.
2. **LOCKED DERIVED JUDGMENT** — a non-canon interpretation that survived stronger review or a successful roundtrip and is preserved as reusable case law/evidence.
3. **PROVISIONAL INFERENCE** — cheap semantic interpretation produced for routing or transformation.

A higher-confidence inference is still an inference.

When a downstream task needs high certainty, it can request exact canon source alongside any derived fields.

---

## 3. Architectural constraint: evolve the current pipeline

Do **not** create a parallel `scene-compiler`, `compiler/`, second editorial engine, or new root lane.

The existing PERFORMANCE production funnel remains the stable owner.

Current relevant surfaces include:

- `scripts/performance_production_funnel.py`
- `.github/workflows/performance-production-funnel.yml`
- `state/editorial/performance-production/`
- `state/editorial/performance-roundtrip/`
- `scripts/performance_roundtrip_references.py`
- the existing PERFORMANCE lab / novelization evidence that proved the technique

The new architecture should extend or replace internals behind these surfaces rather than advertise another system beside them.

The current `performance_production_batch/v1` format is transitional evidence, not a permanent constraint.

---

## 4. Optimization philosophy

### 4.1 Wide at rest, narrow in context

If extraction is cheap, extract broadly.

The persistent scene representation may contain far more information than any one worker needs. Downstream AI workers should receive only a task-specific projection.

Do not confuse:

- **cheap to compute/store**, and
- **cheap to load into model context**.

The durable scene record can be wide. The compiled working packet should be narrow.

### 4.2 Cache cognition, recompute metadata

Preserve expensive/non-obvious semantic understanding when it earns reuse.

Regenerate or re-fetch mechanical facts when they are cheaper than preserving complicated stale state.

### 4.3 Deterministic shell, intelligent center

Use deterministic machinery for:

- HTML/prose extraction
- paragraph indexing
- quote/dialogue parsing when mechanically resolvable
- regex signals
- entity-string mentions
- counts and ratios
- source anchors
- hashes
- schema validation
- dependency invalidation
- patch boundary matching
- no-em-dash and attribution invariants

Use model reasoning where interpretation begins:

- scene boundaries when ambiguous
- goals
- state in/out
- relationship pressure
- knowledge asymmetry
- dramatic turn
- scene function
- emotional state
- performance stance
- whether the performed version actually improves prose

### 4.4 Universal cheap transform before selective expensive judgment

The architecture should work toward:

- screenplay/performed-script generation for every scene;
- cheap comparison for every scene;
- expensive reverse-edit reasoning only for scenes where the comparison indicates a plausible reader-facing improvement.

Screening may remain as diagnostic feature extraction, but not as the gate that prevents screenplay generation.

---

## 5. Unit boundaries

### 5.1 Chapter = scheduling and user-command unit

Normal commands remain intuitive:

- compile Chapter 214
- compile 201–220
- compile all stale chapters
- run PERFORMANCE across the manuscript

The user and high-level worker should not need to manually address every scene.

### 5.2 Scene = compilation, caching, and invalidation unit

Internally, scenes are the smallest durable semantic unit.

Benefits:

- one changed scene does not invalidate an entire chapter;
- smaller AI inputs improve reliability and cost;
- PERFORMANCE naturally operates at scene/exchange scale;
- unchanged scene cognition can be reused;
- dialogue/illustration/continuity consumers can retrieve only relevant scenes;
- successful reverse-edit evidence can point at the exact performed unit.

A chapter screenplay is a disposable assembly of its scene renders, not the atomic storage unit.

---

## 6. Stable scene identity

Paragraph numbers are locations, not identities.

Use lineage-stable scene IDs with spacing, for example:

- `214.s010`
- `214.s020`
- `214.s030`

If a durable new scene is inserted between two existing scenes, a worker may assign `214.s015` rather than renumbering every later scene.

A scene manifest records current ordering separately.

### 6.1 Identity rules

A scene ID should survive:

- paragraphs inserted before the scene;
- minor prose edits inside the scene;
- changes in paragraph numbering;
- unrelated changes elsewhere in the chapter.

A scene ID should not be silently reused when the underlying dramatic unit is replaced by a materially different scene.

### 6.2 Split and merge lineage

When a scene fundamentally splits or merges, preserve lineage explicitly.

For a split, retire the old current ID and point to the successor scenes:

```json
{
  "scene_id": "214.s020",
  "status": "superseded",
  "split_into": ["214.s021", "214.s022"]
}
```

For a merge, the new current scene points back to all parents:

```json
{
  "scene_id": "214.s025",
  "supersedes": ["214.s020", "214.s030"]
}
```

Historical IDs remain provenance, not current routing targets.

### 6.3 Scene matching after edits

Rebuild should attempt deterministic continuity first using:

- source anchors;
- normalized-text similarity/fingerprints;
- character/entity overlap;
- nearby ordering;
- previous paragraph span as a hint only.

If deterministic matching is ambiguous, cheap semantic reconciliation may propose a mapping.

If identity remains ambiguous, mark the scene for re-identification rather than silently attaching cached semantics to the wrong prose.

---

## 7. Scene segmentation

Segmentation should be layered.

### 7.1 Deterministic candidate boundaries

The parser may identify likely boundaries from:

- explicit scene separators;
- HTML structure;
- paragraph runs;
- strong location/time transition markers;
- cast turnover;
- headings/subheadings when present;
- large narration-to-dialogue mode changes;
- known chapter-level structural markers.

Regex and parsers produce **candidate boundaries**, not dramatic truth.

### 7.2 Cheap semantic boundary resolution

A cheap semantic pass decides whether candidate spans belong to one dramatic scene or should split/merge.

Useful questions include:

- Does one active task continue?
- Does the cast/relationship pressure remain continuous?
- Is there one state transition or multiple independent ones?
- Did time/location materially jump?
- Would treating these paragraphs separately destroy required context?

### 7.3 Boundary confidence

Store boundary provenance and confidence so uncertain segmentation is discoverable.

Do not treat a segmentation confidence score as canon authority.

---

## 8. Storage inside the existing PERFORMANCE production surface

Do not create a new root system.

Evolve `state/editorial/performance-production/` toward small, addressable records.

Recommended eventual shape:

```text
state/editorial/performance-production/
  214/
    manifest.json
    s010.json
    s020.json
    s030.json
```

This is still the PERFORMANCE production pipeline.

### 8.1 Chapter manifest

The chapter manifest should remain small and answer routing questions without loading every scene.

Example responsibilities:

- schema version
- canon chapter
- source path
- current chapter source blob/hash
- compiler versions
- ordered current scene IDs
- per-scene source hash
- per-scene cache validity
- lineage pointers
- latest chapter compile status

It should not duplicate every semantic field from scene records.

### 8.2 Scene record

A scene record is the AI-facing persistent cache for one semantic scene.

Git already stores each committed file as content-addressed blob data. The architecture should use normal Git files and blob SHAs rather than inventing a separate blob service.

Blob identity is useful for exact content identity and caching, but does not itself reduce model cost. The cost win comes from small addressable records, narrow retrieval, stable dependencies, and reuse of unchanged derived cognition.

### 8.3 AI-native representation rules

The structured record is not a human report encoded as JSON.

Optimize it for machine retrieval and model reasoning:

- stable field names and schema versions;
- atomic claims rather than paragraphs of explanatory prose;
- arrays/objects for independent facts that downstream workers may project separately;
- explicit `unknown`, `not_applicable`, or omitted-field semantics rather than filling gaps with guesses;
- source anchors/pointers instead of copying large source passages into every derived record;
- no duplicate field merely because it makes a human document read more smoothly;
- bounded free-text fields where semantic nuance is necessary;
- preserve distinctions such as observed/inferred/locked rather than flattening them into polished prose;
- allow task views to serialize into compact JSON or dense model-facing text without requiring Markdown headings.

Human-readable `dramatic.md`, `performance.md`, screenplay, or comparison documents are optional renders from stronger structured state when a human actually benefits from them.

---

## 9. Mechanical IR

Mechanical IR is deterministic or nearly deterministic and should be richer than the current funnel's simple screen signals.

It should gather any useful structure that is cheap to calculate and likely reusable across multiple editorial consumers.

Candidate fields include:

### Source / addressing

- `scene_id`
- canon chapter
- source path
- source authority commit when needed for historical provenance
- scene source hash
- normalized source hash
- start/end anchors
- paragraph span
- paragraph hashes or IDs when useful
- word / sentence / paragraph counts

### Dialogue topology

- quote/dialogue spans
- likely speaker sequence
- attributed vs unattributed dialogue
- possible attribution/action-owner conflicts
- turn count
- turn-length distribution
- consecutive short-turn runs
- question/answer density
- interruption markers
- repeated confirmation patterns when mechanically detectable

### Language structure

- sentence length statistics
- fragment count
- repeated paragraph/sentence openings
- repeated phrases
- hedge/qualifier counts
- explicit uncertainty phrases
- explanation-after-evidence patterns when mechanically approximable
- exposition-heavy stretches

### Entities / continuity hooks

- character name mentions
- place mentions
- object/prop mentions
- money/value mentions
- dates/time references
- measurements
- explicit chapter/role references
- terms with continuity significance

### Physicality

- action-beat count
- movement/action verb candidates
- object interactions
- body-state mentions
- spatial/preposition signals where useful

### Structural signals

- candidate scene breaks
- location/time transition candidates
- cast-change candidates
- dialogue/narration ratios
- strong mode changes

Mechanical extraction must remain conservative about meaning. It is allowed to be incomplete; it should not fake certainty in areas that require semantic interpretation.

---

## 10. Semantic Scene IR

Cheap semantic compilation enriches the mechanical record.

The purpose is to avoid repeatedly making stronger models rediscover basic scene meaning from raw prose.

Candidate fields include:

### Scene function

- transaction
- investigation
- relationship shift
- recovery
- training
- comedy/social texture
- worldbuilding-through-work
- conflict
- travel/logistics
- setup/payoff
- other project-relevant functions

A scene may have multiple functions.

### Active situation

- location
- active task
- environment pressure
- immediate conflict
- scene question
- turn/hinge
- required outcome
- unresolved outcomes
- must-not-drift constraints

### Character state by participant

- immediate goal
- attention
- emotional state
- knowledge position
- uncertainty
- social/authority position
- physical state when relevant
- what the character is trying not to reveal

### Relationship state

- relationship at entry
- pressure/change during scene
- relationship at exit
- power/leverage movement
- unspoken asymmetry

### Craft / editorial interpretation

- dialogue mode
- exposition mode
- physicality strength
- voice separation
- compression pressure
- performance opportunity
- possible redundancy
- likely source strengths worth protecting

### Continuity inference

- likely new facts
- reinforced facts
- possible contradictions
- state deltas that may matter later

These remain derived unless promoted under an owning authority.

---

## 11. Provenance on semantic fields

Every non-mechanical semantic value must make its epistemic status legible.

At minimum support:

- `observed`
- `inferred`
- `locked_derived`

A field may also carry:

- compiler/model version
- source/dependency hash
- confidence bucket or numeric confidence
- provenance pointer to a successful roundtrip or case when locked

Example:

```json
{
  "value": "Greg is trying to recover bargaining leverage",
  "kind": "inferred",
  "confidence": 0.88,
  "compiler": "scene-semantic/v1"
}
```

Confidence affects routing/review, not truth status.

---

## 12. Semantic conflict handling

Cheap models may disagree across recompilations or with locked derived evidence.

Do not silently overwrite a materially different interpretation merely because it is newer.

When useful, record a conflict such as:

```json
{
  "field": "characters.antonius.goal",
  "previous": "finish cleanup",
  "candidate": "maximize sale value",
  "status": "semantic_conflict"
}
```

A downstream task may ignore the conflict if it is irrelevant.

A stronger reasoning pass should resolve it only when the distinction matters to actual work.

Do not create a global semantic-conflict bureaucracy for low-value disagreements.

---

## 13. PERFORMANCE IR

PERFORMANCE IR remains derived scene-local material.

It should capture the successful categories already proven in the current roundtrip archive while becoming structured and compact.

Per-character candidate fields:

- current state
- performed stance
- attention
- baseline bend
- shift trigger
- action ownership
- silence/withholding behavior
- relevant social register
- scene-specific voice modulation

Scene-level candidate fields:

- performance topology
- who owns which exchange/result
- physical actions that should carry information
- where dialogue should yield to action/interiority
- required beats
- prohibited drift

This is not permanent character state.

A successful performance in one scene is evidence that the behavior worked under those conditions, not a universal character rule.

---

## 14. Universal screenplay render

The performed screenplay/script is a **generated output** by default.

Inputs:

- exact scene prose
- relevant Scene IR projection
- relevant PERFORMANCE IR projection
- current project character/voice authority only when needed
- renderer/compiler version

Output:

- explicit performed script sufficient to expose action ownership, silence, physical behavior, exchange rhythm, and dialogue alternatives

The screenplay should be generated for every scene once the path is cheap enough.

Do not commit every screenplay merely because it was generated.

A chapter screenplay may be assembled transiently from scene renders for human inspection or chapter-level comparison.

---

## 15. Comparison / reverse-edit IR

After screenplay generation, run a cheap comparison against source.

Possible outcomes:

- `source_win`
- `performance_candidate`
- `ambiguous`

The comparator should use diagnostic features to focus attention but may still protect source strengths the diagnostics did not predict.

Candidate compact result:

```json
{
  "verdict": "performance_candidate",
  "possible_wins": [
    {
      "surface": "dialogue",
      "problem": "repeated verbal confirmation",
      "performed_advantage": "physical diagnosis carries distinction",
      "source_span": ["anchor A", "anchor B"]
    }
  ]
}
```

Only plausible candidates pay for the deeper prose judgment needed to decide whether a canon change actually survives.

The goal is not to reduce screenplay runs. The goal is to reduce **expensive reverse-edit judgment**.

---

## 16. Canon patch boundary

The existing exact-boundary patch discipline remains valuable and should be preserved or strengthened.

A surviving change must:

- identify exact current canon source boundaries;
- fail closed when boundaries are missing or ambiguous;
- preserve no-em-dash policy where applicable;
- respect dialogue attribution/ownership validation;
- preserve canon facts, causality, character authority, and continuity;
- update only authoritative prose surfaces declared by the current project architecture;
- never apply merely because a screenplay differs from source.

`SOURCE WIN` is an expected successful outcome.

---

## 17. Dependency fingerprints and cache invalidation

Derived cognition should be reusable only when its meaningful dependencies remain valid.

### Mechanical IR

Depends on:

- scene source hash
- parser/mechanical compiler version

### Semantic Scene IR

Depends on:

- mechanical/source scene hash
- semantic compiler version
- only the project doctrine actually required by that inference

### PERFORMANCE IR

Depends on:

- Scene IR hash
- relevant character/relationship authority hashes when loaded
- PERFORMANCE compiler version

### Screenplay

Depends on:

- source scene hash
- PERFORMANCE IR hash
- screenplay renderer version

Screenplay is normally regenerated rather than treated as expensive cache.

### Comparison

Depends on:

- source scene hash
- screenplay/performance result identity
- comparator version

### Rule

If the dependency fingerprint matches, do not ask an AI to reconsider the same semantic problem without a reason.

If a dependency changes, invalidate only the lowest affected layer and its dependents.

Example:

- punctuation/source edit -> mechanical and all downstream scene layers may need recheck;
- character doctrine change -> mechanical remains valid, PERFORMANCE may invalidate;
- screenplay renderer change -> Scene/PERFORMANCE IR remain valid;
- unrelated chapter change -> no invalidation.

---

## 18. Task-specific compiled views

Downstream workers should request a **view**, not manually read every stored field/file.

The view may be assembled transiently by code or a worker. It does not need to be committed.

### PERFORMANCE view

Likely includes:

- exact source slice
- cast
- goals/attention
- state in
- knowledge asymmetry
- relationship pressure
- active task
- physical beats
- required outcome
- must-not-drift
- dialogue topology

### Dialogue view

Likely includes:

- exact source slice
- speaker sequence
- attribution anomalies
- turn lengths
- rapid-response runs
- character voice/state projection
- relationship/mood
- action ownership

### Continuity view

Likely includes:

- source anchors
- entities
- money/measurements
- new/reinforced facts
- state changes
- unresolved facts
- possible contradictions

### Illustration view

Likely includes:

- cast
- location
- props
- physical actions
- body state
- relationship geometry
- scene turn
- visual anchors

The stored record can be rich. Context packets stay task-sized.

---

## 19. Relationship to successful PERFORMANCE archive

The current `state/editorial/performance-roundtrip/` five-file archive is **proven reference architecture**, not immediate deletion material.

It currently preserves successful cases using:

- `source.lock.json`
- `dramatic.md`
- `performance.md`
- `screenplay.md`
- `comparison.md`

The new representation must first prove it can preserve/reconstruct the useful information in known successful cases, especially canon 007, 013, and 018.

### Golden equivalence test

For each known successful case:

1. compile current/historical source through the new scene representation;
2. verify the rich Scene/PERFORMANCE IR contains the dramatic and performance distinctions that mattered;
3. render a screenplay from the structured input;
4. confirm a capable reverse editor can recover the same class of reader-facing improvement without loading the old five Markdown documents;
5. preserve any unique provenance the old archive still carries.

Only after this succeeds may future successful cases use a more structured archival format by default.

Old successful evidence may remain as historical case law even after its operational storage role retires.

---

## 20. Replacement-first cleanup protocol

The universal PERFORMANCE compiler is explicitly intended to simplify the backend over time.

Do not perform cleanup merely because a new abstraction exists.

For each older editorial surface, ask:

1. What live job does this currently perform?
2. Does the evolved PERFORMANCE production funnel now perform that job more cheaply or reliably?
3. Can current consumers be rerouted to the new scene/view interface?
4. Is there unique authority, provenance, case law, recovery evidence, or craft doctrine that the new representation does not preserve?
5. Has replacement behavior been tested on real work?

Then classify:

- **KEEP ACTIVE** — new primitive does not replace the live job.
- **REROUTE / RETIRE OPERATIONAL ROLE** — new primitive owns the job; old artifact remains reference/case law.
- **MIGRATE RESIDUE THEN DELETE** — old surface is operational duplication after unique value is moved/preserved.
- **NO ACTION** — cleanup would save little or evidence is insufficient.

The rule is:

**PROVE REPLACEMENT -> REROUTE CONSUMERS -> PRESERVE UNIQUE RESIDUE -> RETIRE THE WEAKER MECHANISM**

Never delete first and hope the new abstraction was equivalent.

---

## 21. Likely future cleanup targets

These are hypotheses, not pre-approved deletions.

### 21.1 Giant PERFORMANCE production batch records

Current monolithic batch JSON is useful proof but should not become the long-term per-scene AI interface.

If small scene records + chapter manifests fully replace coverage, validation, verdict, and patch routing, retire giant batch files from active generation.

### 21.2 Repeated dramatic/performance Markdown generation

If structured IR preserves all operational semantics and human-readable documents can be rendered when needed, future `dramatic.md` / `performance.md` generation may become optional render behavior rather than mandatory storage.

Historical successful archives remain evidence until migration proves otherwise.

### 21.3 Duplicate dialogue extraction

If dialogue passes currently rediscover speaker topology, question density, short-turn chains, or attribution candidates independently, move those mechanical observations into the shared scene representation and have dialogue consumers request the dialogue view.

Do not move dialogue-specific craft judgment into the generic compiler merely because mechanical extraction is shared.

### 21.4 Duplicate illustration extraction

If illustration machinery independently rediscovers cast, props, location, body state, blocking, or action ownership, prefer the shared scene/visual view where it is accurate enough.

Illustration-specific selection and aesthetic judgment remain local to the visual pipeline.

### 21.5 Large editorial continuation/state files

If large files mostly preserve reconstructible progress, repeated source facts, or mechanical scene state, shrink or retire those portions after the scene compiler becomes the stronger owner.

Keep unique editorial doctrine and hard-earned judgment.

---

## 22. Failure handling

### Missing/ambiguous source anchors

Fail closed. Do not apply patches or reuse a cache entry against uncertain source identity.

### Ambiguous scene continuity

Mark for scene re-identification. Do not silently map historical semantics onto a different scene.

### Malformed IR

Schema validation fails the compile. Do not partially trust malformed structured state.

### Semantic inference failure

Preserve mechanical IR and mark semantic layer unavailable/stale. Downstream high-value tasks may read exact source directly rather than blocking the whole chapter.

### PERFORMANCE failure

Source remains source. A failed derived transform cannot damage canon.

### Screenplay generation failure

Mark render failure and continue other independent scenes when safe. Do not reinterpret render failure as `SOURCE WIN`.

### Comparison uncertainty

Use `ambiguous`; escalate only if the scene warrants deeper review.

---

## 23. Testing strategy

The implementation must be test-driven where code is involved.

### Deterministic parser tests

Cover:

- prose extraction
- paragraph indexing
- dialogue topology
- regex signals
- source anchors
- hashing
- scene manifest validation
- split/merge lineage validation

### Incremental invalidation tests

Prove:

- unrelated chapter edits do not invalidate a scene;
- paragraph insertion before a scene does not automatically destroy scene identity;
- source change invalidates only the affected scene/downstream layers;
- renderer-version change does not force semantic recompilation;
- character/performance dependency change preserves valid mechanical IR.

### Patch safety tests

Preserve current exact-boundary behavior and stale-edit rejection.

### Golden successful-roundtrip tests

Use 007, 013, and 018 as known successful evidence.

The goal is semantic equivalence, not byte-for-byte reproduction of the historical screenplay.

### Source-win tests

Include scenes where current prose is already better than performed alternatives. Universal screenplay generation must not create pressure to edit merely because a transform ran.

### AI-interface retrieval tests

Demonstrate that a worker can request one scene/task view without loading giant chapter/batch/editorial files.

---

## 24. Rollout sequence

This design should be implemented in the same existing PR/branch only after the current branch is reconciled with newer `main` and a fresh implementation plan is approved.

Recommended sequence:

### Phase A — reconcile existing PR #143

Preserve useful current work:

- exact patch application
- batch validation concepts
- proven source-win/change-survives examples
- workflow/test coverage that remains relevant

Do not blindly merge stale branch state over newer `main`.

### Phase B — scene manifest + mechanical IR

Introduce stable scene identity, deterministic extraction, hashes, rich mechanical fields, and small scene records inside `performance-production`.

No canon edits required to prove this phase.

### Phase C — semantic Scene IR + provenance

Add cheap semantic enrichment and provenance/confidence handling.

Calibrate against known chapters and existing successful archives.

### Phase D — structured PERFORMANCE IR + universal screenplay render

Generate performed screenplay for every test scene/chapter.

Screenplay remains disposable by default.

### Phase E — cheap comparator + selective deep reverse edit

Move expensive judgment after universal screenplay generation.

Apply surviving edits through existing canon-safe patch boundary.

### Phase F — replacement audit

Use real evidence to reroute/remove older duplicate extraction/storage jobs one at a time.

Do not bundle a broad cleanup purge into the compiler launch.

---

## 25. Success criteria

The architecture succeeds when:

1. **Universal screenplay is economically routine.** Running PERFORMANCE/script rendering on every scene is cheaper/simpler than manually screening scenes out first.
2. **Exact canon stays authoritative.** No derived record can silently override current prose.
3. **AI context gets smaller.** A worker can retrieve a task-sized scene projection instead of swallowing giant Markdown/batch files.
4. **Cheap extraction gets richer.** Mechanical and cheap semantic layers expose enough reusable structure that downstream systems stop rediscovering the same facts.
5. **Incremental compilation works.** Unchanged scene cognition is reused; small edits do not trigger manuscript-scale re-analysis.
6. **Source wins remain common and acceptable.** Running a screenplay does not create an edit quota.
7. **Successful roundtrip evidence remains reproducible and inspectable.** The new representation preserves what mattered in proven cases.
8. **Backend conceptual surface shrinks over time.** At least one older duplicate job can be safely rerouted/retired after the new primitive proves itself.
9. **No new root lane or parallel compiler appears.** This remains the existing PERFORMANCE production funnel becoming better.

---

## 26. Non-goals

Do not:

- create a universal story database;
- replace canon prose with semantic JSON;
- make every inference permanent character state;
- build SQLite merely because querying might someday be useful;
- invent a separate blob store when Git already provides immutable blob identity;
- archive every generated screenplay;
- create a giant prompt/context packet containing every field;
- encode semantic editorial judgment into increasingly complex regex;
- delete old machinery before replacement is proven;
- make scene compiler logic the owner of project-specific dialogue, visual, or continuity craft rules;
- require maximum reasoning for every scene.

---

## 27. Core rules to preserve

**Store rich reusable cognition. Compile narrow working context.**

**Wide at rest. Narrow in context.**

**Regex/parser finds syntax. Models interpret semantics.**

**Screenplay is a generated render, not story authority.**

**Cache expensive understanding. Recompute cheap facts.**

**Chapter is the command unit. Scene is the cache/invalidation unit.**

**Run the cheap transform broadly. Spend deep reasoning only where the transformed comparison earns it.**

**A stronger primitive should retire weaker duplicate jobs after proving replacement.**
