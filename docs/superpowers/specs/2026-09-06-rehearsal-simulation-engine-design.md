# REHEARSAL Simulation Engine Design

## Purpose

Evolve the existing faithful PERFORMANCE pipeline into a reusable REHEARSAL system that deliberately simulates scenes rather than merely certifying the source.

The system should use current canon plus existing scene understanding to let characters move, speak, pause, interrupt, react, handle objects, and occupy space in ways that may differ substantially from the source while preserving locked story truth. Useful discoveries can then return to prose, accumulate into evidence-backed character learning, and feed future illustration work.

The intended editorial progression is:

`canon prose -> faithful scene understanding -> rehearsal simulation -> discoveries -> prose return -> validated canon candidate -> downstream visual use`

The central rule is:

> Preserve canon truth, not canon choreography.

## Existing authority and reuse

The repository already contains the expensive substrate this design should reuse rather than replace:

- canonical prose in `chapters/*.html`
- scene IDs, segmentation, mechanical IR, dependency fingerprints, semantic/performance layers, and task views in `scripts/performance_production_funnel.py`
- successful PERFORMANCE roundtrip evidence under `state/editorial/performance-roundtrip/`
- compact whole-campaign PERFORMANCE records under `state/editorial/performance-production/`
- dialogue ownership and variance rules in `state/editorial/DIALOGUE_VARIANCE_PASS_STATE.md`
- durable but non-authoritative character guidance in `state/CHARACTER_BIBLE.md`
- exact-source patching and dialogue rewrite helpers already present under `scripts/`

PR #159 completes campaign-history PERFORMANCE review coverage across canon 1-491. REHEARSAL should consume that existing work where fresh enough rather than recomputing faithful understanding by default.

No new story authority is introduced.

## Authority model

### Canon

Canonical chapter prose remains the only story authority.

### Dramatic lock

A rehearsal receives a derived dramatic lock containing only what cannot move without changing the story:

- state in
- required scene result
- state out
- established facts
- knowledge boundaries
- relationship state
- physical limitations and current bodily state
- location
- materially important objects
- active task
- causality that must survive
- required information or lines only when genuinely necessary

### Faithful PERFORMANCE baseline

The existing PERFORMANCE layer remains the faithful baseline. It answers:

> What is actually happening in the current source scene?

It is not renamed retroactively because existing evidence was generated under that contract.

### REHEARSAL

REHEARSAL is explicitly exploratory. It answers:

> Given the locked truth, what happens if these particular characters actually play the scene?

REHEARSAL may diverge from source wording and choreography. Divergence is not itself a failure.

### Editorial return

Only an editorial return may propose changed prose. A rehearsal never writes canon directly.

## Rehearsal freedom

Unless the dramatic lock says otherwise, rehearsal may change:

- exact dialogue wording
- amount of dialogue
- sentence length
- pauses
- silence
- interruption
- overlap
- gestures
- action beats
- blocking
- minor beat order
- physical business
- object handling
- who looks at whom
- how long a character takes to answer
- whether a response is verbal or behavioral
- tags and attribution opportunities

Rehearsal may not silently change:

- plot outcome
- established fact
- who knows what
- earned competence
- injury or mobility state
- relationship milestone
- chronology
- economic fact
- location continuity
- an unresolved mystery into a solved one
- hidden publication state into story meaning

## Actor model

An actor is initially a compiled task view, not a persistent autonomous agent.

Each actor packet contains only the scene-relevant subset of:

- identity
- current bodily state
- relationship-specific context
- canon observations
- promoted behavioral tendencies
- current emotional or practical pressure
- current objective
- domain responsibility
- knowledge and ignorance boundaries
- relevant visual casting reference
- anti-caricature warnings

The actor instruction is:

> Do not write a good line for this character. Play this person in this situation.

Actor packets must vary by scene. A character in a work scene should not receive the same task packet as the same character in a domestic, romantic, combat, or recovery scene.

## Character learning states

Rehearsal can produce character evidence in four states.

### OBSERVED

Directly supported by current canon.

### INFERRED

A strong interpretation of current canon with explicit provenance and confidence.

### REHEARSAL_HYPOTHESIS

A behavior or relationship tendency repeatedly useful in simulation but not yet independently established by canon.

