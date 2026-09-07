# REHEARSAL Modes, Relationship Memory, Take Variance, and Greg Inner Voice

Status: approved design, implementation pending

Branch: `editor/rehearsal-simulation-engine`

## Purpose

Extend the existing REHEARSAL system without creating a parallel engine.

The next REHEARSAL contract adds four capabilities:

1. explicit `FAITHFUL`, `FREE`, and `DIRECTED` rehearsal modes
2. relationship-local performance memory with separate supported and hypothesis lanes
3. take-variance testing for disputed or high-leverage scenes
4. an explicit `BODY / VOICE / INNER VOICE` performance model for Greg, played by Nico

The existing central rule remains:

> Preserve canon truth, not canon choreography.

The calibration decision is also promoted into the normal operating philosophy:

> Let movement, dialogue, tone, and Greg's live thought generate prose. Do not make prose prove that a rehearsal happened.

## Authority

Canonical prose remains the only story authority.

Hard story surfaces remain locked during rehearsal and prose return:

- plot outcome
- established facts
- knowledge boundaries
- causality
- chronology
- economics
- major relationship state
- injury and physical state
- earned competence
- unresolved mystery state

REHEARSAL may freely explore soft prose surfaces when the dramatic lock is preserved:

- dialogue wording and amount
- movement
- blocking
- silence and pauses
- interruptions
- object handling
- local beat order
- paragraphing
- interaction timing
- tone
- Greg's live internal dialogue

## Rehearsal modes

### FAITHFUL

Purpose: control take.

FAITHFUL plays the current scene close to source wording and choreography. It establishes what the source already does well and provides a comparison baseline for later takes.

FAITHFUL is not the preferred production take. It is the control condition.

Expected behavior:

- preserve source beat order unless clarification requires otherwise
- preserve most dialogue wording
- preserve most blocking
- expose speaker and action ownership clearly
- surface existing strengths and ambiguities

### FREE

Purpose: default creative take.

FREE is the normal production rehearsal mode.

The dramatic lock remains strict, but actors may substantially reshape soft prose surfaces. Actors are expected to play the scene rather than repair individual sentences.

FREE may alter:

- dialogue wording, amount, and rhythm
- movement and blocking
- pauses and silence
- object use
- local interaction order
- response timing
- paragraph rhythm
- Greg's spoken and internal performance

A FREE take may become the primary generative model for an editorial return when critics prefer it to source.

The previous `overtuned_calibration` run is treated as an upper-bound reference, not as a separate creative philosophy. High actor authority is now normal, while motif recursion and stage-direction density are controlled by critics rather than by broadly reducing actor freedom.

### DIRECTED

Purpose: answer a specific editorial question.

DIRECTED is not simply a stronger FREE take. It receives an explicit direction describing what to test.

Examples:

- make the exchange more physical
- reduce spoken dialogue
- increase social pressure without changing outcome
- separate two voices that sound interchangeable
- strengthen Greg's inner performance
- test whether silence carries the beat better than a reply
- test a more expansive conversational rhythm

Every DIRECTED take records its direction so its results are not mistaken for neutral evidence.

## Relationship-local performance memory

Actor memory is keyed to a relationship context, not only to the actor globally.

Examples:

- Desmond playing Antonius opposite Greg
- Desmond playing Antonius opposite Arlo
- Mara playing Hessa opposite Greg
- Noa playing Alden opposite Greg

The same actor may therefore carry different expectations, pressures, rhythms, and behavioral tendencies depending on the scene partner.

### Supported lane

High-trust relationship memory.

May contain:

- direct current-canon observations
- accepted prose returns
- promoted tendencies supported by independent evidence
- user-authored relationship anchors

Supported memory may be compiled automatically into future actor packets when scene-relevant.

### Hypothesis lane

Low-trust synthetic memory.

May contain:

- useful rehearsal discoveries
- recurring actor interpretations
- relationship behaviors that repeatedly improve takes but are not independently supported

Hypothesis memory may influence future takes, but it must remain visibly labeled as synthetic.

### Anti-self-confirmation

A hypothesis cannot become more authoritative merely because future rehearsals repeat it after receiving it in their packets.

Only independent canon evidence or accepted prose returns can increase support toward promotion.

Repeated synthetic use is not independent evidence.

## Take-variance testing

Take variance is used for disputed, ambiguous, or high-leverage scenes.

The goal is not to generate many pretty alternatives. The goal is to separate stable character behavior from one-off improvisation.

A variance set uses the same dramatic lock and comparable actor packets while changing the take conditions in controlled ways.

All takes in one variance group receive the same frozen actor-memory snapshot and cannot see sibling take outputs before comparison. A take cannot use another take in the same variance group as evidence or context. This preserves meaningful independence inside the test.

A typical disputed scene may receive:

1. one FAITHFUL control
2. one FREE take
3. one additional FREE take with fresh stochastic variation
4. one DIRECTED take if a specific editorial question remains

The comparison asks:

- which behaviors recur across independent takes?
- which dialogue shapes remain character-specific?
- which discoveries depend on one direction only?
- which gestures are incidental?
- which motifs recur only because actor memory fed them back in?
- which version produces the strongest novel prose while preserving the dramatic lock?

