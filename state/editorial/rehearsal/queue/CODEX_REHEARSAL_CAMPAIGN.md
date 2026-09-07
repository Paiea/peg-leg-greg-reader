# Codex REHEARSAL Campaign Worker Contract

This is an execution contract over the existing REHEARSAL lane. It does not create a new story authority.

## Scope

Work exactly one currently claimed queue batch from `state/editorial/rehearsal/queue/canon-061-491.json`.

Default sequence is serial: 061-070, 071-080, and so on through 481-490, then 491.

Do not precompute later batches. Each batch reads the prose authority settled by the preceding batch.

## Required inputs

Read:

- exact current `chapters/NNN.html` for the claimed batch
- enough neighboring canon to preserve continuity
- current REHEARSAL actor/casting state
- `state/editorial/rehearsal/relationship-memory.json`
- fresh PERFORMANCE/REHEARSAL evidence when available
- `docs/superpowers/specs/2026-09-07-rehearsal-autonomous-campaign-queue-design.md`
- `state/editorial/CODEX_EXECUTION_POLICY.md` when present on current authority

Use deterministic extraction and current source HTML before model inference.

## Heat

Use the approved 051-060 boundary-hunt calibration.

Actors may materially reshape local unlocked surfaces:

- rewrite short exchanges substantially
- expand or contract dialogue
- interrupt, overlap, withhold, redirect, or reorder local responses
- replace explanation with silence or behavior
- alter local blocking and task continuation
- let object use and physical action carry subtext
- change who closes an exchange
- propose plausible entrances/exits when locked reality allows them
- let Nico perform richer private cognition than final prose must print

There is no edit quota. SOURCE WIN is valid.

## Hard locks

Do not change:

- plot outcome
- established facts
- who knows what
- causality
- chronology
- economics
- earned competence
- injury, mobility, or physical state
- major earned relationship milestones
- unresolved mystery state

Truth is constrained. Staging is negotiable.

## Repetition rule

Repeated words, objects, gestures, or motifs are not automatically synthetic tics.

Keep repetition when it escalates irritation, pressure, rhythm, fixation, obsession, or payoff. Reject it only when it reads as model recursion without new scene-local work.

## Actor entrance rule

A character absent from source choreography may enter a rehearsal when geography, chronology, simultaneous state, knowledge, and other hard locks make the presence possible.

Record the proposal as staging evidence. Do not treat source absence alone as a continuity failure.

## Namespace warning

Canon Kellan is the watch mage introduced in canon 029.

The synthetic actor historically named Kellan plays Jorren. Until that synthetic actor is explicitly renamed, identify that performer as `Jorren actor`, never bare `Kellan`.

## Writable prose surfaces

A prose candidate may use only actual writable surfaces such as:

- dialogue
- paragraphing
- movement
- blocking
- silence
- interaction_timing
- reaction_placement
- object_handling
- local_exchange_shape
- tone
- internal_dialogue
- narration_rhythm
- attention_order
- sensory_emphasis
- memory_intrusion

`relationship_behavior` and `speaker_legibility` are discovery categories, not writable surfaces.

## Boundary-hunt rejection evidence

When a take is too hot, record one or more labels rather than silently lowering campaign heat:

- `overacted_theatre`
- `quip_inflation`
- `gratuitous_interruption`
- `prop_recursion`
- `movement_saturation`
- `overcompression`
- `character_caricature`
- `pov_crowding`
- `useful_repetition_destroyed`
- `cast_expansion_rejected`

## Output

Write exactly one schema-bound result to:

`state/editorial/rehearsal/queue/current-worker-result.json`

Use schema:

`state/editorial/rehearsal/queue/worker-result.schema.json`

Every chapter in the claimed batch must appear exactly once in order. Each chapter must have a disposition, compact discoveries, and rejected-hot evidence when relevant.

Only prose candidates that survive actor preference, dramatic-lock check, reader check, and novel suitability belong in `candidates`.

For every candidate, copy `before` from literal current HTML. Never reconstruct HTML paragraph boundaries from rendered retrieval. No fuzzy anchors.

Do not edit `chapters/*.html` directly. Committing the worker result triggers the serialized GitHub integration workflow, which is the only prose-write path.

## Stop conditions

Stop and leave the batch blocked when:

- hard story authority is ambiguous
- exact current prose cannot be established
- a required source authority is stale
- a material continuity conflict cannot be resolved from current canon
- ordinary worker execution fails twice total, initial attempt plus one retry

Never skip ahead to a later batch.