### PROMOTED_TENDENCY

A derived tendency supported by enough independent current-canon evidence to be included automatically in future actor packets.

Promotion is semi-automatic.

A rehearsal hypothesis may accumulate freely, but it cannot become a canon fact. Identity-defining or consequential promotion should remain reviewable.

### Anti-recursion rule

Synthetic evidence cannot validate itself.

If a rehearsal invents a tendency and future rehearsals reproduce it because that tendency was included in their actor packet, those later rehearsals do not count as independent support.

Only independent current-canon evidence or editorially accepted prose returns can increase promotion support.

## Rehearsal run

### Stage 1: Build rehearsal lock

Compile the scene's dramatic lock from existing fresh semantic/PERFORMANCE evidence plus current canon anchors.

If existing evidence is stale, recompute only the affected scene.

### Stage 2: Cast actor packets

Build scene-local actor packets for every participant who materially affects the scene.

Background participants may remain lightweight unless they own a line, action, decision, or important visual beat.

### Stage 3: Ensemble take

Generate one integrated ensemble rehearsal by default.

The rehearsal should represent:

- explicit speaker ownership
- explicit action ownership
- movement
- pauses and silence
- interruptions when natural
- object use
- physical response
- relationship pressure
- current task continuation
- character-specific dialogue shape
- Greg interiority as a separate channel when useful

The default objective is not to maximize dialogue volume. It is to maximize performed specificity while preserving the dramatic lock.

### Stage 4: Targeted second take

A second take is conditional, not automatic.

Possible directed modes:

- `voice`: maximize character-specific response without gimmicks
- `physical`: let movement, objects, task work, blocking, silence, and reactions carry more of the scene
- `pressure`: increase the felt social or emotional pressure without changing outcome
- `minimal`: test whether the scene works with less speech
- `expansive`: allow more natural verbal space when source dialogue is implausibly compressed

The scheduler should request a second take only when critics or route heuristics identify a reason.

## Critics

Critics are narrow consumers. They should not all rewrite prose.

### Reader critic

Reads source prose cold and reconstructs speaker ownership.

Flags:

- attribution uncertainty
- speaker reassignment or backtracking
- another character's action visually attached to a speaker's line
- ambiguous speaker re-entry
- long untagged alternation that becomes fragile
- three-plus speaker ambiguity

The standard is first-reader legibility, not technical grammatical correctness.

### Actor critic

Checks whether rehearsal behavior is supported by the actor packet and current scene state.

Rejects generic cleverness, unsupported omniscience, domain leakage, and caricature.

### Voice discriminator

May strip names from selected exchanges and estimate whether dialogue and behavior are character-distinct.

Interchangeability is a candidate signal, not an automatic failure.

### Director critic

Checks the dramatic lock and rejects or quarantines discoveries that changed canon truth.

### Novel critic

Checks whether a performed discovery belongs in first-person PLG prose.

A good rehearsal beat is not automatically good narration.

## Discovery ledger

The first durable output of a rehearsal is a compact discovery ledger, not replacement chapter prose.

Discovery kinds include:

- `movement`
- `dialogue_expand`
- `dialogue_contract`
- `speaker_legibility`
- `voice`
- `interaction_timing`
- `blocking`
- `object_behavior`
- `relationship_behavior`
- `character_hypothesis`
- `visual_beat`
- `source_win`

Each discovery records:

- scene ID
- source authority
- exact source anchors
- rehearsal version
- involved characters
- discovery kind
- concise finding
- supporting take IDs
- critic support
- dramatic-lock status
- candidate usefulness
- provenance class

## Editorial return

Novelization receives:

- exact current source scene
- dramatic lock
- accepted rehearsal discoveries
- Greg POV constraints
- dialogue ownership rules
- relevant actor packets
- current prose-rhythm guidance

It may rewrite the local scene where rehearsal earned the change.

The system should be materially less conservative about dialogue scaffolding than the prior PERFORMANCE campaign.

Soft surfaces include:

- tags
- paragraph breaks
- action ownership
- reaction placement
- movement
- timing
- local dialogue shape
- minor exchange structure

Hard surfaces remain:

- plot
- facts
- knowledge
- causality
- major relationship change
- earned competence