Stable behavior across independent takes is stronger rehearsal evidence than a single successful gesture, but it still does not become canon truth without independent support.

## Greg performance model

Greg is the only character whose inner performance is directly available to the reader.

Nico therefore plays Greg through three simultaneous channels.

### BODY

What Greg physically does.

Includes:

- movement
- posture
- object interaction
- hesitation
- physical avoidance
- embodied reaction

### VOICE

What Greg says aloud.

Includes:

- dialogue
- interruptions
- deliberate omissions
- jokes
- strategic phrasing
- lies and half-truths

### INNER VOICE

What Greg thinks in real time.

INNER VOICE is treated as dialogue, not generic exposition.

It may:

- interrupt itself
- branch associatively
- contradict Greg's spoken line
- suppress a joke
- misread another character
- revise an interpretation
- remember something at the wrong moment
- route around an emotion
- jump ahead strategically
- become excited when a system becomes legible
- become fragmentary under pressure

Only Nico authors Greg's internal performance.

Other actors may cause the stimulus that produces the thought, but they do not author Greg's internal response.

The novelizer synthesizes BODY, VOICE, and INNER VOICE into first-person prose. It does not need to retain every performed thought. Rehearsal may contain substantially more internal activity than the final prose shows.

## Editorial return and production authority

The default production philosophy now follows the high-authority calibration more closely.

An actor-preferred soft-prose return may be applied on an isolated editorial branch when all required gates pass:

- dramatic lock preserved
- reader legibility passes
- exact source is still current
- target branch is not `main`
- changed surfaces are soft prose only
- no hard story surface changes
- provenance is recorded

Scene-scale prose rebuilding is allowed when the performed result is clearly stronger.

Edit distance from source is not a quality criterion.

The comparison question is:

> Does the candidate preserve every locked truth while producing a better reading experience than source?

## Critics added by the calibration

### Motif recursion critic

Detects when a useful behavioral principle is being reduced to a repeated prop, gesture, or signature move.

Example failure:

- Antonius correctly owns transactional space
- the engine then repeatedly translates that into touching the ledger

The critic should preserve the principle and penalize literal repetition.

### Stage-direction density critic

Detects prose that over-externalizes cognition or reads like transcription of blocking.

Movement earns prose space when it materially improves:

- timing
- ownership
- pressure
- legibility
- character specificity

Not every internal reaction should become a gesture.

### Inner-voice critic

Checks Greg's live thought for:

- voice specificity
- excessive explanatory neatness
- retrospective analysis masquerading as immediate thought
- repeated joke cadence
- thought density that smothers scene action
- thoughts that merely restate visible behavior

The critic should prefer live, interruptible cognition over polished postmortem narration when the scene is happening in real time.

## Default run order

The normal sequence becomes:

`FAITHFUL control -> FREE take -> critics -> editorial decision`

If the FREE take is clearly stronger and all gates pass:

`FREE -> novelization -> validated prose return`

If the result is disputed or high-leverage:

`FAITHFUL -> FREE A -> FREE B -> variance comparison`

If a specific question remains:

`variance result -> DIRECTED take -> critics -> editorial decision`

Greg scenes include Nico's `INNER VOICE` in FREE and relevant DIRECTED takes.

Accepted prose returns may update supported relationship memory.

Rehearsal-only discoveries remain in hypothesis memory until independently supported.

## Data model guidance

Extend the current packet and discovery structures rather than creating a second engine.

Expected additions include:

- `mode`: `faithful | free | directed`
- `direction`: optional string required for DIRECTED
- `take_id`
- `variance_group_id`: optional shared identifier for comparison sets
- `memory_snapshot_id`: frozen within a variance group
- actor performance channels
- relationship-memory key
- `supported_memory`
- `hypothesis_memory`
- memory provenance
- independent-support count

Greg actor packets should declare:

- `performance_channels: [body, voice, inner_voice]`

Other actors should normally declare:

- `performance_channels: [body, voice]`

No separate Greg-only engine is introduced.

## Acceptance criteria

Implementation is complete when:

1. the engine validates and emits FAITHFUL, FREE, and DIRECTED modes
2. DIRECTED takes require an explicit direction
3. relationship-local memory has separate supported and hypothesis lanes
4. synthetic hypothesis repetition cannot self-promote
5. take-variance sets can be grouped and compared with provenance intact
6. variance siblings use the same frozen memory snapshot and cannot observe one another before comparison
7. Nico/Greg packets expose BODY, VOICE, and INNER VOICE channels
8. only Nico can author Greg's INNER VOICE
9. FREE is the default creative production take
10. high-authority scene-scale prose return is permitted on isolated editorial branches after existing safety gates
11. motif-recursion, stage-direction-density, and inner-voice critics are represented in the contract
12. existing PERFORMANCE and REHEARSAL evidence remains readable and backward-compatible
13. no write path grants unrestricted direct authority to `main`

## First campaign after implementation

After the architecture is implemented and tested, rerun the early Greg-heavy scenes in canon 001-020 with emphasis on Nico's INNER VOICE.

The first pass should not simply add more thoughts. It should compare the current prose against performed live cognition and allow thought rhythm to reshape paragraph rhythm, timing, spoken dialogue, and local narration where clearly stronger.

The high-authority FREE setting should be treated as the normal calibration for this campaign.