After novelization, run a lightweight rehearsal/check on the candidate to verify that the proposed prose preserved the useful discovery rather than smoothing it away.

## Visual casting agent

Visual casting is a first-class derived input to REHEARSAL and later illustration work.

It is not final art and is not canon authority.

### Purpose

A visual casting reference helps the actor packet maintain a stable sense of physical identity, posture, presence, age, body type, costume silhouette, and visual contrast with other characters.

### Canon visual facts

The casting agent must separate locked canon facts from invented visual interpretation.

Examples of user-approved anchors for the initial cast:

- Greg: male, nineteen in second life, early-book left BKA with no peg until later canon establishes it, scruff/beardish look, not pretty-boy polished, disheveled intensity, slightly feral or theatrical presence, intense eyes, practical worn-in presentation
- Lyssa: tall, thin/lithe Black woman with Afro-textured or afro-ish hair; visual energy may loosely echo the user's Alyssa reference without requiring literal identity
- Antonius: Black
- Alden: islander boy; should not visually collapse toward Greg
- all other characters: casting agent may interpret freely within canon facts

### Casting autonomy

The casting agent is encouraged to invent visual identity where canon is silent.

The user does not need to art-direct every character.

A generated casting choice is derived reference and may be recast later.

### Distinctness objective

The cast must remain distinguishable at thumbnail size, not merely in high-resolution portraits.

The casting agent should optimize across:

- face shape
- skin tone
- hair silhouette
- age
- height and build
- posture
- costume silhouette
- facial-hair silhouette
- expression energy
- occupation or task cues

The system should detect visual collisions and request recasting when two recurring characters become too similar.

Important collision examples already noticed by the user:

- Alden should not resemble Greg
- Marek should not resemble Greg
- Davin should not resemble Arlo
- Hara should not resemble Lyssa

These are calibration examples, not permanent pairwise bans.

### Casting packet

A character casting packet contains:

- locked visual facts
- free visual interpretation
- one primary identity reference
- optional secondary work-mode or three-quarter reference
- silhouette description
- distinguishing markers
- prohibited collisions
- current era/state validity
- source/provenance
- quality score
- thumbnail-distinctness score
- status: `candidate`, `selected`, `demoted`, `archived`

### Era-sensitive continuity

Visual references must be valid for the scene era.

A later prosthetic, haircut, scar, costume, injury state, or other appearance change cannot leak backward merely because it appears in a strong reference image.

For Greg specifically, the initial casting system must not make a peg leg the early default.

## Existing image policy

Current illustration assets are not protected merely because they exist.

The visual pipeline may classify existing images as:

- `keep`
- `demote`
- `archive`

Strong existing images can remain selected references.

Images that are off-model, misleading, visually collision-prone, stale, or grounded in weaker prior scene understanding should be demoted or archived rather than allowed to contaminate future casting and illustration selection.

No bulk deletion is required for the first REHEARSAL pilot.

## Rehearsal to illustration handoff

REHEARSAL discoveries may emit visual beats containing:

- decisive action
- blocking
- object use
- physical relationship
- silent reaction
- who is looking where
- environment interaction
- bodily limitation or mobility state
- emotional pressure visible in posture or action

Illustration generation remains a separate consumer.

Final scene art should validate against current canon and current-era casting references before generation.

## Persistence strategy

Avoid a repository full of disposable synthetic screenplays.

Persist:

- compact rehearsal discovery ledgers
- actor evidence needed for promoted tendencies
- selected visual casting metadata
- exact rehearsal evidence behind surviving prose edits
- freshness/dependency metadata

Do not persist by default:

- every raw rehearsal take
- every critic chain-of-thought
- redundant screenplay variants
- failed or uninteresting takes

A raw take may be archived when it directly explains a surviving edit or a consequential character promotion.

## Freshness and invalidation

Rehearsal artifacts depend on:

- source scene hash
- dramatic-lock compiler version
- actor-packet version
- character evidence version
- selected visual-casting reference version
- rehearsal compiler version

A source scene change stales only dependent rehearsal work.

A recast should stale visual-dependent rehearsal outputs only when visual identity materially affected the discovered behavior. Pure dialogue ownership evidence should not be invalidated by an unrelated portrait change.

## Routing and cost

Use the lightest worker that preserves quality.

Suggested routing:

- deterministic code: segmentation, source hashes, dependency tracking, collision metadata, exact patch validation
- Instant-level semantic worker: actor packet generation, baseline rehearsal, reader critic, obvious ownership checks, discovery extraction
- higher-reasoning worker: ambiguous scene truth, consequential voice changes, character promotion disputes, difficult ensemble scenes, final editorial adjudication

The scheduler should spend more on:

- multi-character ensemble scenes
- high dialogue density
- broken alternation
- major recurring-character interactions
- scenes with strong voice-collision risk
- scenes with visual staging importance

It should spend less on:

- Greg-alone bookkeeping or reflection
- mechanically clear two-person exchanges
- scenes with very little interaction

## Pilot

Before a whole-canon REHEARSAL campaign, run a bounded pilot over existing fresh screenplay/PERFORMANCE evidence.

Pilot goals:

1. prove reuse of existing faithful evidence without full recompile
2. prove actor packets are scene-local
3. prove one ensemble rehearsal can generate useful movement/dialogue/ownership discoveries
4. prove targeted second takes are conditional
5. prove a reader critic catches real attribution ambiguity
6. prove character hypotheses do not self-promote
7. prove casting references are era-sensitive
8. prove low-resolution distinctness can reject visual collisions
9. produce at least one novelization candidate that survives the lightweight recheck, or produce a legitimate SOURCE WIN without forcing edits

Suggested pilot cast:

- Greg
- Antonius
- Hessa
- Lyssa
- Alden
- Arlo
- selected theatre ensemble members where useful

Suggested pilot scenes should include:

- one Antonius work/task scene
- one Hessa testing scene
- one Greg/Lyssa domestic or relationship scene
- one Alden scene
- one Arlo scene
- one three-plus speaker theatre scene

Do not require all pilot scenes to change.

## Success metrics

The pilot should report:

- scenes rehearsed
- faithful evidence reused vs recomputed
- actor packets built
- primary takes
- targeted second takes
- speaker-legibility findings
- movement discoveries
- dialogue expansion/contraction discoveries
- voice discoveries
- character hypotheses
- visual collisions detected
- recasts requested
- novelization candidates
- surviving prose candidates
- SOURCE WIN count
- false-positive or lock-violation count

A successful pilot is not defined by a high edit rate. It is defined by producing genuinely new performed information that the prior faithful PERFORMANCE pass did not expose.

## Failure modes

### Faithful paraphrase loop

If rehearsal merely restates source choreography, the contract is too conservative. The director must explicitly permit divergence in unlocked surfaces.

### Dialogue inflation

More dialogue is not automatically better. Rehearsal should allow expansion and contraction.

### Character gimmick drift

Actor packets should use tendencies under conditions, not catchphrase/fixed-cadence rules.

### Synthetic self-confirmation

Rehearsal hypotheses cannot count their own descendants as independent evidence.

### Visual canon leakage

Generated appearance details cannot become canon facts. Era-sensitive references must prevent later states from leaking backward.

### Cast homogenization

High-resolution beauty is not enough. Thumbnail-level distinctness is a hard casting objective.

### Subsystem duplication

REHEARSAL should extend scene IR, provenance, dialogue ownership, character evidence, and illustration reference machinery rather than creating competing authority stores.

## Non-goals for the first implementation

Do not initially build:

- persistent autonomous character agents
- real-time multi-agent chat between actors
- speech synthesis
- 3D blocking
- full-book image regeneration
- automatic canon writes
- automatic deletion of existing images
- a giant universal character database separate from existing project state

The first implementation should prove the simulation loop and visual casting interface with the smallest reusable architecture.

## Rollout

1. implement rehearsal contracts and persistence schema
2. implement actor packet compilation and character-evidence provenance
3. implement casting packet schema, era validation, and collision checks
4. implement ensemble rehearsal and conditional directed take routing
5. implement critics and discovery extraction
6. implement novelization handoff and lightweight candidate recheck
7. run bounded pilot over existing PERFORMANCE/screenplay evidence
8. review pilot output and calibrate
9. only then schedule broader canon/Showcase rehearsal campaigns
10. after prose/dialogue stabilizes, use rehearsal/casting outputs to drive illustration rehabilitation
